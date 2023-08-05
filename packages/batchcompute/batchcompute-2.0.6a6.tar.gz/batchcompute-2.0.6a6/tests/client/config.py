from batchcompute import CN_QINGDAO as REGION
# Your access_id and secret_key pair
ID = ''
KEY = ''
assert ID and KEY, 'You must supply your accsess_id and secret key.'

OSS_HOST = ''
OSS_BUCKET = ''
assert OSS_HOST and OSS_BUCKET, 'You also must supply a bucket \
    created with the access_id above.'

LINUX_IMAGE_ID = ''
WINDOWS_IMAGE_ID = ''
assert LINUX_IMAGE_ID or WINDOWS_IMAGE_ID, "You'd better specify a valid image id."

PATH_TMPL = 'oss://%s/%s'

PACKAGE_PATH = 'batchcompute_python_sdk/package/worker.tar.gz'
# FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)
FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)

DATA_PATH = 'batchcompute_python_sdk/data/'
FULL_DATA = PATH_TMPL%(OSS_BUCKET, DATA_PATH)
LOCAL_DATA = '/home/admin/batch_python_sdk/'

OUTPUT_PATH = 'batchcompute_python_sdk/output/find_task_result.txt'
FULL_OUTPUT = PATH_TMPL%(OSS_BUCKET, OUTPUT_PATH)

LOG_PATH = 'oss://%s/batchcompute_python_sdk/logs/'%OSS_BUCKET
