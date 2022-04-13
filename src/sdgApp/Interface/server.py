import importlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sdgApp.Interface import routers
from sdgApp.Infrastructure.MongoDB.session_maker import connect, close

conn_factory = {}


def create_app() -> FastAPI:

    app = FastAPI(
        debug=True,
        title="SDG Server",
        version="v0.4.0",
        description="",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # register_startend(app)
    connect()
    register_fastapi_users(app)
    register_all_routers(app)

    return app


def register_fastapi_users(app: FastAPI) -> None:

    from sdgApp.Interface.FastapiUsers.manager import fastapi_users, auth_backend

    app.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


def register_all_routers(app: FastAPI) -> None:
    for routermodule in routers.__all__:
        imported_module = importlib.import_module("sdgApp.Interface.routers." +
                                                  routermodule)
        app.include_router(imported_module.router)


# def register_startend(app: FastAPI) -> None:
#     @app.on_event("startup")
#     async def startup():
#         # database connection init
#         await connect()
#
#
#     @app.on_event("shutdown")
#     async def shutdown():
#         # database disconnection
#         await close()
