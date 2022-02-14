FROM linc/base

ARG LIN_WORKDIR=/root

ENV LIN_LOGSDIR=/var/log/linapi
ENV LIN_TMPDIR=/tmp/linapi
ENV LIN_WORKSPACE=$LIN_WORKDIR/project
ENV LIN_CONFDIR=$LIN_WORKDIR/libs/conf

## -- Install all python development deps and all python tested versions
RUN yum install -y python3-devel libffi-devel pcre pcre-devel
COPY --chmod=711 scripts/python_install.sh .
RUN ./python_install.sh 3.7.11 3.8.11 3.9.8 \
    && rm python_install.sh

ENV LIN_SRCDIR=$LIN_WORKDIR/libs

RUN mkdir $LIN_LOGSDIR $LIN_TMPDIR

WORKDIR $LIN_WORKDIR/libs
ADD . .

RUN pip3 install --upgrade \
	'pip==21.3.1' \
	'wheel==0.37.1'
RUN pip3 install --upgrade \
	'setuptools==59.6.0' \
	'tox==3.24.5' \
	'pytest==6.2.5' \
	'uwsgi==2.0.20'
RUN python3 -m setup develop

EXPOSE 80
ENTRYPOINT uwsgi --ini $LIN_SRCDIR/uwsgi.ini
