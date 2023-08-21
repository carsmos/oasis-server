# Oasis-Server

Oasis-Server provides the web service for the Oasis simulation platform. It supports Oasis-Web frontend for UI and dispatches simulation tasks to Oasis-Engine. 

## Getting Started from Source


#### Prerequisites

- ubuntu 18.04

- python == 3.8

- pip

- poetry 

#### How to run

##### Installation

   ```bash
   # download repo
   git clone https://github.com/oasis-platform/oasis-server.git
   
   # go to the folder where the pyproject.toml is
   pip install -r requirements.txt

   ```

##### Configuration

before this step please make sure mysql and REDIS server is installed. and create a mysql db named 'oasis', you should update below ENV to yours.
   
   ```bash
   export REDIS_HOST=<your reids ip>
   export REDIS_PORT=<your reids port>
   export MYSQL_HOST=<your mysql ip>
   export MYSQL_ROOT_PASS=<your mysql root password>
   export MYSQL_PORT=<your mysql port>
   ```

##### Run

   ```bash
   aerich init-db
   poetry run python main.py
   ```

open browser with OpenAPI link [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

you can use this interactive doc to execute the provided request api with examples.
