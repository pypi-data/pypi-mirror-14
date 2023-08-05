# -*- coding: utf-8 -*-

import os
import random
import string
import cos2


# 以下代码展示了文件上传的高级用法，如断点续传、分片上传等。
# 基本的文件上传如上传普通文件、追加文件，请参见object_basic.py


# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
#
# 以杭州区域为例，Endpoint可以是：
#   http://cos2.chinac.com
#   https://cos2.chinac.com
# 分别以HTTP、HTTPS协议访问。
access_key_id = os.getenv("COS_TEST_ACCESS_KEY_ID")
access_key_secret = os.getenv("COS_TEST_ACCESS_KEY_SECRET")
bucket_name = os.getenv("COS_TEST_ENDPOINT")
endpoint = os.getenv("COS_TEST_BUCKET")


# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = cos2.Bucket(cos2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
#bucket.create_bucket()

def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

# 生成一个本地文件用于测试。文件内容是bytes类型。
filename = "my-first-cos-upload.txt"
content = cos2.to_bytes(random_string(102*1024 * 1024 ))

with open(filename, 'wb') as fileobj:
    fileobj.write(content)


# 也可以直接调用分片上传接口。
# 首先可以用帮助函数设定分片大小，设我们期望的分片大小为128KB
total_size = os.path.getsize(filename)
part_size = cos2.determine_part_size(total_size, preferred_size=101*1024*1024)

# 初始化分片上传，得到Upload ID。接下来的接口都要用到这个Upload ID。
key = 'remote-multipart.txt'
upload_id = bucket.init_multipart_upload(key).upload_id

# 逐个上传分片
# 其中cos2.SizedFileAdapter()把fileobj转换为一个新的文件对象，新的文件对象可读的长度等于num_to_upload
with open(filename, 'rb') as fileobj:
    parts = []
    part_number = 1
    offset = 0
    while offset < total_size:
        num_to_upload = min(part_size, total_size - offset)
        result = bucket.upload_part(key, upload_id, part_number,
                                    cos2.SizedFileAdapter(fileobj, num_to_upload))
        print(result.etag)
        parts.append(cos2.models.PartInfo(part_number, result.etag))

        offset += num_to_upload
        part_number += 1

    # 完成分片上传
    bucket.complete_multipart_upload(key, upload_id, parts)


# 验证一下
#with open(filename, 'rb') as fileobj:
#    assert bucket.get_object(key).read() == fileobj.read()

os.remove(filename)
