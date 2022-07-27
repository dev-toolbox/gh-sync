from github import Github
from git import Repo
import os
import logging

base_path = "/Volumes/Daten/Projekte/Webs"
logging.basicConfig(level=logging.INFO)


def create_dir(org):
    path = f"{base_path}/{org}"
    exists = os.path.exists(path)
    if not exists:
        logging.info(f"creating path {path}")
        os.makedirs(path)


def get_projects(org, repository):
    path = f"{base_path}/{org}/{repository.name}"
    exists = os.path.exists(path)
    if not exists:
        logging.info(f"cloning repo  {path}")
        Repo.clone_from(repository.clone_url, path)
    else:
        existing_repo = Repo(path)
        if not existing_repo.bare:
            remote_origin = existing_repo.remotes.origin
            if len(existing_repo.refs) > 0:
                logging.info(f"updating repo  {path}")
                remote_origin.pull()


g = Github(login_or_token=os.getenv('GITHUB_TOKEN'))
# Then play with your GitHub objects:
for repo in g.get_user().get_repos():
    if repo.organization is not None:
        logging.info(f"{repo.organization.login}/{repo.name}")
        create_dir(repo.organization.login)
        get_projects(repo.organization.login, repo)
    else:
        logging.info(f"{g.get_user().login}/{repo.name}")
        create_dir(g.get_user().login)
        get_projects(g.get_user().login, repo)
