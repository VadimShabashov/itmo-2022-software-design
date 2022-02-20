from pathlib import Path, PurePath
import subprocess
import sys


class Operation:
    """
    Этот класс играет роль интерфейса, от которого наследуются все операторы bash.
    Операторы переопределяют метод execute.
    """

    @staticmethod
    def execute(*args, prev_output):
        pass


class Echo(Operation):
    @staticmethod
    def execute(*args, prev_output):
        return " ".join(args), ""


class Pwd(Operation):
    @staticmethod
    def execute(*args, prev_output):
        return Path(__file__).resolve().parent.parent, ""


class Cat(Operation):
    @staticmethod
    def execute(*args, prev_output):
        if args:
            outputs = []
            for file_name in args:
                try:
                    with open(file_name, 'r') as file:
                        outputs.append(file.read())
                except FileNotFoundError:
                    try:
                        with open(PurePath(Path(__file__).resolve().parent.parent, file_name), 'r') as file:
                            outputs.append(file.read())
                    except FileNotFoundError:
                        return "", f"cat: {file_name}: No such file or directory"
            return "\n".join(outputs), ""
        else:
            if prev_output:
                return prev_output, ""
            else:
                return sys.stdin.read(), ""


class Wc(Operation):
    @staticmethod
    def execute(*args, prev_output):
        outputs = []

        # Либо читаем из stdin, либо из файлов
        if len(args) == 0:
            statistics = [0, 0, 0]

            if prev_output:
                text = prev_output
            else:
                text = sys.stdin.read()

            for line in text.split('\n'):
                statistics[0] += 1
                words = line.split()
                statistics[1] += len(words)
                statistics[2] += len(line) + 1

            outputs.append(" ".join(str(s) for s in statistics))
        else:
            statistics_total = [0, 0, 0]
            for file_name in args:
                statistics = [0, 0, 0]

                try:
                    with open(file_name) as file:
                        file_text = file.read()
                except FileNotFoundError:
                    try:
                        with open(PurePath(Path(__file__).resolve().parent.parent, file_name), 'r') as file:
                            file_text = file.read()
                    except FileNotFoundError:
                        return "", f"wc: {file_name}: No such file or directory"

                for line in file_text.split('\n'):
                    line = line.rstrip()
                    statistics[0] += 1
                    words = line.split()
                    statistics[1] += len(words)
                    statistics[2] += len(line) + 1

                if len(args) > 1:
                    for ind, statistic in enumerate(statistics):
                        statistics_total[ind] += statistic

                outputs.append(" ".join(str(s) for s in statistics) + " " + file_name)

            if len(args) > 1:
                outputs.append(" ".join(str(s) for s in statistics_total) + " " + "total")

        return "\n".join(outputs), ""


class Exit(Operation):
    @staticmethod
    def execute(*args, prev_output):
        return "", "exit"


class OperationGetter:
    """
    Класс отвечает за выполнение переданной в текстовом виде команды.
    """

    operations_dict = {"echo": Echo,
                       "pwd": Pwd,
                       "cat": Cat,
                       "wc": Wc,
                       "exit": Exit}

    def __init__(self):
        pass

    @staticmethod
    def execute_operation(*args, name, prev_output):
        if name in OperationGetter.operations_dict:
            return OperationGetter.operations_dict[name].execute(*args, prev_output=prev_output)
        else:
            try:
                # Пробуем запустить процесс в терминале
                process = subprocess.run([f"x-terminal-emulator -e {name}", *args], shell=True)
                output = process.stdout
                status = process.stderr or ""
                return output, status
            except FileNotFoundError:
                return "", f"{name}: command not found"
