import os

from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Pwd


class TestPwd:
    pwd = Pwd()

    def test_pwd_start_dir(self):
        execution_status = ExecutionStatus()
        self.pwd.execute(execution_status=execution_status)
        assert execution_status.output == os.getcwd()
