# -*- coding: utf-8 -*-

import unittest
import cos2
import socket
import sys
from common import *


class TestApiBase(CosTestCase):
    # if COS_CNAME:
    #     def test_cname_bucket(self):
    #         bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), COS_CNAME, COS_BUCKET, is_cname=True)
    #         bucket.get_bucket_acl()
    #
    #     def test_cname_object(self):
    #         bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), COS_CNAME, COS_BUCKET, is_cname=True)
    #         bucket.put_object(self.random_key('test'), 'hello world')

    #def test_https(self):
    #    bucket_name = random_string(63)
    #    bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), 'https://cos2.chinac.com', bucket_name)
    #    self.assertRaises(cos2.exceptions.NoSuchBucket, bucket.get_object, 'hello.txt')

    # 只是为了测试，请不要用IP访问COS，除非你是在VPC环境下。
   # def test_ip(self):
   #     bucket_name = random_string(63)

   #     bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), COS_CNAME, bucket_name)
   #     self.assertRaises(cos2.exceptions.NoSuchBucket, bucket.get_object, 'hello.txt')

    #def test_invalid_bucket_name(self):
    #    bucket_name = random_string(64)
    #    bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), COS_CNAME, bucket_name)
    #    self.assertRaises(cos2.exceptions.NoSuchBucket, bucket.get_object, 'hello.txt')

    def test_whitespace(self):
        bucket = cos2.Bucket(cos2.Auth(COS_ID, ' ' + COS_SECRET + ' '), COS_ENDPOINT, COS_BUCKET)
        bucket.get_bucket_acl()

        bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), ' ' + COS_ENDPOINT + ' ', COS_BUCKET)
        bucket.get_bucket_acl()

        bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), COS_ENDPOINT, ' ' + COS_BUCKET + ' ')
        bucket.get_bucket_acl()

    if sys.version_info >= (3, 3):
        def test_user_agent(self):
            app = 'fantastic-tool'

            assert_found = False
            def do_request(session_self, req, timeout):
                if assert_found:
                    self.assertTrue(req.headers['User-Agent'].find(app) >= 0)
                else:
                    self.assertTrue(req.headers['User-Agent'].find(app) < 0)

                raise cos2.exceptions.ClientError('intentional')

            from unittest.mock import patch
            with patch.object(cos2.Session, 'do_request', side_effect=do_request, autospec=True):
                # 不加 app_name
                assert_found = False
                self.assertRaises(cos2.exceptions.ClientError, self.bucket.get_bucket_acl)

                service = cos2.Service(cos2.Auth(COS_ID, COS_SECRET), COS_ENDPOINT)
                self.assertRaises(cos2.exceptions.ClientError, service.list_buckets)

                # 加app_name
                assert_found = True
                bucket = cos2.Bucket(cos2.Auth(COS_ID, COS_SECRET), COS_ENDPOINT, COS_BUCKET,
                                     app_name=app)
                self.assertRaises(cos2.exceptions.ClientError, bucket.get_bucket_acl)

                service = cos2.Service(cos2.Auth(COS_ID, COS_SECRET), COS_ENDPOINT,
                                       app_name=app)
                self.assertRaises(cos2.exceptions.ClientError, service.list_buckets)


if __name__ == '__main__':
    unittest.main()