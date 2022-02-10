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
   git clone https://codeup.aliyun.com/5f3f374f6207a1a8b17f933f/sdg_server_2.1.0.git
   
   # go to the folder where the pyproject.toml is
   poetry install 
   ```

2. Configuration

   ```python
   # src/conf.ini
   
   [DB Mongo]
   connection_string = 
   db_name = 
   
   [Queue Redis]
   host = 
   port = 
   db = 
   password = 
   ```

3. Run

   ```bash
   cd ./src
   poetry run python main.py
   ```

open browser with OpenAPI link [127.0.0.1:8000/docs]()

you can use this interactive doc to execute the provided request api with examples



## Docker

