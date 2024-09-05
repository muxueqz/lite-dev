#!/bin/sh
echo Reloading Docker compose
if [ -z ${COMPOSE_FILE} ]; then
  COMPOSE_FILE='docker-compose.yml'
fi
COMPOSE_CMD="podman_compose.py -f ${COMPOSE_FILE}"
echo ${COMPOSE_CMD}
# podman_compose.py down -t 1
# podman_compose.py down -t 1
sleep 0.5s
$@
if [[ $? == 0 ]]; then
  # podman_compose.py -f ${COMPOSE_FILE} restart
  ${COMPOSE_CMD} restart -t 0
  echo "my exit:" $?
  # flock --unlock ${lock_file} echo
  # flock --close ${lock_file} podman_compose.py logs -f &
  rm -rfv ${lock_file}
  ${COMPOSE_CMD} logs -f &
  # podman_compose.py up &
fi
