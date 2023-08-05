import subprocess
from .utils import sub_output

def run(path, cmd, opt=[], args=[],
        check=True, universal_newlines=True):
    git_cmd = cmd + opt + args
    sh_cmd = ["git", "-C", path] + git_cmd
    try:
        return subprocess.run(sh_cmd, stdout=subprocess.PIPE, 
                check=check, universal_newlines=universal_newlines)
    except subprocess.CalledProcessError as ex:
        return None

def branch_local_head(path, branch):
    cmd = ["rev-parse", branch+"@{0}"]
    return sub_output(run(path, cmd))

def branch_remote_head(path, branch):
    cmd = ["rev-parse", branch+"@{u}"]
    return sub_output(run(path, cmd))

def branch_merge_base(path, branch):
    cmd = ["merge-base", branch+"@{0}", branch+"@{u}"]
    return sub_output(run(path, cmd))

def get_commits(path, args):
    cmd = ["rev-list"]
    opt = ["--max-count=3", "--oneline"]
    return sub_output(run(path, cmd, opt, args)).split("\n")

def get_branch(path):
    cmd = ["symbolic-ref", "HEAD"]
    refs_prefix = "refs/heads"
    ref = sub_output(run(path, cmd))
    if ref.startswith(refs_prefix):
        return ref[len(ref):]
    else:
        return None

def get_branches(path):
    cmd = ["for-each-ref"]
    opt = ["--format=%(refname:short)"]
    args = ["refs/heads/"]
    return sub_output(run(path, cmd, opt, args)).split("\n")
