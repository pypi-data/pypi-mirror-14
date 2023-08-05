S3AM, pronounced ``\ˈskrēm\``, is a fast, parallel, streaming multipart
uploader for S3. It efficiently streams content from any URL for which the
locally installed libcurl and the remote server support byte range requests,
for example ``file://``, ``ftp://`` (many servers) and ``http://`` (some
servers).

S3AM is intended to be used with large files, has been tested with 300GB files
but imposes no inherent limit on the maximum file size. While it can be used to
transfer small files, you may find that it performs worse than other utilities
if the file size is below, say, 5MB.

S3AM supports encrypting the uploaded files with SSE-C.

S3AM can also copy objects between buckets and within a bucket, and do so
without actually transferring any data between client and server. It supports
the use of separate SSE-C encryption keys for source and destination of the
copy operation so it can be used to efficiently re-encrypt an object.

S3AM uses the PyCurl bindings for libcurl and Python's multiprocessing module
to work around lock contention in the Python interpreter and to avoid potential
thread-safety issues with libcurl.


Prerequisites
=============

Python 2.7.x, libcurl and pip.

On Ubuntu the dependencies can be installed with

::

   sudo apt-get install python-dev gcc make libcurl4-openssl-dev


Installation
============

It is recommended that you install S3AM into a virtualenv::

   virtualenv ~/s3am && source ~/s3am/bin/activate
   pip install s3am

If you get ``No distributions matching the version for s3am`` or if you would
like to install the latest unstable release, you may want to run ``pip install
--pre s3am`` instead.

If you get ``libcurl link-time ssl backend (nss) is different from compile-time
ssl backend`` the required fix is to prefix the pip installation command with
``PYCURL_SSL_LIBRARY=nss``, for example ``PYCURL_SSL_LIBRARY=nss pip install
s3am --pre``.

Optionally, add a symbolic link to the ``s3am`` command such that you don't
need to activate the virtualenv before using it::

   mkdir -p ~/bin
   ln -s ~/s3am/bin/s3am ~/bin

Then append ``~/bin`` to your ``PATH`` environment variable. I would tell you
explicitly how to modify ``PATH`` but unfortunately this depends on various
factors, e.g. which shell you are using and which operating system. On OS X,
for example, you need to edit ``~/.profile`` and append

::

   export PATH="$HOME/bin:$PATH"

Configuration
=============

Obtain an access and secret key for AWS. Create ``~/.boto`` with the following
contents::

   [Credentials]
   aws_access_key_id = PASTE YOUR ACCESS KEY ID HERE
   aws_secret_access_key = PASTE YOUR SECRET ACCESS KEY HERE

Please note that while S3AM is designed to support credentials injected to an
EC2 instance via instance profiles and IAM roles, this currently does not `work
reliably <https://github.com/BD2KGenomics/s3am/issues/16>`_.

The ``~/.boto`` file is being deprecated. Consider using ``~/.aws/credentials``
instead. It is supported by various AWS SDKs and allows for easily switching
between different AWS accounts (profiles)::

    [foo]
    aws_access_key_id=PASTE_YOUR_FOO_ACCESS_KEY_ID_HERE
    aws_secret_access_key=PASTE_YOUR_FOO_SECRET_KEY_ID_HERE
    region=us-west-2

    [bar]
    aws_access_key_id=PASTE_YOUR_BAR_ACCESS_KEY_ID_HERE
    aws_secret_access_key=PASTE_YOUR_BAR_SECRET_KEY_ID_HERE
    region=us-west-2

To choose an active profile, set the ``AWS_PROFILE`` environment variable::

    export AWS_PROFILE=foo

.. _access key: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html

Usage
=====

Run with ``--help`` to display usage information::

   s3am --help

For example::

   s3am upload \
        ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data/NA12878/sequence_read/ERR001268.filt.fastq.gz \
        bd2k-test-data

If an upload was interrupted you can resume it by running the command again
with the ``--resume`` option. To cancel an unfinished upload, run ``s3am
cancel``. Be aware that incomplete multipart uploads do incur storage fees.


Optimization
============

By default S3AM concurrently transfers one part per core. This is a very
conservative setting. Since S3AM is mostly IO-bound you should significantly
oversubscribe cores, probably by a factor of at least 10. On a machine with 8
cores, for example, you should run S3AM with ``--download-slots 40
--upload-slots 40``.

If you run S3AM on EC2, you will likely have more bandwidth to S3 than from the
source server. In this case it might help to have more download than upload
slots.

The default part size of 5MB is also very conservative. If the source has a
high latency, you will want to increase that as it might take a while for the
TCP window to grow to an optimal size. If the source is ``ftp://`` there will
be significantly more round-trips before the actual transfer starts than with
``http://`` or ``http://``. In either case you should probably increase the
part size to at least 50MB.


Building
========

Clone the repository, create a virtualenv, activate it and run `make develop`::

    git clone https://github.com/BD2KGenomics/s3am.git
    cd s3am
    virtualenv venv
    venv/bin/activate
    make develop


Encryption
==========

With SSE-C, the S3 server performs the actual encryption but the client
provides the encryption key. This is more secure than plain SSE because with
SSE-C the secret encryption key is not persisted on the server, it only exists
there in memory for the duration of a request and is discarded afterwards.
SSE-C also lets you make a bucket public and control access via the
distribution of encryption keys.


Scripting
=========

You can enable resumption and keep trying a few times::

    for i in 1 2 3; do s3am upload --resume $src $dst && break; done
    s3am cancel $dst

There are situations after which resumption is futile and care must be taken
not to get into an infinite loop that would likely cost an infinite amount of
money. S3AM exits with status code 2 on obvious user errors but there may be
other failures like auth problems where user intervention is required. There is
no reliable way to classify errors into resumable and non-resumable ones so
S3AM doesn't even try. Running ``s3am cancel`` is a best effort to avoid
leaving unfinished uploads. If ``s3am upload`` was successful for a given
object, running ``s3am cancel`` on that object does nothing.

Alternatively, you can force S3AM to eradicate previous, unsuccessful attempts,
creating a clean slate and preventing them from corrupting the current attempt.
This comes at the expense of wasting resources by discarding the progress made
in those previous attempts::

   for i in 1 2 3; s3am upload --force $src $dst && break; done
   s3am cancel $dst
   
The --force and --resume options are mutually exclusive, but both provide a
certain degree of idempotence. While ``--resume`` refuses to function if it
detects *multiple* unfinished uploads for a given S3 object, ``--force`` is not
so easily dissuaded. Hence the name.

In a Toil script I would either use the ``--resume`` option with a hand-coded
loop or the ``--force`` option while relying on Toil's built-in job retry
mechanism.


Caveats
=======

S3AM doesn't support non-US buckets yet. See issue #12.

S3AM uses a buffer per upload and download slot. The buffer will hold an entire
part. This means that the lower bound of S3AM's memory footprint is
(download_slots + upload_slots) * part_size. The buffer is needed because S3
doesn't support chunked transfer coding.

S3AM does not implement back-to-back checksumming. An MD5 is computed for every
part uploaded to S3 but there is no code in place to compare the MD5 with the
source side. I think S3 exposes the MD5 of all part MD5's concatenated. So if
we could get libcurl and the sending server to support the Content-MD5 HTTP
header we could use that. But that would not be as strong a guarantee as
verifying the MD5 over the file in its entirety.
