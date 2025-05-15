#! python

import argparse
import subprocess
import os
import colorama
import requests

# Filesystem
FILENAME_MAXLEN = 128
SOURCES_FILENAME = ".yt_info\source-urls.txt"
INFO_TYPES = "infojson,description"
INFO_DIR = ".yt_info"
SUBS_DIR = "Subs"

# Formats
AUDIO_FORMAT = "ba[ext=m4a]/ba[ext=mp4]/ba[ext=mp3]/ba/b"
BEST_FORMAT = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b"
HD_FORMAT = "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4] / bv*+ba/b"

# Templates
DEFAULT_TEMPLATE = "%(title)s [%(id)s].%(ext)s"
AUDIO_TEMPLATE = "%(artist&{:} - |)s%(title)s [%(id)s].%(ext)s"
DOMAIN_TEMPLATE = "%(webpage_url_domain)s,%(id)s"
ID_TEMPLATE = "%(id)s.%(ext)s"
ID_INFO_TEMPLATE = "%(id)s.%(ext)s/%(original_url)s-%(id)s.%(ext)s"
INFO_TEMPLATE = f"%(title).{FILENAME_MAXLEN}s [%(id)s]/%(original_url)s-%(id)s.%(ext)s"
SHORT_TEMPLATE = f"%(title).{FILENAME_MAXLEN}s [%(id)s].%(ext)s"


def parse_args():
    parser = argparse.ArgumentParser(prog="twat", description="The yt-dlp wrapper.")

    parser.add_argument("-c", action="store_true", help="Use Firefox cookies.")

    parser.add_argument(
        "-f",
        metavar="FORMAT",
        help="Format to download. DEFAULTS: mp4 Video (max 1080p), m4a Audio.",
    )

    parser.add_argument(
        "-i", action="store_true", help="DO NOT download JSON info unless -x is set."
    )

    parser.add_argument(
        "-Q",
        action="store_true",
        help="Download highest quality video even those larger than 1080p.",
    )

    parser.add_argument(
        "-a",
        action="store_true",
        help="Download the audio only.",
    )

    parser.add_argument("-s", action="store_true", help="Download subtitles.")

    parser.add_argument(
        "-S",
        action="store_true",
        help="Download subtitles only. Equivalent to -s -x.",
    )
    parser.add_argument(
        "-u", action="store_true", help="Use video id as output filename."
    )

    parser.add_argument("-w", action="store_true", help="Overwrite files.")

    parser.add_argument(
        "-x", action="store_true", help="Skip download.", dest="skip-download"
    )

    parser.add_argument("URI", help="Twitter URL, or filename.")

    return parser.parse_known_args()


def build_command(args, yt_args):
    # Determine the download format.
    if args["f"]:
        yt_format = args["f"]
    elif args["Q"]:
        yt_format = BEST_FORMAT
    elif args["a"]:
        yt_format = AUDIO_FORMAT
    else:
        yt_format = HD_FORMAT

    # Create the command list with non-wrapper, and default flags.
    command = (
        ["yt-dlp"]
        + yt_args
        + ["-f", yt_format, "-S", "tbr,size", "--windows-filenames"]
    )

    if args["c"]:
        command.extend(["--cookies-from-browser", "firefox"])

    if not args["w"]:
        command.extend(["--no-overwrites"])

    if args["skip-download"] and not args["i"]:
        args["i"] = True

    # Add wrapper flags to the command list
    if args["S"]:
        args["i"] = True
        args["s"] = True
        args["skip-download"] = True

    # Handle subs
    if args["s"]:
        command.extend(
            ["-P", f"{'subtitle'}:{SUBS_DIR}", "--write-subs", "--write-auto-subs"]
        )

    # Handle output template
    info_dir_template = INFO_TEMPLATE
    output_template = SHORT_TEMPLATE

    if args["u"]:
        info_dir_template = ID_INFO_TEMPLATE
        output_template = ID_TEMPLATE
    elif args["a"]:
        output_template = AUDIO_TEMPLATE

    if not args["i"]:
        command.extend([
            "--write-description",
            "--write-info-json",
            "--no-clean-infojson",
            "-P",
            f"{INFO_TYPES}:{INFO_DIR}",
            "-o",
            f"{INFO_TYPES}:{info_dir_template}",
        ])

    command.extend(["-o", output_template])

    return command


def update_sources(uri):
    if not os.path.exists(INFO_DIR):
        return

    with open(SOURCES_FILENAME, "a") as a, open(SOURCES_FILENAME, "r") as r:
        if not uri in r.read():
            a.write(uri + "\n")


def run_command(cmd, capture_output=False):
    print(colorama.Fore.GREEN + " ".join(cmd))
    return subprocess.run(cmd, capture_output=capture_output, text=True)


def download_uri(command, uri):
    # Do the deed
    result = run_command(command + [uri])

    # Retry with ID_TEMPLATE on first failure.
    if result.returncode:
        print(
            colorama.Fore.RED
            + f'Problem downloading file. Retrying with -o "{ID_TEMPLATE}".'
        )

        result = run_command(
            command
            + [
                "-o",
                ID_TEMPLATE,
                "-o",
                f"{INFO_TYPES}:{ID_INFO_TEMPLATE}",
            ]
            + [uri]
        )

    # Write uri to file on success
    if not result.returncode:
        update_sources(uri)

    return result


def download_file(command, uri):
    failed = []

    with open(uri) as file:
        while line := file.readline():
            url = line.strip()

            if not url or url[0] == "#":
                continue

            result = download_uri(command, url)

            if result.returncode:
                failed.append(url)

    return failed


def process_command(command, uri):
    failed = []

    if os.path.isfile(uri):
        failed = download_file(command, uri)
    else:
        result = download_uri(command, uri)
        if result.returncode:
            failed = [uri]

    if failed:
        print(colorama.Fore.RED + "Failed to download the following URL(s):")
        print(colorama.Fore.RED + "\n".join(failed))


def get_info(url):
    id_cmd = ["yt-dlp", "-O", DOMAIN_TEMPLATE, url]
    result = run_command(id_cmd, True)

    if result.returncode:
        return [""]

    info = result.stdout.rstrip().split(",")

    return info


def get_yt_id(url):
    info = get_info(url)

    if info[0] == "youtube.com" and len(info) > 1:
        return info[1]

    return ""


def get_yt_thumbnail(url):
    yt_id = get_yt_id(url)

    tn_url = f"https://i.ytimg.com/vi/{yt_id}/maxresdefault.jpg"

    print("Downloading thumbnail from", tn_url)

    response = requests.get(tn_url, stream=True)

    if not response.ok:
        print(colorama.Fore.RED + f"Could not download thumbnail for {yt_id}")
        return False

    t_dir = f"{INFO_DIR}/thumbnails"

    if not os.path.exists(t_dir):
        os.makedirs(t_dir)

    with open(f"{t_dir}/{yt_id}.jpg", "wb") as file:
        file.write(response.content)

    return True


def main():
    arg_ns, yt_args = parse_args()
    args = vars(arg_ns)
    uri = args.pop("URI")

    colorama.init(autoreset=True)

    command = build_command(args, yt_args)

    if args["skip-download"]:
        print("Skipping download.")
        command.extend(["--skip-download"])

    process_command(command, uri)


if __name__ == "__main__":
    main()
