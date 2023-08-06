#! /usr/bin/env python3
""" usage: repo-sync CONFIG

Creates a sync repo in PWD.

Environment:
    REPONAME    name of the sync repo in workdir (Default: repo-sync.git)

Configuration:
    Sync configuration in json format,defines which branch of
    "origin.url" will be mirrored to "mirror.url"

    $name.origin.ref defaults to "heads/master"
    $name.mirror.ref defaults to "heads/${name}"

    A special "@latest" entry defines where the ref with the latest
    update is pushed to the mirror-url.
    @latest.mirror.ref defaults to "heads/master"

Literal example for config file:
{
    "$username-repo": {
        "origin": {
            "url": "http://github.com/username/repo"
            "ref": "heads/dev"
        },
        "mirror": {
            "url": "git@internal:mirror-repo",
            "ref": "heads/github-mirror-dev"
        }
    },
    ...
    "@latest": {
        "mirror": {
            "url": "git@internal:mirror",
            "ref": "heads/master"
        }
    }
}

"""
from git import Repo
import git
from docopt import docopt
import logging
import os
from datetime import datetime
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("repo-sync")

def load_config(fname):
    import json
    with open(fname) as f:
        return json.load(f)

def sync_ref(repo,k,v):
    log.info("begin sync of {}".format(k))
    oname = k
    mname = oname+'-mirror'
    ourl = v['origin']['url']
    murl = v['mirror']['url']

    # it is easier to ask for forgiveness than to ask for permission
    try: repo.delete_remote(oname)
    except git.exc.GitCommandError: pass
    try: repo.delete_remote(mname)
    except git.exc.GitCommandError: pass

    # Step 1: fetch remote_ref:local_ref
    # Step 2: push local_ref:mirror_ref
    remote_ref = "refs/" + v['origin']['ref'] if 'ref' in v['origin'] \
            else 'refs/heads/master'
    local_ref = "refs/remotes/{}/master".format(oname)
    refspec = "+{}:{}".format(remote_ref,local_ref)
    oremote = repo.create_remote(oname,url=ourl)
    log.info("fetching refspec {}".format(refspec))
    fetch = oremote.fetch(refspec=refspec)[0]
    print("{} - {}".format(fetch.commit.summary,datetime.fromtimestamp(fetch.commit.committed_date)))

    mremote = repo.create_remote(mname,murl)

    mirror_ref = "refs/" + v['mirror']['ref'] if 'ref' in v['mirror'] \
            else "refs/heads/{}".format(oname)

    mrefspec = "{}:{}".format(local_ref,mirror_ref)
    log.info("pushing refspec {}".format(mrefspec))
    mremote.push(refspec=mrefspec,force=True)
    return { "mirror_ref": mirror_ref,
             "remote_ref": remote_ref,
             "local_ref": local_ref,
             "remote": oremote }


def push_latest(repo,k,v,local_ref):
    """ push the `local_ref` to `v['mirror']['url']`
        `k` is the remote name

        essentially the second half of sync_ref
    """
    try: repo.delete_remote(k)
    except git.exc.GitCommandError: pass
    remote = repo.create_remote(k,url=v['mirror']['url'])

    mirror_ref = "refs/" + v['mirror']['ref'] if 'ref' in v['mirror'] \
            else "refs/heads/master"

    mrefspec = "{}:{}".format(local_ref,mirror_ref)
    log.info("pushing refspec {}".format(mrefspec))
    remote.push(refspec=mrefspec,force=True)


def get_latest_change(repo,sync):
    """ takes { "name" : { "local_ref": "refs/remotes/name/master" },
                "name2": { "local_ref": "..." } }
        returns "refs/remotes/name/master" of the entry with the latest change
    """
    last_change = sorted(sync,key=lambda k:
            git.objects.base.Object.new(repo,sync[k]['local_ref']).committed_date).pop()
    log.info("latest change seen in: {}".format(last_change))
    return sync[last_change]['local_ref']


def mirror(reponame,cfg):
    from os.path import join
    log.info("init repo at {}".format(join(os.curdir,reponame)))
    repo = Repo.init(reponame,bare=True)
    sync = {}
    lk = '@latest'
    for k,v in cfg.items():
        if k == lk: continue
        try:
            sync[k] = sync_ref(repo,k,v)
        except Exception as e:
            log.error("failed to sync repo {}".format(k))

    if lk in cfg:
        log.info("found `latest` entry, starting push")
        push_latest(repo,lk,cfg[lk],get_latest_change(repo,sync))
    else:
        log.debug("no `@latest` entry.")

    log.info("finish sync")


def main():
    args = docopt(__doc__)
    name = os.environ.get("REPONAME","repo-sync.git")
    mirror(name,load_config(args['CONFIG']))


if __name__ == "__main__":
    main()
