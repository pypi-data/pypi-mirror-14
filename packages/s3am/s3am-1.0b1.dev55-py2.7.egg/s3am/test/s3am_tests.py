# Copyright (C) 2015 UCSC Computational Genomics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import logging
import socket
import time
import unittest
from contextlib import closing
from tempfile import mkdtemp
from threading import Lock

import FTPd
import boto.exception
import boto.s3
import os
import pyftpdlib.handlers
import s3am
import s3am.boto_utils
import s3am.cli
import s3am.operations

# The dot in the domain name makes sure that boto.work_around_dots_in_bucket_names() is covered
from bd2k.util.iterables import concat

test_bucket_name_prefix = 's3am-unit-tests.foo'
test_bucket_region = 'us-west-1'
copy_bucket_region = 'us-east-1' # using us-east-1 so we get exposed to its quirks

host = "127.0.0.1"
port = 21212
part_size = s3am.operations.min_part_size
two_and_a_half_parts = int( part_size * 2.5 )
two_parts = 10 * 1024 * 1024
test_sizes = [ 0, 1, part_size - 1, part_size, part_size + 1, two_parts, two_and_a_half_parts ]

verbose = ('--verbose',)  # ('--debug',)

num_slots = 4  # how many download and upload slots to use

log = logging.getLogger( __name__ )

slots = ('--download-slots', str( num_slots ), '--upload-slots', str( num_slots ))
one_slot = ('--download-slots', '1', '--upload-slots', '0')


def md5( contents ):
    return hashlib.md5( contents ).hexdigest( )


class TestFile( object ):
    def __init__( self, ftp_root, size ):
        self.ftp_root = ftp_root
        self.size = size
        buf = bytearray( os.urandom( size ) )
        self.md5 = md5( buf )
        with open( self.path, 'w' ) as f:
            f.write( buf )

    @property
    def name( self ):
        return 'test-%i.bin' % self.size

    @property
    def path( self ):
        return os.path.join( self.ftp_root, self.name )


