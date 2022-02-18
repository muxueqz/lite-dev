#!/bin/sh
echo Reloading Docker compose
# podman_compose.py down -t 1
# podman_compose.py down -t 1
sleep 0.5s
$@
if [[ $? == 0 ]]; then
  podman_compose.py restart
  echo "my exit:" $?
  # flock --unlock ${lock_file} echo
  # flock --close ${lock_file} podman_compose.py logs -f &
  rm -rfv ${lock_file}
  podman_compose.py logs -f &
  # podman_compose.py up &
fi
