import os

from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Cd


class TestCd:
    cd = Cd()
    initial_dir = os.getcwd()

    def return_dir(self):
        self.cd.execute(self.initial_dir, execution_status=ExecutionStatus())

    def test_cd_full_path(self):
        execution_status = ExecutionStatus()
        cur_dir = "./test/operations/resources/"

        self.cd.execute(cur_dir, execution_status=execution_status)
        new_dir = os.path.abspath(os.path.basename(cur_dir))
        assert os.path.abspath(os.getcwd()) == new_dir

        self.return_dir()

    def test_cd_prev_dir(self):
        execution_status = ExecutionStatus()
        cur_dir = "./test/operations/resources/"
        prev_cur_dir = "./test/operations/"
        self.cd.execute(cur_dir, execution_status=execution_status)

        self.cd.execute("..", execution_status=execution_status)
        new_dir = os.path.abspath(os.path.basename(prev_cur_dir))
        assert os.path.abspath(os.getcwd()) == new_dir

        self.return_dir()

    def test_cd_cur_dir(self):
        execution_status = ExecutionStatus()
        cur_dir = "./test/operations/resources/"
        self.cd.execute(cur_dir, execution_status=execution_status)

        self.cd.execute(".", execution_status=execution_status)
        new_dir = os.path.abspath(os.path.basename(cur_dir))
        assert os.path.abspath(os.getcwd()) == new_dir

        self.return_dir()
