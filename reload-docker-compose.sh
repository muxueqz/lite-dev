#!/bin/sh
echo reload docker compose
podman_compose.py down
podman_compose.py down
podman_compose.py up &
