FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Install wkhtmltopdf and dependencies
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get -y install build-essential xorg libssl-dev libxrender-dev xvfb wget && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://bitbucket.org/wkhtmltopdf/wkhtmltopdf/downloads/wkhtmltox-0.13.0-alpha-7b36694_linux-jessie-amd64.deb && \
    dpkg -i wkhtmltox-0.13.0-alpha-7b36694_linux-jessie-amd64.deb && \
    rm wkhtmltox-0.13.0-alpha-7b36694_linux-jessie-amd64.deb

RUN printf '#!/bin/bash\nxvfb-run -a -s "-screen 0 640x480x16" wkhtmltopdf "$@"' >> /usr/bin/wkhtmltopdf.sh && \
    chmod a+x /usr/bin/wkhtmltopdf.sh

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN pip install -r /requirements/production.txt \
    && groupadd -r django \
    && useradd -r -g django django

COPY . /app
RUN chown -R django /app

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
