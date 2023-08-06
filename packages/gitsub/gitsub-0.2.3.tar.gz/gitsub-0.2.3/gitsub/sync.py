from gitsub.repo import RepoFactory, RepoCache
from gitsub.env import Environment

def handler(args, env):
    repo_cache = RepoCache(env.cache_dir)
    repo_cache.load()
    for repo in repo_cache:
        print('Syncing {}'.format(repo.name))
        repo.sync()
    print("Repositories synced")


