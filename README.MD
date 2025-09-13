Recommendation Engine
=====================

_Recommendation Engine is a Python API with MongoDB_

### QuickStart

#### Prerequisites

- [uv](https://docs.astral.sh/uv/guides/install-python/) (Installed by Make command `init-venv` if not present)
- `python3.13` | I suggest to use [pyenv](https://github.com/pyenv/pyenv) and then install python via
  `pyenv install 3.13` Command
- Linux/macOS or [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) on Windows
- [GNU Make](https://www.gnu.org/software/make/)

Run the following (wait a few seconds to bring everything up and build)

```bash
make quickstart
# or if you have issues with App using docker
make quickstart-local
```

Go to http://127.0.0.1:8000

The quickstart should have brought up MongoDB and up running at http://127.0.0.1:8000 also it should have
created some test data.

Run this script to create an access token and request list API

```bash
make script-list-recommendations
```

Also, you can use the Postman collection [API_V1.postman_collection.json](./API_V1.postman_collection.json),
you need to first send a login request which will inject the access_token to the collection and then you can use
The Recommendations api.

**Stop**

```bash
make down
```

#### Application

* Go to http://127.0.0.1:8000
* Admin username: `admin`
* Admin password: `admin`

#### MongoDB Dashboard

* Go to http://localhost:18081
* Username: `admin`
* Password: `pass`

The Application at the moment **does not** have a signup feature, when up and running has an unique "admin" user
defined by these 2 environment variables:

```bash
APP_ADMIN_USERNAME=<admin-username>
APP_ADMIN_PASS_HASH=<admin-password-hash>
```

### Run locally

* Start MongoDB Application

```bash
make docker-mongo-up
```

* To run the app locally, use this command:

```bash
make run
```

API
---

### 1) Auth

```bash
curl --location 'http://127.0.0.1:8000/api/v1/auth/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "admin",
    "password": "admin"
}
'
```

Development
-----------

### Code quality

Run

```bash
make quality-checks 
```

### Tests

There are available the following commands:

```bash
# unit
make test-unit
# integration
make test-integration
# All tests
make tests

# Unit with HTML coverage
make test-unit-coverage
```

Further Reading
===============

* [MongoDB -- Time Series Data](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/data-formats/time-series/#std-label-pymongo-time-series)
* [MongoDB -- Capped Collections](https://www.mongodb.com/docs/manual/core/capped-collections/)
