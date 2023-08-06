import os
import gitsub.git as git
from gitsub.cache import Cache

class RepoFactory:
    @staticmethod
    def from_paths(repo_paths):
        raw_repos = [RepoFactory.new(path) for path in repo_paths]
        return [repo for repo in raw_repos if repo != None]

    @staticmethod
    def new(path):
        try:
            return Repo(path)
        except NotRepositoryException as ex:
            return None

class NotRepositoryException(Exception):
    pass

class RepoCache(Cache):
    """ Repository list cache object

    RepoCache object implemented as iterable Cache object
    containing repositories object.

    On initiation, RepoCache isn't loaded yet. This is to
    make sure the cache loaded ONLY on demand.

    """
    def __init__(self, directory=Cache.DEFAULT_CACHE_DIR):
        super().__init__("repolist", directory)
        self.container = []

    def __iter__(self):
        return iter(self.container)

    def add(self, item):
        """ Add item to cache container """
        self.container.append(item)

    def save(self):
        repo_paths = [repo.path for repo in self.container]
        self.content = "\n".join(repo_paths)
        super().save()

    def load(self):
        super().load()
        repo_paths = self.content.split('\n')
        self.container = RepoFactory.from_paths(repo_paths)

class Repo:
    def __init__(self, path):
        if not git.is_git(path):
            err_msg = "Not a git repository: {}".format(path)
            raise NotRepositoryException(err_msg)

        self.path = os.path.normpath(path)
        self.name = os.path.basename(self.path)
        self.branches = git.get_branches(self.path)
        self.cur_branch = git.get_branch(self.path)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and 
                self.path == other.path)

    def __ne__(self, other):
        return not self == other


    def query(self, queries):
        return {query:self.handle_query(query) for query in queries}

    def handle_query(self, query):
        if query == "name":
            return self.name
        if query == "commits":
            return self.get_updates()

    def sync(self):
        p = git.update_remotes(self.path)
        return p != None

    def get_updates(self):
        for branch in self.branches:
            local = git.branch_local_head(self.path, branch)
            remote = git.branch_remote_head(self.path, branch)
            base = git.branch_merge_base(self.path, branch)
            if base == None:
                print("branch {} on {} does not have commit tree or remote"
                      .format(branch, self.name))
            else:
                if local == remote:
                    return None
                elif local == base:
                    # remote is up-to-date
                    commits = git.get_commits(self.path, ["^" + base,remote])
                    return commits
                elif remote == base:
                    # local is up-to-date
                    commits = git.get_commits(self.path, ["^" + base,local])
                    return commits
                else:
                    new_commits = git.get_commits(self.path, ["^" + base,local])
                    new_updates = git.get_commits(self.path, ["^" + base,remote])
                    return new_commits + new_updates
