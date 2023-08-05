def show(repos):
    for repo in repos:
        print("'{}' repository updates".format(repo['name']))
        for commit in repo['commits']:
            print("\t"+commit)

