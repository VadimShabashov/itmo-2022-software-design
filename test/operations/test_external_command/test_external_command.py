import os

from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import ExternalCommand


class TestExternalCommand:
    external_command = ExternalCommand()

    def test_external_command_echo(self):
        execution_status = ExecutionStatus()

        expected_output = "cats\n"
        agrs = 'cats'
        command_name = 'echo'
        self.external_command.execute(agrs, command_name, execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_external_command_pwd(self):
        execution_status = ExecutionStatus()

        expected_output = os.getcwd() + "\n"
        command_name = 'pwd'
        self.external_command.execute(command_name, execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors
