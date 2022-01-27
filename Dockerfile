FROM python:3.8 as requirements-stage

WORKDIR /tmp

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.8

COPY --from=requirements-stage /tmp/requirements.txt /sdgapp_code/requirements.txt

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir --upgrade -r /sdgapp_code/requirements.txt

COPY ./src /sdgapp_code/src

WORKDIR /sdgapp_code/src

CMD ["python", "main.py"]


