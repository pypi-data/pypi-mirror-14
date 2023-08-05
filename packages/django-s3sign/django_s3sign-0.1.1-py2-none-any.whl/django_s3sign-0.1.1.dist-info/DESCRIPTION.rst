[![Build Status](https://travis-ci.org/ccnmtl/django-s3sign.svg?branch=master)](https://travis-ci.org/ccnmtl/django-s3sign)
[![Coverage Status](https://coveralls.io/repos/github/ccnmtl/django-s3sign/badge.svg?branch=master)](https://coveralls.io/github/ccnmtl/django-s3sign?branch=master)

# django-s3sign
s3 sign view for django

## installation

    $ pip install django-s3sign

## usage

Add `s3sign` to `INSTALLED_APPS`. Subclass `s3sign.views.SignS3View`
and override as needed. Eg with a different root path:


```
from s3sign.views import SignS3View

...

class MySignS3View(LoggedInView, SignS3View):
    root = 'uploads/'
```

With a different S3 bucket:

```
class MySignS3View(LoggedInView, SignS3View):
    def get_bucket(self):
        return settings.DIFFERENT_BUCKET_NAME
```

Attributes you can override:

```
    name_field = 's3_object_name'
    type_field = 's3_object_type'
    expiration_time = 10
    mime_type_extensions = [
        ('jpeg', '.jpg'),
        ('png', '.png'),
        ('gif', '.gif'),
    ]
    default_extension = '.obj'
    root = ''
    path_string = (
        "{root}{now.year:04d}/{now.month:02d}/"
        "{now.day:02d}/{basename}{extension}")
    amz_headers = "x-amz-acl:public-read"
```

Methods you can override:

```
get_aws_access_key(self)
get_aws_secret_key(self)
get_bucket(self)
get_mimetype(self, request)
extension_from_mimetype(self, mime_type)
now(self) # useful for unit tests
now_time(self) # useful for unit tests
basename(self)
get_object_name(self, extension)
```



