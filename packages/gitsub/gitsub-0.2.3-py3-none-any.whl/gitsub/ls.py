from gitsub.repo import RepoCache

def handler(args, env):
    repo_cache = RepoCache(directory=env.cache_dir)
    repo_cache.load()
    for repo in repo_cache:
        print('{} at {}'.format(repo.name, repo.path))
