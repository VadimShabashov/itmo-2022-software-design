from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Echo


class TestEcho:
    echo = Echo()

    def test_echo_single_phrase(self):
        execution_status = ExecutionStatus()
        self.echo.execute("Cats", execution_status=execution_status)
        assert execution_status.output == "Cats"

    def test_echo_several_phrases(self):
        execution_status = ExecutionStatus()
        self.echo.execute("Hello", "cats!", execution_status=execution_status)
        assert execution_status.output == "Hello cats!"

    def test_echo_empty(self):
        execution_status = ExecutionStatus()
        self.echo.execute(execution_status=execution_status)
        assert execution_status.output == ""
