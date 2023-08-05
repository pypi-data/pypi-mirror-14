def handler(args, env):
    paths = args
    repolist = env.cache["repolist"]
    for path in repolist:
        print(path)
