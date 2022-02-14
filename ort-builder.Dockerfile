# ==[ Lincompliance ]==
#
# Dockerfie
#   Build ORT binary &
#   Create a docker image to run
#
# Authors:
#   - Claire Bouttes
#   - Pierre Marty
#



# ====[ ORT build container ]====
FROM adoptopenjdk/openjdk11:alpine-slim AS build

# ==[ Building Variables ]==
ARG ORT_VERSION="Lincompliance-integrated"

# ==[ Install Directories ]==
ARG INST_PREFIX=/usr/local
ARG SRC_PREFIX=/src
ARG BIN_PREFIX=/bin

ARG INST_ORT_SRC=$INST_PREFIX$SRC_PREFIX/oss-review-toolkit/ort

# ==[ System Configuration ]==
RUN apk add --no-cache libstdc++ ca-certificates coreutils openssl nodejs yarn

# ==[ Getting Sources ]==
WORKDIR $INST_ORT_SRC
COPY ./ort $INST_ORT_SRC

# ==[ Building ORT ]==
RUN --mount=type=cache,target=/tmp/.gradle/ \
    GRADLE_USER_HOME=/tmp/.gradle/ && \
    scripts/import_proxy_certs.sh && \
    scripts/set_gradle_proxy.sh && \
    sed -i -r 's,(^distributionUrl=)(.+)-all\.zip$,\1\2-bin.zip,' gradle/wrapper/gradle-wrapper.properties && \
    ./gradlew --no-daemon --stacktrace -Pversion=$ORT_VERSION :cli:distTar :helper-cli:startScripts



# ====[ ORT basic running container ]====
FROM centos:8

# ==[ Install Directories ]==
ARG INST_PREFIX=/usr/local
ARG SRC_PREFIX=/src
ARG BIN_PREFIX=/bin

ENV GOPATH=$INST_PREFIX$SRC_PREFIX/go
ENV GOBIN=$GOPATH/bin

ARG INST_COMPOSER_SRC=$INST_PREFIX$SRC_PREFIX/php/composer
ARG INST_DART_SRC=$INST_PREFIX$SRC_PREFIX/google/dart
ARG INST_GIT_SRC=$INST_PREFIX$SRC_PREFIX/git
ARG INST_GODEP_SRC=$GOPATH/src/dep
ARG INST_ORT_SRC=$INST_PREFIX$SRC_PREFIX/oss-review-toolkit/ort
ARG INST_REPO_SRC=$INST_PREFIX$SRC_PREFIX/google/repo
ARG INST_STACK_SRC=$INST_PREFIX$SRC_PREFIX/haskell/stack
ARG INST_SCANCODE_SRC=$INST_PREFIX$SRC_PREFIX/nexB/scancode
ARG INST_ASKALONO_SRC=$INST_PREFIX$SRC_PREFIX/jpeddicord/askalono
ARG INST_BOYTERLC_SRC=$INST_PREFIX$SRC_PREFIX/boyter/lc

ARG INST_COMPOSER_BIN=$INST_PREFIX$BIN_PREFIX/composer
ARG INST_GIT_BIN=$INST_PREFIX
ARG INST_GODEP_BIN=$INST_PREFIX$BIN_PREFIX/dep
ARG INST_ORT_BIN=$INST_PREFIX$BIN_PREFIX/ort
ARG INST_REPO_BIN=$INST_PREFIX$BIN_PREFIX/repo
ARG INST_STACK_BIN=$INST_PREFIX$BIN_PREFIX/stack
ARG INST_SCANCODE_BIN=$INST_PREFIX$BIN_PREFIX/scancode
ARG INST_ASKALONO_BIN=$INST_PREFIX$BIN_PREFIX/askalono
ARG INST_BOYTERLC_BIN=$INST_PREFIX$BIN_PREFIX/lc

# ==[ Dependencies Version ]==
ARG VERSION_RUBY=2.7
ARG VERSION_NPM=7.20.5
ARG VERSION_YARN=1.22.0
ARG VERSION_GIT=2.29.0
ARG VERSION_SCANCODE=3.2.1rc2
ARG VERSION_LICENSEE=9.13.0
ARG VERSION_ASKALONO=0.4.3
ARG VERSION_BOYTERLC=1.3.1

# ==[ System Configuration ]==
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Linux-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-Linux-*

RUN curl -L https://www.scala-sbt.org/sbt-rpm.repo > /etc/yum.repos.d/sbt-rpm.repo
RUN yum install -y epel-release
RUN yum module reset -y ruby
RUN yum module enable -y ruby:$VERSION_RUBY
RUN yum install -y cargo curl curl-devel cvs expat-devel gcc gettext-devel golang java-11-openjdk-headless make mercurial nodejs openssl-devel perl-ExtUtils-MakeMaker php-cli php-json php-zip python3 python3-flask python3-pip python3-virtualenv ruby ruby-devel sbt unzip wget which zlib-devel python36-devel zlib bzip2-libs xz-libs libxml2-devel libxslt-devel lbzip2 cmake

