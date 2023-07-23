#!/bin/bash
PHASE=$1
function build()
{
  # flask app
  #rm -rf docker/python/apps
  #cp apps/ -R docker/python/apps/

  docker-compose up -d --build
}

if [ ${PHASE} == "QA" ]
then
    build
elif [ ${PHASE} == "LOCAL" ]
then
    build

elif [ ${PHASE} == "RELEASE" ]
then
    build
    #docker-compose rm -f -s -v mysql
else
    echo "[ERROR] Usage : docker-build.sh [ QA | RELEASE ]"
fi
