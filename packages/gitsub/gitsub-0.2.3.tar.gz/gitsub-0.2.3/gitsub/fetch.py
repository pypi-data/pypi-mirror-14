from gitsub.display import show
from gitsub.repo import RepoFactory, RepoCache
from gitsub.env import Environment

def handler(args, env):
    repo_cache = RepoCache(env.cache_dir)
    repo_cache.load()
    updates = [repo.query(["name", "commits"]) for repo in repo_cache]
    show(updates)

