#!/usr/bin/env bash

for version in "$@"
do
    cd /usr/src || return

    echo "Install python version $version start."

    wget https://www.python.org/ftp/python/"$version"/Python-"$version".tgz
    tar xzf Python-"$version".tgz

    cd Python-"$version" || continue
    ./configure --enable-optimizations
    make altinstall

    echo "Python$version installed."
done

rm -f /usr/src/Python-*.tgz
