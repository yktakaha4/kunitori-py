from collections import Counter, OrderedDict
from re import Pattern
from typing import List

import git


def aggregate_author_count(
    git_directory_path: str,
    filters: List[Pattern[str]],
    revision: str = "HEAD",
):
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
            print(f"skip: {abspath}")
            continue

        print(f"read: {abspath}")

        author_counter = Counter(
            [
                blame_entry[0].author.name
                for blame_entry in repo.blame(rev=revision, file=abspath)
            ]
        )

        for matched_filter in matched_filters:
            author_count_per_filters[matched_filter] += author_counter

    return author_count_per_filters
