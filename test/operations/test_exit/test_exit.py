from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Exit


class TestExit:
    exit = Exit()

    def test_exit(self):
        execution_status = ExecutionStatus()
        self.exit.execute(execution_status=execution_status)
        assert execution_status.exit
