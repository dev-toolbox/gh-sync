from github import Github
from git import Repo
import os
import logging

base_path = "/Volumes/Daten/Projekte/Webs"
logging.basicConfig(level=logging.INFO)


def createDirectory(org):
    path = f"{base_path}/{org}"
    exists = os.path.exists(path)
    if not exists:
        logging.info(f"creating path {path}")
        os.makedirs(path)

def get_projects(org, repo):
    path = f"{base_path}/{org}/{repo.name}"
    exists = os.path.exists(path)
    if not exists:
        logging.info(f"cloning repo  {path}")
        Repo.clone_from(repo.clone_url, path)
    else:
        r = Repo(path)
        if not r.bare:
            o = r.remotes.origin
            if len(r.refs) > 0:
                logging.info(f"updating repo  {path}")
                o.pull()

g = Github("access_token")

g = Github(login_or_token=os.getenv('GITHUB_TOKEN'))
# Then play with your Github objects:
for repo in g.get_user().get_repos():
    if repo.organization is not None:
        logging.info(f"{repo.organization.login}/{repo.name}")
        createDirectory(repo.organization.login)
        get_projects(repo.organization.login, repo)
    else:
        logging.info(f"{g.get_user().login}/{repo.name}")
        createDirectory(g.get_user().login)
        get_projects(g.get_user().login, repo)