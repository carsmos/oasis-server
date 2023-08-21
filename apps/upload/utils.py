import datetime
import os
import random
import oss2

from core import settings

def get_path_format_vars():
    return {
        "datetime": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "rnd": random.randrange(100, 999)
    }


def get_output_file_info(path_format, path_format_vars):
    outputFile = "%(datetime)s_%(rnd)s_%(basename)s.%(extname)s"% path_format_vars
    outputFile = outputFile.replace("/", "_")
    outputPath = os.path.join(path_format, outputFile)
    return outputPath


def upload_file_to_oss(filename, file):
    access_id = settings.ACCESSID if settings.ACCESSID else "XXXXXXXXX"
    access_key = settings.ACCESSKEY if settings.ACCESSKEY else "XXXXXXX"
    auth = oss2.Auth(access_id, access_key)
    bucket_endpoint = settings.BUCKET_ENDPOINT if settings.BUCKET_ENDPOINT else "https://oss-accelerate.aliyuncs.com"
    object_path = settings.OBJECT_PATH if settings.OBJECT_PATH else "local/email/images"
    bucket_name = settings.BUCKET  if settings.BUCKET else "sdg-bags"

    upload_origin_name, upload_origin_ext = os.path.splitext(filename)
    path_format_var = get_path_format_vars()
    path_format_var.update({
        "basename": upload_origin_name,
        "extname": upload_origin_ext[1:],
        "filename": filename
    })

    file_path = get_output_file_info(object_path, path_format_var)

    bucket = oss2.Bucket(auth, bucket_endpoint, bucket_name)

    ret = bucket.put_object(file_path, file.file)

    a = list(bucket_endpoint)
    a.insert(8, '{}.'.format(bucket_name))
    download_endpoint = ''.join(a)
    image_url = "{}/{}".format(download_endpoint, file_path)
    print("upload image to oss sucessful! url=%s" % image_url)

    return image_url, ret


def upload_file(files):
    filename = files.filename
    try:
        image_url, ret = upload_file_to_oss(filename, files)
        if ret.status == 200:
            ret_info = {"errno": 0, "data": {"url": image_url}}
        else:
            ret_info = {"errno": 1, "message": ret.resp.response.reason}
        return ret_info
    except Exception as e:
        print(e)
        raise Exception