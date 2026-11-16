FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/of-watchdog:0.10.4 AS watchdog
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3.12-alpine

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

RUN apk --no-cache add ca-certificates

RUN addgroup -S app && adduser -S -g app app

WORKDIR /home/app/

COPY index.py .
COPY requirements.txt .

RUN chown -R app /home/app && \
    mkdir -p /home/app/python && chown -R app /home/app
USER app

ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/home/app/python

RUN pip install --no-cache-dir -r requirements.txt --target=/home/app/python

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY function/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/home/app/python

WORKDIR /home/app/

USER root
COPY function function
RUN chown -R app:app ./
USER app

ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
