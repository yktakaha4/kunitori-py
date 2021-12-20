from binascii import Error
import itertools
from collections import Counter, OrderedDict
from logging import getLogger
from re import Pattern
from typing import List

import git

logger = getLogger(__name__)


def aggregate_author_count(
    git_directory_path: str,
    filters: List[Pattern[str]],
    revision: str = "HEAD",
):
    logger.info(f"{git_directory_path=}, {filters=}, {revision=}")

    author_count_per_filters: OrderedDict[Pattern[str], Counter] = OrderedDict(
        [(f, Counter()) for f in filters]
    )

    repo = git.Repo(path=git_directory_path)
    for entry in repo.commit(rev=revision).tree.traverse():
        if entry.type != "blob":
            continue

        abspath = entry.abspath

        matched_filters = [f for f in filters if f.search(abspath)]
        if not matched_filters:
            logger.debug(f"skip: {abspath}")
            continue

        logger.debug(f"read: {abspath}")

        author_counter = Counter(
            itertools.chain.from_iterable(
                [
                    [blame_entry.author.name] * len(lines)
                    for blame_entry, lines in repo.blame(rev=revision, file=abspath)
                ]
            )
        )

        for matched_filter in matched_filters:
            author_count_per_filters[matched_filter] += author_counter

    return author_count_per_filters
