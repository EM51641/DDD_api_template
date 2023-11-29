# Domain Driven Development Template


## Information

- This repository hosts an example of an API developed using clean coding patterns and test driven development.

- It uses the devconainer setup tool to ease environment replication.

## Setup
It contains a generic entity model Part that describes the physical things that we manufacture or use in the manufacturing process (bolts, screws, speaker drivers and cabinets, cables, fully assembled modules, ...).
We store all of the data in the Postgres database, which has a single table named `parts`.
The interaction with the database is done with the [SQLAlchemy](https://www.sqlalchemy.org/) library, and the simple GET, POST, and DELETE endpoints are exposed via the API, which is written with the [FastAPI](https://fastapi.tiangolo.com/) framework.

To manage dependencies, we use [poetry](https://python-poetry.org/).
Additional guidelines can be found in [CONTRIBUTING.md](/CONTRIBUTING.md).

To launch an API instance, you should:
1. Have a running Postgres instance, e.g. in a container. The application will read the [/devcontainer/.env](.env) file to setup the database.
2. Create a virtual environment and install the dependencies in it. You can run `poetry install` for that.
3. Use [start_app.sh](/start_app.sh) to run the server. By default, it will bind to http://localhost:8000.
4. An automatically generated documentation can be found at http://localhost:8000/docs. The endpoints are accessible at http://localhost:8000/api/<endpoint_name>.



## Additional Information
The whole environment can be started using the command (Meanwhile, you should use the devcontainer technology to run. On ```VSCode```, you can run the build and run the containarized environment with the command: ```@command:remote-containers.rebuildAndReopenInContainer```):

```shell
$ docker compose -f .devcontainer/docker-compose.yml up --detach
```
