__author__ = 'zuoqin'

import cos2
import os
if __name__ == '__main__':

    access_key_id = os.getenv("COS_TEST_ACCESS_KEY_ID")
    access_key_secret = os.getenv("COS_TEST_ACCESS_KEY_SECRET")
    bucket_name = os.getenv("COS_TEST_ENDPOINT")
    endpoint = os.getenv("COS_TEST_BUCKET")

# Init COS Python SDK


