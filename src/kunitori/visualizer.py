from collections import Counter
from datetime import datetime
from logging import getLogger
from os.path import dirname, join
from re import Pattern
from typing import List, OrderedDict, Tuple

from jinja2 import Environment, FileSystemLoader

template_directory_path = join(dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_directory_path))

logger = getLogger(__name__)


def visualize(
    export_directory_path: str,
    name: str,
    data: List[Tuple[str, OrderedDict[Pattern[str], Counter]]],
):
    logger.info(f"{export_directory_path=}, {name=}, {data=}")
    template = jinja_env.get_template("chart.j2")
    template_data = {
        "revisions": [
            {
                "revision": revision,
                "patterns": [
                    {"pattern": pattern.pattern, "counter": counter}
                    for pattern, counter in patterns.items()
                ],
            }
            for revision, patterns in data
        ]
    }

    file_name = f'chart_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    with open(join(export_directory_path, file_name), mode="w") as f:
        f.write(
            template.render(
                {
                    "name": name,
                    "data": template_data,
                }
            )
        )
