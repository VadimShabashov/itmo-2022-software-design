import io
import sys

from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Wc


class TestWc:
    wc = Wc()

    def test_wc_prev_output(self):
        execution_status = ExecutionStatus()
        execution_status.prev_output = "Wonderful cats surround us!"
        expected_output = "1 4 28"
        self.wc.execute(execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_wc_file(self):
        execution_status = ExecutionStatus()
        expected_output = "3 14 66 ./test/operations/resources/wc/text1.txt"
        self.wc.execute('./test/operations/resources/wc/text1.txt', execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_wc_files(self):
        execution_status = ExecutionStatus()
        expected_output = ("3 14 66 ./test/operations/resources/wc/text1.txt\n"
                           "3 13 58 ./test/operations/resources/wc/text2.txt\n"
                           "6 27 124 total")
        self.wc.execute('./test/operations/resources/wc/text1.txt',
                        './test/operations/resources/wc/text2.txt',
                        execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_wc_stdin(self):
        execution_status = ExecutionStatus()
        input_string = "Amazing cats\nAmazing day"
        sys.stdin = io.StringIO(input_string)

        self.wc.execute(execution_status=execution_status)
        assert execution_status.output == "2 4 25"
        assert not execution_status.errors
