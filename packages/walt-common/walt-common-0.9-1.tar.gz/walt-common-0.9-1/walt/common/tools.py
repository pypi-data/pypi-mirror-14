import subprocess, os, json, re
from plumbum.cmd import cat
from collections import OrderedDict

DEVNULL = open(os.devnull, 'w')

def eval_cmd(cmd):
    return cmd()

def get_mac_address(interface):
    return eval_cmd(cat["/sys/class/net/" + interface + "/address"]).strip()

def do(cmd):
    return subprocess.call(cmd, stdout=DEVNULL, shell=True)

def succeeds(cmd):
    return do(cmd) == 0

def failsafe_makedirs(path):
    # create only if missing
    if not os.path.exists(path):
        os.makedirs(path)

def failsafe_symlink(src, dst):
    # remove existing symlink if any
    if os.path.lexists(dst):
        os.remove(dst)
    # ensure parent dir of dst exists
    failsafe_makedirs(os.path.dirname(dst))
    # create the symlink
    os.symlink(src, dst)

def failsafe_mkfifo(path):
    # check if it does not exist already
    if os.path.exists(path):
        return
    # ensure parent dir exists
    failsafe_makedirs(os.path.dirname(path))
    # create the fifo
    os.mkfifo(path)

# Note: json comments are not allowed in the standard
# and thus not handled in the json python module.
# We handle them manually.
def read_json(file_path):
    content = None
    try:
        with open(file_path) as f:
            # filter out comments
            filtered = re.sub('#.*', '', f.read())
            # read valid json
            content = json.loads(filtered, object_pairs_hook=OrderedDict)
    except:
        pass
    return content
