import subprocess
import os
from gitsub.utils import sub_output

def _run(path, cmd, opt=[], args=[],
         check=True,
         universal_newlines=True,
         stdout=subprocess.PIPE,
         stderr=subprocess.DEVNULL,
        ):
    git_cmd = cmd + opt + args
    sh_cmd = ["git", "-C", path] + git_cmd
    return subprocess.run(sh_cmd,
                          check=check,
                          stdout=stdout,
                          stderr=stderr,
                          universal_newlines=universal_newlines
                         )

def branch_local_head(path, branch):
    return _rev_parse(path,branch+"@{0}")

def branch_remote_head(path, branch):
    return _rev_parse(path,branch+"@{u}")

def branch_merge_base(path, branch):
    cmd = ["merge-base", branch+"@{0}", branch+"@{u}"]
    try:
        return sub_output(_run(path, cmd))
    except subprocess.CalledProcessError as ex:
        return None

def _rev_parse(path, interval):
    cmd = ["rev-parse", interval]
    try:
        return sub_output(_run(path, cmd))
    except subprocess.CalledProcessError as ex:
        return []

def get_commits(path, args):
    cmd = ["rev-list"]
    opt = ["--max-count=3", "--oneline"]
    try:
        return sub_output(_run(path, cmd, opt, args)).splitlines()
    except subprocess.CalledProcessError as ex:
        return []

def get_branch(path):
    cmd = ["symbolic-ref", "HEAD"]
    refs_prefix = "refs/heads/"
    try:
        ref = sub_output(_run(path, cmd))
        if ref.startswith(refs_prefix):
            return ref[len(refs_prefix):]
        else:
            return None
    except subprocess.CalledProcessError as ex:
        return None

def get_branches(path):
    try:
        cmd = ["for-each-ref"]
        opt = ["--format=%(refname:short)"]
        args = ["refs/heads/"]
        return sub_output(_run(path, cmd, opt, args)).split("\n")
    except subprocess.CalledProcessError as ex:
        return []

def is_git(path):
    if os.path.isabs(path):
        try:
            p = _run(path, ["status"])
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        return False

def update_remotes(path):
    try:
        p = _run(path, ["remote", "update"], stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
