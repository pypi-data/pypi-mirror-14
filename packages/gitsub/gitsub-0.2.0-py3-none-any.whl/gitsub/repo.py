import os
import gitsub.git as git

class RepoFactory:
    @staticmethod
    def new(path):
        if (git.is_git(path)):
            return Repo(path)
        else:
            return None

class Repo:
    def __init__(self, path):
        self.path = os.path.normpath(path)
        self.name = os.path.basename(self.path)
        self.branches = git.get_branches(self.path)
        self.cur_branch = git.get_branch(self.path)


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
