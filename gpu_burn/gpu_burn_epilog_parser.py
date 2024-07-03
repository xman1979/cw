"""
Parses the output from `gpu_burn` to create 0 or 1 flags for SLURM epilog
    - returns non-zero flag if at least one GPU is faulty or less than 8 GPUs found
Non-zero flag in epilog leads to the node entering the DRAIN state: https://slurm.schedmd.com/prolog_epilog.html
"""
import argparse
import logging
import json
import sys
from typing import Sequence, Optional

### LOGGING ###
log = logging.getLogger(__name__)

def main_impl(argv: Sequence[str]) -> int:
    """
    Handles argument parsing, logging, and script execution
    """
    ### ARGUMENT PARSING ###
    # Add a command line argument
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="""Toggle for running the script in debug mode""",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=argparse.FileType("r"),
        help="""Path to the log file where the gpu_burn output lives""",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="""Toggle for emitting gpu_burn_output to stdout""",
    )

    args = parser.parse_args(argv)
    debug = args.debug
    path = args.path
    output = args.output

    ### LOGGING ###
    # set a severity threshold based on the mode (debug or info)
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s | %(levelname)s: %(message)s",
    )

    # emit a info that logger is set
    log.debug("Logger configured")

    ### GPU BURN PARSER ###
    gpu_burn_output = json.loads(path.read())
    path.close()

    if output:
        # serialize `gpu_burn_output` to JSON and escape double quotes for bash safety
        print(json.dumps(gpu_burn_output).replace('"', '\\"'))
    returncode = int(gpu_burn_output["returncode"])

    # use the returncode directly from the gpu_burn_script
    log.debug(f"Using the return code; found: {returncode}")
    return returncode

def main(args: Optional[Sequence[str]] = None):
    if args == None:
        # first item is the path or name of the script itself https://stackoverflow.com/a/17119118
        args = sys.argv[1:]

    sys.exit(main_impl(args))

if __name__ == "__main__":
    main()
    
