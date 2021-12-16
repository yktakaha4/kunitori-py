import re
from os import environ, getcwd
from os.path import basename, join

from kunitori.aggregator import aggregate_author_count
from kunitori.visualizer import visualize


def main():
    git_directory_path = environ["GIT_DIRECTORY_PATH"]
    filters = [re.compile(r"\.py$"), re.compile(r"\.(ts|vue)$")]
    revisions = environ["GIT_REVISIONS"].split(",")

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


if __name__ == "__main__":
    main()
