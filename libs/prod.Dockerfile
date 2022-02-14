FROM python:alpine AS libs
WORKDIR /app
COPY . .
RUN pip3 install build
RUN python3 -m build --sdist --wheel

FROM linc/base

ENV LIN_WORKDIR=/root
ARG LIN_USER=uwsgi
ARG LIN_GROUP=uwsgi
ENV LIN_VENVDIR=$LIN_WORKDIR/venv
ENV LIN_LOGSDIR=/var/log/linapi
ENV LIN_TMPDIR=/tmp/linapi

ENV LIN_WORKSPACE=$LIN_WORKDIR/project
ENV LIN_CONFDIR=$LIN_WORKDIR/conf

WORKDIR $LIN_WORKDIR

COPY --from=libs /app/dist/linapi-*.whl .

RUN yum install -y python3-devel python3-virtualenv nginx pcre pcre-devel

COPY uwsgi.ini $LIN_WORKDIR
COPY conf $LIN_CONFDIR

RUN chmod ug=rwx,o=rx $LIN_WORKDIR                      \
    && groupadd $LIN_GROUP                              \
    && useradd $LIN_USER -g $LIN_GROUP -d $LIN_WORKDIR  \
    && chown -R $LIN_GROUP:$LIN_USER $LIN_WORKDIR       \
    && mkdir $LIN_LOGSDIR $LIN_TMPDIR                  \
    && chown -R $LIN_GROUP:$LIN_USER $LIN_LOGSDIR $LIN_TMPDIR
USER $LIN_USER:$LIN_GROUP

RUN python3 -m venv $LIN_VENVDIR  \
    && source $LIN_VENVDIR/bin/activate   \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade wheel \
    && pip3 install --upgrade setuptools uwsgi linapi-*.whl \
    && deactivate

EXPOSE 80
ENTRYPOINT $LIN_VENVDIR/bin/uwsgi --ini $LIN_WORKDIR/uwsgi.ini -H $LIN_VENVDIR