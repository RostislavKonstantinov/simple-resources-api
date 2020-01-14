FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade \
        pip \
        setuptools

COPY src /code
COPY requirements.txt /code
COPY start.sh /usr/bin
COPY test.sh /usr/bin

RUN pip install -r /code/requirements.txt

RUN chmod +x /usr/bin/start.sh
RUN chmod +x /usr/bin/test.sh


WORKDIR /code

EXPOSE 8000
CMD ["start.sh"]
