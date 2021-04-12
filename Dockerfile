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
FROM python:3-slim as backend

WORKDIR /opt/jaxattax

RUN apt-get update -y \
	&& apt-get install \
		-y --no-install-recommends \
		tini \
		build-essential \
		libjpeg-dev zlib1g-dev musl-dev libffi-dev \
	&& true

COPY ./requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel \
	&& pip3 install --no-cache-dir pyinotify -r /tmp/requirements.txt \
	&& apt-get remove -y --auto-remove \
		build-essential \
		libjpeg-dev zlib1g-dev musl-dev libffi-dev \
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
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["gunicorn", "--chdir", "src", "jaxattax.wsgi"]
