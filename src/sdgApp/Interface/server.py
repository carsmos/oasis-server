import importlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import fastapi_users, auth_backend
from sdgApp.Interface import routers

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

    register_fastapi_users(app)
    register_startend(app)

    return app


def register_fastapi_users(app: FastAPI) -> None:

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




def register_startend(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup():
        # register routers
        for routermodule in routers.__all__:
            imported_module = importlib.import_module("sdgApp.Interface.routers." +
                                                      routermodule)
            app.include_router(imported_module.router)

    @app.on_event("shutdown")
    async def shutdown():
        for conn in conn_factory.values():
            conn.disconnect()
            print("{}  disconnected".format(conn))
