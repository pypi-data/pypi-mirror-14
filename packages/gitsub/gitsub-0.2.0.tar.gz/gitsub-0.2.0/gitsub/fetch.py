from gitsub.display import show
from gitsub.repo import RepoFactory
from gitsub.env import Environment

def handler(args, env):
    repolist = env.cache["repolist"]
    repos = [RepoFactory.new(path) for path in repolist]
    updates = [repo.query(["name", "commits"]) for repo in repos ]
    show(updates)

