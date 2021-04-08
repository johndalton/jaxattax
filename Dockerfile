# Frontend asset builder
FROM node:15-alpine as frontend

ENV NPM_CONFIG_LOGLEVEL=warn
ENV PARCEL_WORKERS=1

WORKDIR /opt/jaxattax
COPY ./package.json ./yarn.lock /opt/jaxattax/

RUN yarn && \
	yarn cache clean && \
	true

COPY ./src/jaxattax/frontend /opt/jaxattax/src/jaxattax/frontend

RUN yarn run build
CMD ["yarn", "start"]

# Backend application
FROM alpine as backend

WORKDIR /opt/jaxattax

RUN apk add --no-cache \
		python3 py3-pip py3-pillow \
		postgresql-dev gcc \
		tini uwsgi uwsgi-python3 \
		jpeg-dev zlib-dev musl-dev python3-dev \
	&& true

COPY ./requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel \
	&& pip3 install --no-cache-dir pyinotify -r /tmp/requirements.txt \
	&& apk del jpeg-dev zlib-dev musl-dev python3-dev \
	&& rm /tmp/requirements.txt \
	&& true


COPY ./src /opt/jaxattax/src
COPY --from=frontend /opt/jaxattax/src/jaxattax/frontend/static /opt/jaxattax/src/jaxattax/frontend/static

ENV PYTHONUNBUFFERED=1 \
	PYTHONIOENCODING=UTF-8 \
	PYTHONDONTWRITEBYTECODE=1 \
	DJANGO_SETTINGS_MODULE=deploy.settings \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8 \
	UWSGI_PROCESSES=1

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["gunicorn", "--chdir", "src", "jaxattax.wsgi"]
