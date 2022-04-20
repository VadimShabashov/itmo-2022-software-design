from src.operations.execution_status.execution_status import ExecutionStatus


class TestExecutionStatus:
    def test_execution_status_do_exit(self):
        execution_status = ExecutionStatus()

        execution_status.do_exit()
        assert execution_status.exit

    def test_execution_status_undo_exit(self):
        execution_status = ExecutionStatus()
        execution_status.exit = False

        execution_status.undo_exit()
        assert not execution_status.exit

    def test_execution_status_add_error(self):
        execution_status = ExecutionStatus()
        errors = ["We", "need", "more", "cats"]

        for error in errors:
            execution_status.add_error(error)

        assert execution_status.errors == errors

    def test_execution_status_provide_output(self):
        execution_status = ExecutionStatus()
        output = "That's output"

        execution_status.provide_output(output)

        assert execution_status.output == output

    def test_execution_status_make_prev_output(self):
        execution_status = ExecutionStatus()
        output = "That's output"
        execution_status.provide_output(output)

        execution_status.make_prev_output()

        assert execution_status.output is None
        assert execution_status.prev_output == output
