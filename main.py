import os

import click
import jsonstreams

from encoder import EnsureAsciiFalseEncoder
from scraping import ScheduleScraping
from table import facultyID2name


@click.command()
@click.argument("termid")
@click.argument("facultyid")
def cmd(termid, facultyid):
    if facultyid == "all":
        facultyIDs = facultyID2name.keys()
    else:
        facultyIDs = [facultyid]

    for facultyID in facultyIDs:
        faculty = facultyID2name[facultyID]
        print(f"{faculty} のデータを取得します")

        dirPath = f"data/{termid}"

        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        filename = f"data/{termid}/{facultyID2name[facultyID]}.json"

        if os.path.exists(filename):
            if input(f"既に{filename}があります。上書きしますか？[y/n] : ") != "y":
                return

        with ScheduleScraping(termid, facultyID) as ss:
            print("結果ページに接続しています...")
            ss.toResultPage()

            with jsonstreams.Stream(
                jsonstreams.Type.ARRAY,
                filename=filename,
                indent=4,
                encoder=EnsureAsciiFalseEncoder,
            ) as s:
                for item in ss.getItems():
                    s.write(item)


def main():
    cmd()


if __name__ == "__main__":
    main()
