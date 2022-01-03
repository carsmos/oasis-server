import uvicorn

from sdgApp.Interface.server import create_app



if __name__ == "__main__":

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn.run("sdgApp.Interface.server:create_app", host="0.0.0.0", port=8000)
