import re
from datetime import datetime
from logging import getLogger
from os import environ, getcwd
from os.path import basename, join

from dateutil.relativedelta import relativedelta

from kunitori.aggregator import aggregate_author_count
from kunitori.revision_searcher import search_revision
from kunitori.visualizer import visualize

logger = getLogger(__name__)


def main():
    git_directory_path = environ["GIT_DIRECTORY_PATH"]
    filters = [re.compile(r"\.py$"), re.compile(r"\.(ts|vue)$")]
    base_date = datetime.now()
    revision_interval = 12

    logger.info(
        f"{git_directory_path=}, {filters=}, {base_date=}, {revision_interval=}"
    )

    revisions = [
        search_revision(
            git_directory_path=git_directory_path,
            target=(base_date - relativedelta(months=before_month)),
        )
        for before_month in range(revision_interval)
    ]

    export_directory_path = join(getcwd(), "out")
    name = basename(git_directory_path)
    data = [
        (
            revision,
            aggregate_author_count(
                git_directory_path=git_directory_path,
                filters=filters,
                revision=revision,
            ),
        )
        for revision in revisions
    ]

    visualize(export_directory_path=export_directory_path, name=name, data=data)
    logger.info("done.")


if __name__ == "__main__":
    main()
