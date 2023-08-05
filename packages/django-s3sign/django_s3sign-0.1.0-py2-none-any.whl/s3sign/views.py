import base64
import hmac
import json
import time
import urllib
import uuid

from datetime import datetime
from hashlib import sha1

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View


class SignS3View(View):
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

    def get_aws_access_key(self):
        return settings.AWS_ACCESS_KEY

    def get_aws_secret_key(self):
        return settings.AWS_SECRET_KEY

    def get_bucket(self):
        return settings.AWS_UPLOAD_BUCKET

    def get_mimetype(self, request):
        return request.GET.get(self.type_field)

    def extension_from_mimetype(self, mime_type):
        for m, ext in self.mime_type_extensions:
            if m in mime_type:
                return ext
        return self.default_extension

    def now(self):
        return datetime.now()

    def now_time(self):
        return time.time()

    def basename(self):
        return str(uuid.uuid4())

    def get_object_name(self, extension):
        now = self.now()
        basename = self.basename()
        return self.path_string.format(
            now=now, basename=basename, extension=extension,
            root=self.root)

    def get(self, request):
        AWS_ACCESS_KEY = self.get_aws_access_key()
        AWS_SECRET_KEY = self.get_aws_secret_key()
        S3_BUCKET = self.get_bucket()
        mime_type = self.get_mimetype(request)
        extension = self.extension_from_mimetype(mime_type)

        object_name = self.get_object_name(extension)

        expires = int(self.now_time() + self.expiration_time)

        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (
            mime_type, expires, self.amz_headers, S3_BUCKET, object_name)

        signature = base64.encodestring(
            hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
        signature = urllib.quote_plus(signature.strip())

        # Encode the plus symbols
        # https://pmt.ccnmtl.columbia.edu/item/95796/
        signature = urllib.quote(signature)

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
        signed_request = '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (
            url, AWS_ACCESS_KEY, expires, signature)

        return HttpResponse(
            json.dumps({
                'signed_request': signed_request,
                'url': url
            }), content_type="application/json")
