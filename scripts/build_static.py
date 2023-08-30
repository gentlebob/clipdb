import ujson as json
import sys
from pathlib import Path
import os
import itertools

LIMIT = 50


# recursively generate json files in descending order
def recursiveLsJson(directory):
    entries = list(os.scandir(directory))
    entries.sort(key=lambda e: e.name, reverse=True)
    for entry in entries:
        path = os.path.join(directory, entry.name)
        if entry.is_file() and entry.name.endswith(".json"):
            yield path
        else:
            yield from recursiveLsJson(path)


def main():
    repoBasePath = Path(os.path.realpath(__file__)).parent.parent.absolute()
    dataBasepath = os.path.join(repoBasePath, "data")
    staticBuildBasePath = os.path.join(repoBasePath, "gentlebob.github.io", "cd")
    Path(staticBuildBasePath).mkdir(parents=True, exist_ok=True)
    total = 0
    for filename in itertools.islice(recursiveLsJson(dataBasepath), LIMIT):
        outFilename = os.path.join(staticBuildBasePath, str(total))
        with open(filename) as f, open(outFilename, "w+") as outf:
            info = json.load(f)
            outf.write("%s %d" % (info["webpage_url"], info["duration"] + 3))
            total += 1

    jsFilename = os.path.join(staticBuildBasePath, "randclip.txt")
    with open(jsFilename, "w+") as f:
        f.write(
            """"https://www.gentlebob.com/cd/" + Math.floor(Math.random()*%d)""" % total
        )


if __name__ == "__main__":
    main()
