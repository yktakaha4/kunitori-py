from datetime import datetime
from logging import getLogger

import git

now = datetime.now()
logger = getLogger(__name__)


def search_revision(
    git_directory_path: str,
    target: datetime,
):
    logger.info(f"{git_directory_path=}, {target=}")
    repo = git.Repo(path=git_directory_path)
    before = target.strftime("%Y.%m.%d")
    revision = repo.git.log("-1", "--format=%h", f"--before={before}")
    return revision
