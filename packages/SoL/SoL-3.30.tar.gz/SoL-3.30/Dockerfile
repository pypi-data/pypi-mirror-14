# -*- coding: utf-8 -*-
# :Project:   SoL -- Dockerization setup
# :Created:   mer 30 mar 2016 21:08:50 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

# Start from a minimalistic Python image: the standard one is almost twice as big because it
# contains lots of useless stuff (even MySQL, wtf!)
FROM python:3.5-slim

MAINTAINER Lele Gaifax <lele@metapensiero.it>

# Install a minimal set of development libraries, needed for Pillow and YAML
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    apt-get autoremove -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
       fonts-dejavu \
       gcc \
       libc-dev \
       libjpeg-dev \
       libpng12-dev \
       libxml2-dev \
       libxslt1-dev \
       libyaml-dev \
       zlib1g-dev \
       && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

WORKDIR /tmp
COPY requirements/base.txt /tmp/requirements.txt
RUN pip install --no-cache -r requirements.txt
RUN pip install --no-cache SoL
RUN python3 -m metapensiero.extjs.desktop --no-cache
RUN rm -f /tmp/requirements.txt

WORKDIR /srv
RUN mkdir /srv/data /srv/data/backups /srv/data/emblems /srv/data/portraits

RUN soladmin create-config --password admin --data-dir /srv/data config.ini
RUN soladmin initialize-db config.ini
RUN soladmin restore config.ini

EXPOSE 6996
VOLUME /srv/data

COPY docker-entrypoint.sh /srv/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["start"]
