# Lincompliance (Early Bird)

## Prerequis

* docker
* docker-compose
* make


## Development

```shell
make                    # sync deps (if required), build images, then start services in background
make docker_up          # update images then run services and follow logs
make docker_up_detached # update images then run services ins background
make docker_down        # stop all services
make docker_logs        # follow logs of running services
```


## Production

### Docker

Run a centos 8 docker container with the api exposed at the 8080 port.


```shell
make docker_prod
# or
DOCKER_BUILDKIT=1 docker build . -f docker/build.Dockerfile -t "linc/base"
docker build . -f docker/prod.Dockerfile -t <image_name>[:<image_tag>]
docker run -d -it -p <host_port>:8080 <image_name>[:<image_tag>]
```


This will create two images linc:base which correspond to the build stage and the final one, you can name as you need.
Then we launch the container creation and links the 8080 port to the wanted host port. This is the access port to the api.


### Complete installation

#### Ort


Ort is the main tool used by Lincompliance to find dependancies, licences and download sources.
You can refer to their documentation to install locally.


#### Libraries


```shell
cd libs
pip3 install build
python3 -m build --sdist --wheel
pip3 install dist/linapi-*.whl
# or
cd libs
python3 -m setup install
```


#### Api


The 8080 port must be available.


```shell
cd api
python3 app.py
```


## Development


```shell
DOCKER_BUILDKIT=1 docker build . -f docker/build.Dockerfile -t "linc/base"
docker build . -f docker/dev.Dockerfile -t <image_name>[:<image_tag>]
docker run -d -it -p <host_port>:8080 \
                  -v `pwd`/libs:/root/libs  \
                  -v `pwd`/api/app.py:/root/api/app.py  \
                  -v `pwd`/api/templates:/root/api/templates  \
                  <image_name>[:<image_tag>]  
```
