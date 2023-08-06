import os
from gitsub.repo import RepoFactory,RepoCache

def handler(args, env):
    paths = args
    repo_cache = RepoCache(directory=env.cache_dir)
    repo_cache.load()
    for path in paths:
        dfs_root = os.path.abspath(path)
        new_repos = dfs_repo(dfs_root)
        for new_repo in new_repos:
            if not new_repo in repo_cache:
                repo_cache.add(new_repo)
    repo_cache.save()

MAX_DEPTH = 7
def dfs_repo(root, depth=0):
    """ Return list of valid Repo within MAX_DEPTH depth from root """
    if depth > MAX_DEPTH:
        return []

    repo = RepoFactory.new(root)
    if repo != None:
        return [repo]
    else:
        new_repos = []
        dirents = os.scandir(root)
        for entry in dirents:
            if entry.is_dir():
                next_root = os.path.abspath(entry.path)
                new_repos += dfs_repo(next_root, depth+1)
        return new_repos
