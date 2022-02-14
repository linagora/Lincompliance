# File              : Makefile
# License           : AGPL-3.0-or-later
# Author            : Pierre Marty <pmarty@linagora.com>
# Date              : 2022.01.19
# Last Modified Date: 2022.02.02
# Last Modified By  : Pierre Marty <pmarty@linagora.com>

SHELL = /bin/sh
MAKE = make -s

all: modules docker

# ====[ Git Submodules ]====
modules:
	@if git submodule status | egrep -q '^[-]|^[+]' ; then \
		$(MAKE) modules_sync; \
	fi

modules_sync:
	@echo "INFO: updating git submodules"
	@git submodule sync --recursive
	@git submodule update --init --recursive

# ====[ Docker ]====
docker: docker_up_detached

docker_up: ort_docker_build
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up --build

docker_up_detached: ort_docker_build
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up -d --build

docker_down:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose down

docker_logs:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose logs --follow

# ====[ Docker ORT ]====
ort_docker_build:
	@echo "INFO: building ort image..."
	@DOCKER_BUILDKIT=1 docker build . -f ort-builder.Dockerfile -t "linc/base"
	@echo "INFO: ort build done!"

.PHONY: all modules modules_sync docker docker_up docker_up_detached docker_down ort_docker_build
