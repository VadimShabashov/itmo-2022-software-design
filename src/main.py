import sys

from src.parser.parser import Parser
from src.operations.operation_executor import OperationExecutor
from src.operations.execution_status.execution_status import ExecutionStatus
from src.stream.stream import Stream


class Bash:
    """
    Класс реализует функциональность Bash.
    """

    def __init__(self, input_stream=sys.stdin):
        self.stream = Stream(input_stream, sys.stdout)
        self.parser = Parser()
        self.operation_getter = OperationExecutor

    def execute_string(self, input_string):
        """
        Исполняем строку, которую считали из потока.
        Она может быть пайплайном; поэтому между всеми операциями передается execution_status
        """

        parsed_string, parse_status = self.parser.parse(input_string)
        execution_status = ExecutionStatus()
        if parse_status:
            execution_status.add_error(parse_status)

        is_cd_none_effect = len(parsed_string) > 1
        for pipe_ind, pipeline in enumerate(parsed_string):
            if pipeline:
                operator = pipeline[0]
                args = pipeline[1:]

                if operator == "cd" and is_cd_none_effect:
                    # no such effect
                    self.operation_getter.execute_operation(*args, command_name="pwd",
                                                            execution_status=execution_status)
                    current_directory = execution_status.output
                    self.operation_getter.execute_operation(*args, command_name="cd",
                                                            execution_status=execution_status)
                    self.operation_getter.execute_operation(current_directory, command_name="cd",
                                                            execution_status=execution_status)
                else:
                    self.operation_getter.execute_operation(*args, command_name=operator,
                                                            execution_status=execution_status)

                if pipe_ind != len(parsed_string) - 1:
                    execution_status.make_prev_output()

                    # Т.к. при команде ... | exit | ... команда exit будет просто проигнорирована
                    execution_status.undo_exit()

        return execution_status

    def run(self):
        """
        Реализуем REPL. Он читает из input_stream и передает в пайплайне execution_status.
        В конце выводит результат в output_stream.
        """

        self.stream.welcome()

        while True:
            input_string = self.stream.read()
            execution_status = self.execute_string(input_string)
            self.stream.write_execution_status(execution_status)

            if execution_status.exit:
                break

        self.stream.goodbye()


if __name__ == "__main__":
    bash = Bash()
    bash.run()
