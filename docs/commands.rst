Commands
========

The Makefile contains the central entry points for common tasks related to this project.

Syncing data to S3
^^^^^^^^^^^^^^^^^^

* `make sync_data_to_s3` will use `aws s3 sync` to recursively sync files in `data/` up to `s3://[OPTIONAL] your bucket and folder for s3, as you would use it with the aws cli. Do not include a trailing / in the url. For example s3://foo/bar/data/`.
* `make sync_data_from_s3` will use `aws s3 sync` to recursively sync files from `s3://[OPTIONAL] your bucket and folder for s3, as you would use it with the aws cli. Do not include a trailing / in the url. For example s3://foo/bar/data/` to `data/`.
