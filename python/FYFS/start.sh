#!/usr/bin/env bash


mkdir -p /var/run/ldfs
mkdir -p /opt/log/ldfs
mkdir -p /opt/data/ldfs



uwsgi3 -i ./uwsgi.ini

cd - >/dev/null 2>&1
