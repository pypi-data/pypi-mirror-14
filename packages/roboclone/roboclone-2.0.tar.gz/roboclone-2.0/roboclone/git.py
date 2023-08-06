from git.repo.base import Repo
from git.remote import RemoteProgress
import math
import sys


class ProgressPrinter(RemoteProgress):
    prev_pos = 0

    def update(self, op_code, cur_count, max_count=None, message=''):
        percent = math.floor(cur_count / (max_count or 100.0) * 100)
        if percent <= 100:
            sys.stdout.write("\r%d" % percent)
            sys.stdout.flush()


def clone(uri, path):
    return Repo.clone_from(uri, path, progress=ProgressPrinter())