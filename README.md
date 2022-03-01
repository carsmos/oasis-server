# SDG-App



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

1. Installation

   ```bash
   # download repo
   git clone https://codeup.aliyun.com/5f3f374f6207a1a8b17f933f/sdg-server.git
   
   # go to the folder where the pyproject.toml is
   poetry install 
   ```

2. Configuration

   ```python
   # src/conf.ini
   
   [DB_MONGO]
   MONGO_CONNECTION_STRING = 
   MONGO_DB_NAME = 
   
   [DB_REDIS]
   REDIS_HOST = 
   REDIS_PORT = 
   REDIS_DB = 
   REDIS_PASSWORD = 
   ```

3. Run

   ```bash
   cd ./src
   poetry run python main.py
   ```

open browser with OpenAPI link [127.0.0.1:8000/docs]()

you can use this interactive doc to execute the provided request api with examples



## Docker

1.拉取镜像

```bash
docker pull registry.cn-beijing.aliyuncs.com/selfdriveguard/sdg-server:0.3.2
```

此镜像的制作是基于根目录下的dockerfile

2.编辑docker-compose.yml

```yaml
services: 
    app:
        image:
        ports:
            - "8000:8000"
        environment: 
            REDIS_HOST: ""
            REDIS_PORT: ""
            REDIS_DB: ""
            REDIS_PASSWORD: ""
            MONGO_CONNECTION_STRING: ""
            MONGO_DB_NAME: ""
```

3. Run

```bash
docker-compose -f docker-compose.yml -p sdg-replay up -d
```

4. Stop

```bash
docker-compose -p sdg-replay down
```

