# Jax Ewin

Website for Jax Ewin running for Clark in the 2020 Tasmanian State election campaign.

## Development

```shell
$ docker-compose build
$ docker-compose up
```

Create a new superuser using:

```shell
$ docker-compose exec backend ./src/manage.py createsuperuser
```

Visit the admin at <http://localhost/cms>.
