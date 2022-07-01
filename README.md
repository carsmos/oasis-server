# Oasis-Server

Oasis-Server provides the web service for the Oasis simulation platform. It supports Oasis-Web frontend for UI and dispatches simulation tasks to Oasis-Engine. 

## Getting Started from Source


#### Prerequisites

- ubuntu 18.04

- python == 3.8

- pip

- poetry 

  > Poetry is a tool for **dependency management** and **packaging** in Python. See more detailed information at https://python-poetry.org/
  >
  > python 3.8 with pip and poetry can be downloaded by:
  >
  > ```bash
  > sudo apt-get update
  > sudo apt-get install python3.8
  > sudo apt-get install python3-pip
  > pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
  > pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  > pip install poetry
  > ```



#### How to run

##### Installation

   ```bash
   # download repo
   git clone https://github.com/oasis-platform/oasis-server.git
   
   # go to the folder where the pyproject.toml is
   poetry install

   ```

##### Configuration

before this step please make sure mongodb and redis server is installed. below is an example for [src/conf.ini](./src/conf.ini). you should update it to yours.
   ```python
   # src/conf.ini
   
   [DB_MONGO]
   MONGO_CONNECTION_STRING =  "mongodb://admin:123456@localhost:27017/admin?compressors=disabled&gssapiServiceName=mongodb"
   MONGO_DB_NAME = oasis
   
   [DB_REDIS]
   REDIS_HOST = localhost
   REDIS_PORT = 6379
   REDIS_DB = 0
   REDIS_PASSWORD = 123456
   USER_ID = oasis
   ```

##### Run

   ```bash
   cd ./src
   poetry run python main.py
   ```

open browser with OpenAPI link [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

you can use this interactive doc to execute the provided request api with examples.
