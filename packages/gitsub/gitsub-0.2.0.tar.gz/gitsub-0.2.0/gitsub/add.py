import os
from gitsub.git import is_git

def handler(args, env):
    paths = args
    repolist = env.cache["repolist"]
    for path in paths:
        new_repos = traverse(os.path.abspath(path))
        for new_path in new_repos:
            if not new_path in repolist:
                repolist.append(new_path)
    env.cache.write()

def traverse(path):
    if is_git(path):
        return [path]
    else:
        new_repos = []
        dirents = os.scandir(path)
        for entry in dirents:
            if entry.is_dir():
                new_repos += traverse(entry.path)
        return new_repos
