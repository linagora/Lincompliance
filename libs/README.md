# Lincompliance python library
Main source of the lincompliance api implementation.

## Structure
```
libs
 └── pyproject.toml
 └── setup.cfg
 └── setup.py
 └── tox.ini
 └── README.md
 └── src
 │   └──package1
 │   └──package2
 │   └──...
 └── tests
    └──package1
    └──package2
    └──...
```

## Test
### Requirements
    * python3-devel
    * python3.6-8-7-9
    * tox
    * pytest (if you don't need tox isolation system)

### Tox
Thanks to tox, we can run all tests in different python environment.
To run them just execute the following command:
```shell
tox -q
```

### Pytest
```shell
pytest -s # will print all output including the program's
```

### Docker
Because of the ort script needed to execute the core of the project, it is easier to execute all tests from a docker container.
You can execute all tests thanks to the dev.Dockerfile, it already implements all needed dependencies and python tested version.
#### Via command lines 
```shell
export DOCKER_BUILDKIT=1 # Needed for both builds
docker build . -f docker/build.Dockerfile  -t linc/base
docker build . -f docker/dev.Dockerfile  -t linc/test 
docker run -itd --mount type=bind,src="$(readlink -f ./libs)",dst=/root/libs linc/test
```
You can execute the last command each time to tests all project.
#### Via Makefile
```shell
make docker_build
make docker_dev
make docker_dev_run
```
#### Tests execution
Because we already mount the library folder to the container, all changes made on the host machine in the python code will be applied on the docker tests.
Also, all conf changes are also applied. If you don't need to test with all python version, pytest is installed on the container. The tested version will be python3.6.
```shell
docker exec -it <container_id> tox <tox_options>
docker exec -it <container_id> pytest <pytest>
```