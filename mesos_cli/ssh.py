
import copy
import os
import platform
import sys

from . import cli
from .master import current as master
from . import log
from . import slave
from . import task

parser = cli.parser(
    description="SSH into the sandbox of a specific task"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task."""
)

def main():
    # There's a security bug in Mavericks wrt. urllib2:
    #     http://bugs.python.org/issue20585
    if platform.system() == "Darwin":
        os.environ["no_proxy"] = "*"

    cfg, args = cli.init(parser)

    t = master.task(args.task)
    cmd = [
        "ssh",
        "-t",
        t.slave.hostname,
        "cd {} && bash".format(t.directory)
    ]
    log.fn(os.execvp, "ssh", cmd)
