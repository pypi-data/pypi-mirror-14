from gitsub.repo import RepoFactory
from gitsub.env import Environment

def handler(args, env):
    repolist = env.cache["repolist"]
    repos = [RepoFactory.new(path) for path in repolist]
    for repo in repos:
        repo.sync()
    print("repositories synced")


