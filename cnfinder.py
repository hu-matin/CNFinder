import argparse
import platform
import shutil
import subprocess
from pathlib import Path


GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CLEAR = "\033[0m"


def find_tool() -> str | None:
    system = platform.system()

    if system == "Windows":
        if shutil.which("nslookup"):
            return "nslookup"
    else:
        for tool in ("dig", "nslookup"):
            if shutil.which(tool):
                return tool

    return None


def get_cname(domain: str, tool: str) -> str | None:
    try:
        if tool == "nslookup":
            command = ["nslookup", "-type=CNAME", domain]
        else:
            command = ["dig", "+short", "CNAME", domain]

        result = subprocess.run(command, capture_output=True, text=True, timeout=5)

    except (subprocess.SubprocessError, OSError):
        return None

    if result.returncode != 0:
        return None

    if tool == "dig":
        for line in result.stdout.splitlines():
            line = line.strip()

            if line:
                return line.rstrip(".")

    # nslookup output
    for line in result.stdout.splitlines():
        line = line.strip()

        if "canonical name =" in line.lower():
            return line.split("=", 1)[1].strip().rstrip(".")

    return None


def cname_finder(file: Path, output: Path | None = None) -> None:
    if not file.is_file():
        print(f"{RED}[!] File not found: {file}{CLEAR}")
        return

    tool = find_tool()

    if tool is None:
        print(f"{RED}[!] No supported DNS tool found (dig/nslookup).{CLEAR}")
        return

    print(f"{GREEN}[*] Using: {tool}{CLEAR}")

    output_file = None

    try:
        if output:
            output_file = output.open(
                "w",
                encoding="utf-8",
            )

            print(f"{GREEN}[*] Saving CNAME results to: {output}{CLEAR}")

        print()

        with file.open("r", encoding="utf-8") as f:
            for line in f:
                domain = line.strip()

                if not domain:
                    continue

                cname = get_cname(domain, tool)

                if cname:
                    result_line = f"{domain} -> {cname}"

                    print(f"{GREEN}[+] CNAME found: {result_line}{CLEAR}")

                    if output_file:
                        output_file.write(result_line + "\n")
                        output_file.flush()

                else:
                    print(f"{YELLOW}[-] No CNAME found for {domain}{CLEAR}")
    finally:
        if output_file:
            output_file.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CNAME finder"
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Input file (.txt) containing domains.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Save only domains with found CNAMEs to your .txt file.",
    )

    args = parser.parse_args()

    cname_finder(
        args.input,
        args.output,
    )


if __name__ == "__main__":
    main()