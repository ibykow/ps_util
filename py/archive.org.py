import argparse
from internetarchive import download

def parse_args():
    parser = argparse.ArgumentParser(prog="archive.org", description="The arhive.org downloader.")
    parser.add_argument('-q', '--quiet', action='store_true', help="Quiet mode.")
    parser.add_argument('ID', help="archive.org identifier")

    return parser.parse_known_args()

def main():
    arg_ns, alt_args = parse_args()
    args = vars(arg_ns)
    id = args.pop("ID")

    download(id, verbose=(not args.pop("quiet")))

if __name__ == "__main__":
    main()