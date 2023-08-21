from fastapi import APIRouter, Depends, status, HTTPException, Request, UploadFile, File

from . import utils

router = APIRouter()


@router.post(
    "/upload_files",
    summary='上传文件',
    tags=["Email"]
)
async def files(files: UploadFile = File(...)):
    try:
        ret_infors = utils.upload_file(files)
        return ret_infors
    except Exception:
        assert False, '上传失败'
