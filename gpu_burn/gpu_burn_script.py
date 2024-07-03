# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

"""
This script will wrap around the `gpu_burn` binary
It will serve several functions:
    - Make it easier to use the `gpu_burn` binary as it needs to be ran
        from a directory that has `compare.ptx` to work (as `compare.ptx` provides the kernel setting);
        This script will handle this dependency on `compare.ptx` making it less of a hassle for users
    - Get the stdout of `gpu_burn` for downstream parsing such as converting the `gpu_burn` stdout to binary output,
        such as a binary signal (0 or 1 for success or failure) for epilog action, health check, and/or for scuba logging
    - Provide better logging to help debug

The approach for the running `gpu_burn` binary is as follows:
    - Go to the directory where the `gpu_burn` and `compare.ptx` are
        - Use a default path but provide options for users to specify their own paths
   - Execute the `gpu_burn` binary and return the stdout and stderr
        - Handle any errors that may occur in the `gpu_burn` process
"""

### IMPORTS ###
import argparse
import json
import logging
import os
import subprocess
from subprocess import PIPE
from typing import List, Tuple
import sys


### LOGGING ###
log = logging.getLogger()

### GLOBAL VARIABLES ###
# default absolute path to `gpu_burn` and `compare.ptx` based on RPM installation configurations unless otherwise specified
GPU_BURN_ROOT = "/usr/lib/gpu_burn"

### FUNCTIONS ###
def run_shell_command(
    cmd: List[str], timeout_threshold_secs: int = 60
) -> Tuple[str, str]:
    """
    Given a command, it executes the shell command and handles errors

    Inputs:
        `cmd`: the terminal commands string as a list of each component
        `timeout_threshold_secs`: the timeout threshold in seconds; by default, it's a 60 seconds

    Returns:
        the stdout and stderr from the terminal command
    """
    try:
        log.debug(f"Attempting to run the command: {' '.join(cmd)}")
        res = subprocess.run(
            cmd,
            stdout=PIPE,
            stderr=PIPE,
            timeout=timeout_threshold_secs,
            encoding="utf-8",
        )
        log.debug(f"Successfully ran the command: {' '.join(cmd)}")

        # get the stdout, stderr, and returncode
        stdout = res.stdout
        stderr = res.stderr
        returncode = res.returncode

        log.debug(f"The stdout was: {stdout}\nThe stderr was: {stderr}\nThe returncode was: {returncode}")

        return stdout, stderr, returncode
    except subprocess.TimeoutExpired as e:
        error_msg = f"Process exceeded time out threshold after running for more than {timeout_threshold_secs} seconds; got exception message: {e}"
        log.error(error_msg)

        # return issue as stdout, stderr, and returncode
        return "", error_msg, 0


def valid_gpu_burn_path(gpu_burn_path) -> str:
    """
    Validate if the `gpu_burn` path is valid

    Inputs:
        - `gpu_burn_path`: file path of the `gpu_burn` folder

    Return:
        Throws an error if the paths don't exist, else no errors
    """
    # make sure the folder exists
    if not os.path.isdir(gpu_burn_path):
        error_msg = f"The `gpu_burn` folder does not exist: {gpu_burn_path}"
        log.error(error_msg)
        raise FileNotFoundError(error_msg)
    log.debug(f"The `gpu_burn` folder exists: {gpu_burn_path}")

    # make sure `gpu_burn` and `compare.ptx` is contained in the folder
    gpu_burn_binary_path = os.path.join(gpu_burn_path, "gpu_burn")
    if not os.path.exists(gpu_burn_binary_path):
        error_msg = f"The `gpu_burn` binary is not found at: {gpu_burn_binary_path}"
        log.error(error_msg)
        raise FileNotFoundError(error_msg)
    log.debug(f"The `gpu_burn` binary is found at: {gpu_burn_binary_path}")

    compare_ptx_path = os.path.join(gpu_burn_path, "compare.ptx")
    if not os.path.exists(compare_ptx_path):
        error_msg = f"The `compare.ptx` file is not found at: {compare_ptx_path}"
        log.error(error_msg)
        raise FileNotFoundError(error_msg)
    log.debug(f"The `compare.ptx` file is found at: {compare_ptx_path}")

    log.debug(f"Found `gpu_burn` binary and `compare.ptx` files in: {gpu_burn_path}")
    return gpu_burn_path


def execute_gpu_burn(
    gpu_burn_path: str, gpu_burn_arguments: List[str], time_secs: float
) -> Tuple[str, str]:
    """
    Executes the `gpu_burn` binary

    Inputs:
        - `gpu_burn_path`: file path of the gpu burn directory

    Returns:
        - the stdout and stderr from the `gpu_burn` binary
    """
    # store the current working directory
    cwd = os.getcwd()
    log.debug(f"Current working directory path: {cwd}")

    # change current working directory to the tmp directory
    log.debug(
        f"Attempting to changing current working directory to the tmp directory at: {gpu_burn_path}"
    )
    os.chdir(gpu_burn_path)
    log.debug(
        f"Changed current working directory to the tmp directory at: {gpu_burn_path}"
    )

    try:
        # execute the gpu_burn binary (set timeout to be twice the desired gpu_burn time)
        cmd = ["./gpu_burn", *gpu_burn_arguments, f"{time_secs}"]
        timeout_threshold_secs = 2 * time_secs
        log.debug(
            f"Executing the `gpu_burn` binary with `run_shell_command` with the following input `cmd` = {cmd} and `timeout_threshold_secs` = {timeout_threshold_secs}"
        )
        stdout, stderr, returncode = run_shell_command(
            cmd, timeout_threshold_secs=timeout_threshold_secs
        )
    except Exception as e:
        error_msg = f"Failed to run `gpu_burn` binary; received error: {e}"
        log.error(error_msg)
        raise RuntimeError(error_msg)
    finally:
        # return to the original working directory
        os.chdir(cwd)
        log.debug(f"Returned to the original working directory at: {cwd}")

    # return the stdout, stderr, and returncode
    return stdout, stderr, returncode


def main() -> None:
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
        "gpu_burn_arguments",
        nargs="*",
        help="""Pass arguments to the `gpu_burn` binary""",
    )
    parser.add_argument(
        "-t",
        "--time_secs",
        nargs="?",
        const=60,
        default=60,
        type=int,
        help="""Set the time for running `gpu_burn` in seconds""",
    )
    parser.add_argument(
        "-gbr",
        "--gpu_burn_root",
        default=GPU_BURN_ROOT,
        type=valid_gpu_burn_path,
        help="""Set the gpu burn root directory""",
    )

    args = parser.parse_args()
    debug = args.debug
    gpu_burn_arguments = args.gpu_burn_arguments
    time_secs = args.time_secs
    gpu_burn_root = args.gpu_burn_root

    ### LOGGING ###
    # set a severity threshold based on the mode (debug or info)
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s | %(levelname)s: %(message)s",
    )

    # emit a info that logger is set
    log.debug("Logger configured")

    ### GPU BURN EXECUTION ###
    stdout, stderr, returncode = execute_gpu_burn(gpu_burn_root, gpu_burn_arguments, time_secs)

    # formulate output to a dictionary for easy downstream parsing
    output = {
        "gpu_burn_time": time_secs,
        "gpu_burn_arguments": gpu_burn_arguments,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode
    }
    for key, value in output.items():
        log.debug(f"{key}: {value}")

    # print json formatted output
    print(json.dumps(output))


if __name__ == "__main__":
    main()
