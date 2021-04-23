# Jax Ewin

Website for Jax Ewin running for Clark in the 2020 Tasmanian State election campaign.

## Development

First, make a .env file. This contains local secrets for your development environment.
If you don't intend on testing the donation workflow in development,
the Stripe API credentials can be left as the example values.

```shell
$ cp example.env .env
$ $EDITOR .env
```

Next, start the development server using Docker:


```shell
$ docker-compose build
$ docker-compose up
```

Create a new superuser using:

```shell
$ docker-compose exec backend ./src/manage.py createsuperuser
```

Visit the admin at <http://localhost/cms>.

### Stripe

Invoke the `payments` profile in `docker-compose`:

```shell
$ docker-compose --profile payments up
```


### Testing

Run the `test` container:

```shell
$ docker-compose run test
```

For an interactive session, use:

```shell
$ docker-compose run test bash
```
