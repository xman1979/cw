import unittest
import json
import parameterized
import tempfile
import os
from typing import List, Tuple
import gpu_burn_epilog_parser

### HELPER FUNCTIONS ###
def generate_test_input_gpu_burn_epilog_parser(
    time_secs: int,
    gpu_burn_arguments: str,
    stdout: str,
    stderr: str,
    returncode: int) -> str:
    """
    Creates expected inputs for `gpu_burn_epilog_parser.py`

    Input: parameters that GPU Burn output would be
    Output: JSON string of GPU Burn output
    """
    output = {
        "gpu_burn_time": time_secs,
        "gpu_burn_arguments": gpu_burn_arguments,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode
    }
    return json.dumps(output)

class GpuBurnEpilogParser(unittest.TestCase):
    """
    Unittests for `gpu_burn_epilog_parser.py` assuming input is valid
    """

    # set of test cases
    testcases_map = [
        {
            "name": "Blank STDERR and Exit Code 0",
            "time_secs": 60,
            "gpu_burn_arguments": "",
            "stdout": "stuff",
            "stderr": "",
            "returncode": 0,
            "expected_returncode": 0  
        },
        {
            "name": "Blank STDERR and Exit Code 1",
            "time_secs": 60,
            "gpu_burn_arguments": "",
            "stdout": "stuff",
            "stderr": "",
            "returncode": 1,
            "expected_returncode": 1 
        },
        {
            "name": "Blank STDERR and Exit Code 124",
            "time_secs": 60,
            "gpu_burn_arguments": "",
            "stdout": "stuff",
            "stderr": "",
            "returncode": 124,
            "expected_returncode": 124 
        },
        {
            "name": "Blank STDERR and Exit Code 0 with -d argument",
            "time_secs": 60,
            "gpu_burn_arguments": "-d",
            "stdout": "stuff",
            "stderr": "",
            "returncode": 0,
            "expected_returncode": 0  
        },
        {
            "name": "Blank STDERR and Exit Code 1 with -d argument",
            "time_secs": 60,
            "gpu_burn_arguments": "-d",
            "stdout": "stuff",
            "stderr": "",
            "returncode": 1,
            "expected_returncode": 1 
        },
        {
            "name": "Blank STDERR and Exit Code 124 with -d argument",
            "time_secs": 60,
            "gpu_burn_arguments": "-d",
            "stdout": "stuff",
            "stderr": "",
            "returncode": 124,
            "expected_returncode": 124 
        },
        {
            "name": "Non-Blank STDERR and Exit Code 0 with -d argument",
            "time_secs": 60,
            "gpu_burn_arguments": "-d",
            "stdout": "stuff",
            "stderr": "error",
            "returncode": 0,
            "expected_returncode": 0
        },
        {
            "name": "Non-Blank STDERR and Exit Code 1 with -d argument",
            "time_secs": 60,
            "gpu_burn_arguments": "-d",
            "stdout": "stuff",
            "stderr": "error",
            "returncode": 1,
            "expected_returncode": 1 
        },
        {
            "name": "Non-Blank STDERR and Exit Code 124 with -d argument",
            "time_secs": 60,
            "gpu_burn_arguments": "-d",
            "stdout": "stuff",
            "stderr": "error",
            "returncode": 124,
            "expected_returncode": 124
        },
    ]

    @parameterized.parameterized.expand([
        [
            t["name"], 
            t["time_secs"],
            t["gpu_burn_arguments"],
            t["stdout"],
            t["stderr"],
            t["returncode"],
            t["expected_returncode"]
        ] for t in testcases_map
    ])
    def test_gpu_burn_epilog_parser(
        self,
        name: str,
        time_secs: int,
        gpu_burn_arguments: str,
        stdout: str,
        stderr: str,
        returncode: int,
        expected_returncode: int):
        """Test for correct exit code behavior (assuming inputs are valid)"""
        
        # generate test GPU Burn JSON
        gpu_burn_output = generate_test_input_gpu_burn_epilog_parser(
            time_secs = time_secs,
            gpu_burn_arguments = gpu_burn_arguments,
            stdout = stdout,
            stderr = stderr,
            returncode = returncode
        )

        # create a temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'gpu_burn_output.txt')
            with open(tmpfile, 'w') as f:
                f.write(gpu_burn_output)
                f.flush()

            args = ["-p", tmpfile]

            # check exit codes
            actual_returncode = gpu_burn_epilog_parser.main_impl(args)
            self.assertEqual(actual_returncode, expected_returncode, 
                f"Got incorrect return codes; expected {expected_returncode}, actually got {actual_returncode}")

    @parameterized.parameterized.expand([
        [
            t["name"], 
            t["time_secs"],
            t["gpu_burn_arguments"],
            t["stdout"],
            t["stderr"],
            t["returncode"],
            t["expected_returncode"]
        ] for t in testcases_map
    ])
    def test_gpu_burn_epilog_parser_exit_code(
        self,
        name: str,
        time_secs: int,
        gpu_burn_arguments: str,
        stdout: str,
        stderr: str,
        returncode: int,
        expected_returncode: int):
        """Test for correct exit code behavior (assuming inputs are valid)"""
        
        # generate test GPU Burn JSON
        gpu_burn_output = generate_test_input_gpu_burn_epilog_parser(
            time_secs = time_secs,
            gpu_burn_arguments = gpu_burn_arguments,
            stdout = stdout,
            stderr = stderr,
            returncode = returncode
        )

        # create a temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'gpu_burn_output.txt')
            with open(tmpfile, 'w') as f:
                f.write(gpu_burn_output)
                f.flush()

            args = ["-p", tmpfile]

            # check exit codes
            with self.assertRaises(SystemExit) as cm:
                gpu_burn_epilog_parser.main(args)
            
            self.assertEqual(cm.exception.code, expected_returncode)


if __name__ == '__main__':
    unittest.main()
