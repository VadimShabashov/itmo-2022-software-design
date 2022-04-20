from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Ls


class TestLs:
    ls = Ls()

    def test_ls_with_dir(self):
        execution_status = ExecutionStatus()
        out_dir = "./test/operations/resources/ls"

        self.ls.execute(out_dir, execution_status=execution_status)
        print(execution_status.errors)
        print(execution_status.output)
        assert set(execution_status.output.replace("\n", " ").replace("  ", " ").split(" ")) == \
               {"inner_dir", "in1.txt", "in2.txt"}
        assert execution_status.errors == []

    def test_ls_just_files(self):
        execution_status = ExecutionStatus()
        inner_dir = "./test/operations/resources/ls/inner_dir"

        self.ls.execute(inner_dir, execution_status=execution_status)
        assert set(execution_status.output.replace("\n", " ").replace("  ", " ").split(" ")) == \
               {"in3.txt", "in4.txt", "in5.txt"}
        assert execution_status.errors == []
