import re
from argparse import ArgumentParser
from datetime import datetime
from logging import getLogger
from os import getcwd
from os.path import basename, join

from dateutil.relativedelta import relativedelta

from kunitori.aggregator import aggregate_author_count
from kunitori.revision_searcher import search_revision
from kunitori.visualizer import visualize

logger = getLogger(__name__)


def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument('git_directory_path')
    argument_parser.add_argument('-i', '--revision_interval', default=12, type=int)

    args = argument_parser.parse_args()

    git_directory_path = args.git_directory_path
    filters = [re.compile(r"\.py$"), re.compile(r"\.(ts|vue)$")]
    base_date = datetime.now()
    revision_interval = args.revision_interval

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
