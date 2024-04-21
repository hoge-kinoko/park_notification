import argparse
from pathlib import Path
from lib.aram import Aram


def main(park_list_path: Path, aram_history_path: Path):
    aram = Aram(
        park_list_path=park_list_path,
        aram_history_path=aram_history_path
    )

    aram.exec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aram execution script")
    parser.add_argument("--park-list", dest="park_list_path", type=Path, default="tmp/park_list.txt", help="Path to park list file")
    parser.add_argument("--aram-history", dest="aram_history_path", type=Path, default="tmp/aram_list.txt", help="Path to aram history file")
    args = parser.parse_args()

    main(args.park_list_path, args.aram_history_path)
