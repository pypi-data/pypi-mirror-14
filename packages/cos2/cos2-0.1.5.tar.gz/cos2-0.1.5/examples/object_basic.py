# -*- coding: utf-8 -*-

import os
import shutil

import cos2


# 以下代码展示了基本的文件上传、下载、罗列、删除用法。


# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。

access_key_id = os.getenv("COS_TEST_ACCESS_KEY_ID")
access_key_secret = os.getenv("COS_TEST_ACCESS_KEY_SECRET")
bucket_name = os.getenv("COS_TEST_ENDPOINT")
endpoint = os.getenv("COS_TEST_BUCKET")



# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = cos2.Bucket(cos2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
