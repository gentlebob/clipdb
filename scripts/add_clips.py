#!/usr/bin/env python3

import yt_dlp
import ujson as json
import sys
from pathlib import Path
import os
import datetime

def main():
    dataBasePath = os.path.join(
        Path(os.path.realpath(__file__)).parent.parent.absolute(), "data"
    )
    urls = sys.argv[1:]
    with yt_dlp.YoutubeDL() as ydl:
        for url in urls:
            info = ydl.extract_info(url, download=False)
            if 'Creator' in info and info['Creator'] != "CuteDog_": continue
            if 'creator' in info and info['creator'] != "CuteDog_": continue
            date = datetime.date.fromtimestamp(info["timestamp"])
            outdir = os.path.join(dataBasePath, str(date.year), "%02d" % (date.month))
            Path(outdir).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(outdir, info["id"] + ".json"), "w+") as f:
                json.dump(ydl.sanitize_info(info), f)


if __name__ == "__main__":
    main()
