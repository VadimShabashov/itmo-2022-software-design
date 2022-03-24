from src.parser.parser import Parser
from src.operations.operations import OperationGetter


class Bash:
    """
    Класс реализует функциональность Bash.
    """

    def __init__(self, input_stream=None, output_stream=None):
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.parser = Parser()
        self.operation_getter = OperationGetter

    def make_assignment(self, expression):
        """
        Обеспечиваем функциональность присваивания переменных.
        """
        var_name, var_value = expression.split("=", maxsplit=1)  # Т.к. первый знак равенства отвечает за присваивание
        self.parser.variables[var_name] = var_value

    def execute_string(self, input_string):
        """
        Исполняем строку, которую считали. Она может быть пайплайном; поэтому между всеми операциями передается output.
        """

        parsed_string, assignment_status = self.parser.parse(input_string)
        output = ""
        status = ""

        if assignment_status:
            for expr in parsed_string[0]:
                self.make_assignment(expr)
        else:
            for pipeline in parsed_string:
                if pipeline:
                    operator = pipeline[0]
                    args = pipeline[1:]

                    # status - отвечает за статус возврата из функции:
                    # status = "" при отсутствии ошибки,
                    # status = "exit" при выполнении команды exit,
                    # status = "описание ошибки" при ошибке.
                    output, status = self.operation_getter.execute_operation(*args, name=operator, prev_output=output)

                    if status:
                        if (status == "exit") and (len(parsed_string) > 1):
                            status = ""  # Т.к. при команде ... | exit | ... команда exit будет просто проигнорирована
                        else:
                            return output, status

        return output, status

    def write_output(self, output, status):
        """
        Запись результата может производиться как в stdout, так и в файл. Она производится построчно, поэтому если
        ошибка произошла в i-ой строке, предыдущие (i-1) строчка будут записаны.

        Функция возвращает bool - надо ли продолжать REPL (true - если да; false - если нет).
        """

        if status == "":
            if output:
                if self.output_stream:
                    try:
                        with open(self.output_stream, 'w+') as output_file:
                            output_file.write(str(output))
                    except FileNotFoundError:
                        print(f"File {self.output_stream} wasn't found for output stream")
                        return
                else:
                    print(output)

            return True
        else:
            if status != "exit":
                print(status)
            return False

    def run(self):
        """
        Реализуем REPL. Он читает из input_stream и передает в пайплайне между операциями output.
        В конце выводит результат в output_stream.
        """

        # Чтение команд может производиться из файла
        if self.input_stream:
            try:
                with open(self.input_stream, 'r') as input_file:
                    for input_string in input_file:
                        output, status = self.execute_string(input_string)

                        if not self.write_output(output, status):
                            return
            except FileNotFoundError:
                print(f"File {self.input_stream} wasn't found for input stream")
                return

        else:
            while True:
                input_string = input(">>> ")
                output, status = self.execute_string(input_string)

                if not self.write_output(output, status):
                    return


if __name__ == "__main__":
    print("Bash is started. Welcome back, sir/madame!")
    bash = Bash()
    bash.run()
    print("Bash is terminated. Good day, sir/madame!")