class OperationsTests( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        super( OperationsTests, cls ).setUpClass( )
        s3am.boto_utils.work_around_dots_in_bucket_names( )

    def setUp( self ):
        super( OperationsTests, self ).setUp( )
        self.netloc = '%s:%s' % (host, port)
        self.src_url = 'ftp://%s/' % self.netloc
        self.s3 = s3am.boto_utils.s3_connect_to_region( test_bucket_region )
        self.test_bucket_name = '%s-%i' % (test_bucket_name_prefix, int( time.time( ) ))
        test_bucket_location = s3am.boto_utils.region_to_bucket_location( test_bucket_region )
        self.bucket = self.s3.create_bucket( self.test_bucket_name, location=test_bucket_location )
        self._clean_bucket( self.bucket )
        self.ftp_root = mkdtemp( prefix=__name__ )
        self.test_files = { size: TestFile( self.ftp_root, size ) for size in test_sizes }
        self.ftpd = FTPd.FTPd( self.ftp_root, address=(host, port), dtp_handler=UnreliableHandler )
        logging.getLogger( 'pyftpdlib' ).setLevel( logging.WARN )
        self.ftpd.start( )

    def _clean_bucket( self, bucket ):
        for upload in bucket.list_multipart_uploads( ):
            upload.cancel_upload( )
        for key in bucket.list( ):
            key.delete( )

    def tearDown( self ):
        self.ftpd.stop( )
        self._clean_bucket( self.bucket )
        self.bucket.delete( )
        self.s3.close( )
        for test_file in self.test_files.itervalues( ):
            os.unlink( test_file.path )
        os.rmdir( self.ftp_root )

    def _assert_key( self, test_file, sse_key=None ):
        headers = { }
        if sse_key is not None:
            s3am.operations.Upload._add_encryption_headers( sse_key, headers )
        key = self.bucket.get_key( test_file.name, headers=headers )
        self.assertEquals( key.size, test_file.size )
        self.assertEquals( md5( key.get_contents_as_string( headers=headers ) ), test_file.md5 )

    def test_upload( self ):
        for test_file in self.test_files.itervalues( ):
            s3am.cli.main( concat(
                'upload', verbose, slots,
                self.src_url + test_file.name, self.dst_url( ) ) )
            self._assert_key( test_file )

    def dst_url( self, bucket_name=None, file_name=None ):
        return 's3://%s/%s' % (bucket_name or self.test_bucket_name, file_name or '')

    def test_encryption( self ):
        test_file = self.test_files[ two_and_a_half_parts ]
        src_url = self.src_url + test_file.name
        sse_key = '-0123456789012345678901234567890'
        s3am.cli.main( concat(
            'upload', verbose, slots, src_url, self.dst_url( ),
            '--sse-key=' + sse_key ) )
        self._assert_key( test_file, sse_key=sse_key )
        # Ensure that we can't actually retrieve the object without specifying an encryption key
        try:
            self._assert_key( test_file )
        except boto.exception.S3ResponseError as e:
            self.assertEquals( e.status, 400 )
        else:
            self.fail( )

    def test_resume( self ):
        test_file = self.test_files[ two_and_a_half_parts ]
        src_url = self.src_url + test_file.name

        # Run with a simulated download failure
        UnreliableHandler.setup_for_failure_at( int( 0.75 * test_file.size ) )
        try:
            s3am.cli.main( concat( 'upload', verbose, one_slot, src_url, self.dst_url( ) ) )
        except s3am.WorkerException:
            pass
        else:
            self.fail( )

        # Retrying without --resume should fail
        try:
            s3am.cli.main( concat( 'upload', verbose, slots, src_url, self.dst_url( ) ) )
        except s3am.UserError as e:
            self.assertIn( "unfinished upload", e.message )
        else:
            self.fail( )

        # Retrying with --resume and different part size should fail
        try:
            s3am.cli.main( concat(
                'upload', verbose, slots, src_url, self.dst_url( ),
                '--resume', '--part-size', str( 2 * part_size ) ) )
        except s3am.UserError as e:
            self.assertIn( "part size appears to have changed", e.message )
        else:
            self.fail( )

        # Retry
        s3am.cli.main( concat( 'upload', verbose, slots, src_url, self.dst_url( ), '--resume' ) )

        # FIMXE: We should assert that the resume skips existing parts

        self._assert_key( test_file )

    def test_force( self ):
        test_file = self.test_files[ two_and_a_half_parts ]
        src_url = self.src_url + test_file.name

        # Run with a simulated download failure
        UnreliableHandler.setup_for_failure_at( int( 0.75 * test_file.size ) )
        try:
            s3am.cli.main( concat( 'upload', verbose, one_slot, src_url, self.dst_url( ) ) )
        except s3am.WorkerException:
            pass
        else:
            self.fail( )

        # Retrying without --resume should fail
        try:
            s3am.cli.main( concat( 'upload', verbose, slots, src_url, self.dst_url( ) ) )
        except s3am.UserError as e:
            self.assertIn( "unfinished upload", e.message )
        else:
            self.fail( )

        # Retrying with --force should suceed. We use a different part size to ensure that
        # transfer is indeed started from scratch, not resumed.
        s3am.cli.main( concat(
            'upload', verbose, slots, src_url, self.dst_url( ),
            '--force', '--part-size', str( 2 * part_size ) ) )

    def test_cancel( self ):
        test_file = self.test_files[ two_and_a_half_parts ]
        src_url = self.src_url + test_file.name

        # Run with a simulated download failure
        UnreliableHandler.setup_for_failure_at( int( 0.75 * test_file.size ) )
        try:
            s3am.cli.main( concat( 'upload', verbose, one_slot, src_url, self.dst_url( ) ) )
        except s3am.WorkerException:
            pass
        else:
            self.fail( )

        # A retry without --resume should fail.
        try:
            s3am.cli.main( concat( 'upload', verbose, slots, src_url, self.dst_url( ) ) )
        except s3am.UserError as e:
            self.assertIn( "unfinished upload", e.message )
        else:
            self.fail( )

        # Cancel
        s3am.cli.main( concat( 'cancel', verbose, self.dst_url( file_name=test_file.name ) ) )

        # Retry, should succeed
        s3am.cli.main( concat( 'upload', verbose, slots, src_url, self.dst_url( ) ) )

    def test_copy( self ):
        # setup already created the destination bucket
        dst_bucket_name = self.test_bucket_name
        src_bucket_name = dst_bucket_name + '-src'
        with closing( s3am.boto_utils.s3_connect_to_region( copy_bucket_region ) ) as s3:
            src_location = s3am.boto_utils.region_to_bucket_location( copy_bucket_region )
            src_bucket = s3.create_bucket( src_bucket_name, location=src_location )
            try:
                self._clean_bucket( src_bucket )
                for test_file in self.test_files.itervalues( ):
                    src_url = self.src_url + test_file.name
                    src_sse_key = '-0123456789012345678901234567890'
                    dst_sse_key = 'skdjfh9q4rusidfjs9fjsdr9vkfdh833'
                    dst_url = self.dst_url( src_bucket_name, test_file.name )
                    s3am.cli.main( concat(
                        'upload', verbose, slots, src_url, dst_url,
                        '--sse-key=' + src_sse_key ) )
                    src_url = dst_url
                    dst_url = self.dst_url( )
                    s3am.cli.main( concat(
                        'upload', verbose, slots, src_url, dst_url,
                        '--src-sse-key=' + src_sse_key,
                        '--sse-key=' + dst_sse_key ) )
                    self._assert_key( test_file, dst_sse_key )
            finally:
                self._clean_bucket( src_bucket )
                src_bucket.delete( )

    def test_verify( self ):
        for test_file in self.test_files.itervalues( ):
            s3am.cli.main( concat(
                'upload', verbose, slots,
                self.src_url + test_file.name, self.dst_url( ) ) )
            self._assert_key( test_file )
            buffer_size = s3am.operations.verify_buffer_size
            for verify_part_size in { buffer_size, part_size }:
                md5 = s3am.cli.main( concat(
                    'verify',
                    '--part-size', str( verify_part_size ),
                    self.dst_url( file_name=test_file.name ) ) )
                self.assertEquals( test_file.md5, md5 )


class UnreliableHandler( pyftpdlib.handlers.DTPHandler ):
    """
    Lets us trigger an IO error during the download
    """

    def send( self, data ):
        self._simulate_error( data )
        return pyftpdlib.handlers.DTPHandler.send( self, data )

    lock = Lock( )
    error_at_byte = None
    sent_bytes = 0

    @classmethod
    def _simulate_error( cls, data ):
        with cls.lock:
            if cls.error_at_byte is not None:
                cls.sent_bytes += len( data )
                if cls.sent_bytes > cls.error_at_byte:
                    log.info( 'Simulating error at %i', cls.sent_bytes )
                    cls.error_at_byte = None
                    cls.sent_bytes = 0
                    raise socket.error( )
                else:
                    log.info( 'Not simulating error at %i', cls.sent_bytes )

    @classmethod
    def setup_for_failure_at( cls, offset ):
        with cls.lock:
            cls.error_at_byte = offset
            cls.sent_bytes = 0
