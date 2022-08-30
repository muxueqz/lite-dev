#!/usr/bin/env python
import os
import sys
import subprocess

app = sys.argv[1]
xdg_runtime_dir = os.getenv("XDG_RUNTIME_DIR")
pid_file = "%s/%s.pid" % (xdg_runtime_dir, app)
lock_file = "%s/%s.lock" % (xdg_runtime_dir, app)

app_map = {
    # "docker-compose": "/reload-docker-compose.sh",
    "docker-compose": "/reload-docker-compose-local-build.sh",
    "docker-compose-local-build": "/reload-docker-compose-local-build.sh",
}
print(sys.argv)
script_dir = os.path.dirname(os.path.realpath(__file__))
reload_script = app_map.get(app, "/reload.sh")
reload_cmd = ["bash", script_dir + reload_script]
reload_cmd.extend(sys.argv[2:])

os.environ["pid_file"] = pid_file
os.environ["lock_file"] = lock_file

print(reload_cmd)
subprocess.check_call(reload_cmd, shell=False)

REALPWD = os.path.realpath(os.path.curdir)
# fswatch -l 0.5 -r \
watch_cmd = (
    "fswatch -l 0.5 -o -r --event=Removed --event=Created --event=Updated".split(" ")
)

exclude_list = """.git/
go.sum
run.pid
minimal_devops$
postman.sh$
runtime/
bin/
apisix_log/
.*_default""".split(
    "\n"
)
try:
    with open(".devignore", "r") as _fd:
        for i in _fd:
            exclude_list.append(i.strip("\n"))
except:
    pass

for i in exclude_list:
    exclude_rule = ["--exclude", "^%s/%s" % (REALPWD, i)]
    watch_cmd.extend(exclude_rule)

watch_cmd.append(". | xargs -I[] -n1 -P10")
# watch_cmd.append(". | xargs -I[]")

# watch_cmd.append('sh -c "flock -s -n %s ' % lock_file)
watch_cmd.append("flock -n %s" % lock_file)

watch_cmd.extend(reload_cmd)
# watch_cmd.append('"')
print(watch_cmd)
# subprocess.check_call(' '.join(watch_cmd), shell=True)
os.system(" ".join(watch_cmd))
