from sys import stdin, stdout

from src.parser.parser import Parser
from src.operations.operations import OperationExecutor
from src.operations.execution_status.execution_status import ExecutionStatus


class Bash:
    """
    Класс реализует функциональность Bash.
    """

    def __init__(self, input_stream=stdin, output_stream=stdout):
        self.input_stream = input_stream  # Чтение команд может производиться из файла
        self.output_stream = output_stream
        self.parser = Parser()
        self.operation_getter = OperationExecutor

    def execute_string(self, input_string):
        """
        Исполняем строку, которую считали из потока.
        Она может быть пайплайном; поэтому между всеми операциями передается execution_status
        """

        parsed_string = self.parser.parse(input_string)
        execution_status = ExecutionStatus()

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

    def write_output(self, execution_status):
        """
        Вывод ошибок и результата в поток
        """

        for error in execution_status.errors:
            self.output_stream.write(error)

        if execution_status.output:
            self.output_stream.write(execution_status.output)

    def run(self):
        """
        Реализуем REPL. Он читает из input_stream и передает в пайплайне execution_status.
        В конце выводит результат в output_stream.
        """

        self.output_stream.write("Bash is started. Welcome back, sir/madame!")

        while True:
            if self.input_stream == stdin:
                self.output_stream.write("\n>>> ")

            input_string = self.input_stream.readline().rstrip()
            execution_status = self.execute_string(input_string)
            self.write_output(execution_status)

            if execution_status.exit:
                break

        self.output_stream.write("Bash is terminated. Good day, sir/madame!")


if __name__ == "__main__":
    bash = Bash()
    bash.run()