# ==[ Enabling Tools Detection ]==
RUN ln -s "$(which python3)" "$(dirname $(which python3))/python"
RUN ln -s "$(which pip3)" "$(dirname $(which pip3))/pip"

# ==[ Installing Third Party Dependencies ]==
RUN npm install -g bower npm@$VERSION_NPM yarn@$VERSION_YARN
RUN pip install conan pipenv
RUN gem install bundler cocoapods licensee:$VERSION_LICENSEE

# ==[ Installing Unpackaged Dependencies ]==
WORKDIR $INST_GIT_SRC
RUN wget -c https://mirrors.edge.kernel.org/pub/software/scm/git/git-$VERSION_GIT.tar.gz
RUN tar -xzvf git-$VERSION_GIT.tar.gz
WORKDIR ./git-$VERSION_GIT
# RUN make prefix=$INST_GIT_SRC all
RUN make prefix=$INST_GIT_BIN install

WORKDIR $INST_REPO_SRC
RUN wget -c https://storage.googleapis.com/git-repo-downloads/repo
RUN chmod a+rx ./repo
RUN ln -s "$(readlink -f ./repo)" $INST_REPO_BIN

WORKDIR $INST_COMPOSER_SRC
RUN curl https://getcomposer.org/installer | php
RUN ln -s "$(readlink -f ./composer.phar)" $INST_COMPOSER_BIN

WORKDIR $INST_STACK_SRC
RUN wget -c https://www.stackage.org/stack/linux-x86_64
RUN tar -xvf ./linux-x86_64
RUN ln -s "$(readlink -f ./stack-*/stack)" $INST_STACK_BIN

WORKDIR $INST_GODEP_SRC
RUN mkdir -p $GOBIN
RUN curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh
RUN ln -s "$(readlink -f $GOBIN/dep)" $INST_GODEP_BIN

WORKDIR $INST_DART_SRC
RUN wget -c https://storage.googleapis.com/dart-archive/channels/be/raw/latest/sdk/dartsdk-linux-x64-release.zip
RUN unzip ./dartsdk-linux-x64-release.zip
RUN find ./dart-sdk/bin/ -maxdepth 1 -type f | while read file; do ln -s "$(readlink -f $file)" "/usr/local/bin/$(basename $file)" -f ; done
RUN find ./dart-sdk/include/ -maxdepth 1 -type f | while read file; do ln -s "$(readlink -f $file)" "/usr/local/include/$(basename $file)" -f ; done
RUN find ./dart-sdk/lib/ -maxdepth 1 -type f | while read file; do ln -s "$(readlink -f $file)" "/usr/local/lib/$(basename $file)" -f ; done

# ==[ Scancode Installation ]==
WORKDIR $INST_SCANCODE_SRC
RUN wget -c https://github.com/nexB/scancode-toolkit/releases/download/v$VERSION_SCANCODE/scancode-toolkit-$VERSION_SCANCODE.tar.bz2
RUN tar -xvf scancode-toolkit-$VERSION_SCANCODE.tar.bz2
RUN ln -s "$(readlink -f scancode-toolkit-$VERSION_SCANCODE/scancode)" $INST_SCANCODE_BIN
RUN scancode --version

# ==[ Askalono installation ]==
WORKDIR $INST_ASKALONO_SRC
RUN wget -c https://github.com/jpeddicord/askalono/releases/download/$VERSION_ASKALONO/askalono-Linux.zip
RUN unzip askalono-Linux.zip
RUN ln -s "$(readlink -f askalono)" $INST_ASKALONO_BIN

# ==[ BoyterLC installation ]==
WORKDIR $INST_BOYTERLC_SRC
RUN wget -c https://github.com/boyter/lc/releases/download/v$VERSION_BOYTERLC/lc-$VERSION_BOYTERLC-x86_64-unknown-linux.zip
RUN unzip lc-$VERSION_BOYTERLC-x86_64-unknown-linux.zip
RUN ln -s "$(readlink -f lc)" $INST_BOYTERLC_BIN



# ====[ OSS Review Toolkit binary ]====
WORKDIR $INST_ORT_SRC
COPY --from=build $INST_ORT_SRC/cli/build/distributions/ort-*.tar ./ort.tar

RUN tar -vxf ./ort.tar -C $INST_ORT_SRC --strip-components 1
RUN rm ./ort.tar
RUN ln -s "$(readlink -f ./bin/ort)" $INST_ORT_BIN

WORKDIR /root
