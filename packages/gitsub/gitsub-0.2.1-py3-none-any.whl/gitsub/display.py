def show(repos):
    for repo in repos:
        print("'{}' repository updates".format(repo['name']))
        updates = repo['commits']
        if updates != None:
            for update in updates:
                print("\t"+update)

