from batchcompute import CN_QINGDAO
# Your access_id and secret_key pair
ID = ''
KEY = ''
assert ID and KEY, 'You must supply your accsess_id and secret key.'
REGION = CN_QINGDAO

OSS_HOST = ''
OSS_BUCKET = ''
assert OSS_HOST and OSS_BUCKET, 'You also must supply a bucket \
    created with the access_id above.'

IMAGE_ID = ''
assert IMAGE_ID, "You'd better specify a valid image id."

# COUNT_TASK_NUM is the total instance count
COUNT_TASK_NUM = 2
SUM_TASK_NUM = 1

# The start number and end number which
# specify the region you want to find prime
DATA_START = 1
DATA_END = 10000

PATH_TMPL = 'oss://%s/%s'

PACKAGE_PATH = 'batch_python_sdk/package/worker.tar.gz'
# FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)
FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)

DATA_PATH = 'batch_python_sdk/data/'
FULL_DATA = PATH_TMPL%(OSS_BUCKET, DATA_PATH)
LOCAL_DATA = '/home/admin/batch_python_sdk/'

OUTPUT_PATH = 'batch-python-sdk/output/find_task_result.txt'
FULL_OUTPUT = PATH_TMPL%(OSS_BUCKET, OUTPUT_PATH)

LOG_PATH = 'oss://%s/batch_python_sdk/logs/'%OSS_BUCKET
