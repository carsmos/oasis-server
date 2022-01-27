import uvicorn




if __name__ == "__main__":


    uvicorn.run("sdgApp.Interface.server:create_app", host="0.0.0.0", port=8000)
