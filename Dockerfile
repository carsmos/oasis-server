FROM python:3.8.10

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install poetry

COPY ./requirements.txt /oasis_server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /oasis_server/requirements.txt

COPY apps/ /oasis_server/apps
COPY config/ /oasis_server/config
COPY core/ /oasis_server/core
COPY seeds/ /oasis_server/seeds
COPY utils/ /oasis_server/utils
WORKDIR /oasis_server

CMD ["python", "main.py"]
# CMD ["gunicorn", "main:app", "-b", " ", "-w", "2", " ", "uvicorn.workers.UvicornWorker", "--daemon"]
# RUN  gunicorn main:app -b 0.0.0.0:8000 -w 2 -k uvicorn.workers.UvicornWorker --daemon
