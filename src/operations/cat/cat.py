from src.operations.operation import Operation


class Cat(Operation):
    @staticmethod
    def execute(*args, execution_status):
        if args:
            outputs = []
            for file_name in args:
                try:
                    with open(file_name, 'r') as file:
                        outputs.append(file.read())
                except FileNotFoundError:
                    execution_status.add_error(f"cat: {file_name}: No such file or directory")

            if outputs:
                execution_status.provide_output("\n".join(outputs))

        else:
            if execution_status.prev_output:
                execution_status.provide_output(execution_status.prev_output)
            else:
                execution_status.add_error("Command \"cat\" got zero arguments")
