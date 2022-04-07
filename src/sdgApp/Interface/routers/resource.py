import time

from fastapi import APIRouter, status, Depends

from sdgApp.Application.resource.usercase import ResourceQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user

router = APIRouter()


@router.get(
    "/resource",
    status_code=status.HTTP_200_OK,
    tags=["Resource"]
)
async def get_item_dic(db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return ResourceQueryUsercase(db_session=db, user=user).item_dic()
    except:
        raise


def cost_time(fun):
    def inner(*args, **kwargs):
        start_time = time.time()
        fun(*args, **kwargs)
        end_time = time.time()
        print("The func=%s cost time =%s" % (fun.__name__, end_time-start_time))
    return inner