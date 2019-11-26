FROM python:3.7

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt && rm requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
COPY ./src /app/src
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

ENTRYPOINT ["sh", "entrypoint.sh"]