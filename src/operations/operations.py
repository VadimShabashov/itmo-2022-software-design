from pathlib import Path, PurePath
import subprocess
import sys
import re
import os


class Operation:
    """
    Этот класс играет роль интерфейса, от которого наследуются все операторы bash.
    Операторы переопределяют метод execute.
    """

    @staticmethod
    def execute(*args, execution_status):
        pass


class Echo(Operation):
    @staticmethod
    def execute(*args, execution_status):
        execution_status.output = " ".join(args)
        return


class Pwd(Operation):
    @staticmethod
    def execute(*args, execution_status):
        execution_status.output = os.getcwd()
        return


class Cd(Operation):
    @staticmethod
    def execute(*args, execution_status, current_directory=None):
        list_args = list(args)
        if len(list_args) > 1:
            execution_status.add_error("ls get only zero or one argument")
            return

        if len(list_args) == 0:
            from pathlib import Path
            os.chdir(str(Path.home()))
            return

        path = list_args[0]
        try:
            os.chdir(path)
        except FileNotFoundError:
            execution_status.add_error(f"cd: {path}: No such file or directory")
        return


class Ls(Operation):
    @staticmethod
    def _ls_impl(path):
        import os
        from tabulate import tabulate
        import shutil

        if os.path.isdir(path):
            dir_list = os.listdir(path)
            terminal_size, _ = shutil.get_terminal_size()

            max_column = 1
            num_files = len(dir_list)
            for column_count in range(2, num_files + 1):
                max_len_column = 0
                for j in range(0, num_files, column_count):
                    max_len_column = max(max_len_column, len(" ".join(dir_list[j: j + column_count])))
                if max_len_column > terminal_size:
                    break
                else:
                    max_column = column_count

            total_table = []
            for i in range(0, num_files, max_column):
                total_table.append(dir_list[i: i + max_column])

            return tabulate(total_table, tablefmt="plain")
        elif os.path.isfile(path):
            return path
        else:
            raise FileNotFoundError()

    @staticmethod
    def execute(*args, execution_status):
        list_args = list(args)
        if args and len(list_args) > 1:
            execution_status.add_error("ls get only zero or one argument")
            return

        if args is None or len(list_args) == 0:
            path = "."
        else:
            path = list_args[0]

        try:
            execution_status.provide_output(Ls._ls_impl(path))
        except FileNotFoundError:
            execution_status.add_error(f"ls: {path}: No such file or directory")
        return


class Cat(Operation):
    @staticmethod
    def execute(*args, execution_status):
        outputs = []
        if args:
            for file_name in args:
                try:
                    with open(file_name, 'r') as file:
                        outputs.append(file.read())
                except FileNotFoundError:
                    try:
                        with open(PurePath(Path(__file__).resolve().parent.parent, file_name), 'r') as file:
                            outputs.append(file.read())
                    except FileNotFoundError:
                        execution_status.add_error(f"cat: {file_name}: No such file or directory")
        else:
            if execution_status.prev_output:
                outputs.append(execution_status.prev_output)
            else:
                outputs.append(sys.stdin.read())

        execution_status.output = "\n".join(outputs)
        return


class Wc(Operation):
    @staticmethod
    def execute(*args, execution_status):
        outputs = []

        # Либо читаем из stdin, либо из файлов
        if len(args) == 0:
            statistics = [0, 0, 0]

            if execution_status.prev_output:
                text = execution_status.prev_output
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
                        execution_status.add_error(f"wc: {file_name}: No such file or directory")

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

        execution_status.provide_output("\n".join(outputs))
        return


class Exit(Operation):
    @staticmethod
    def execute(*args, execution_status):
        execution_status.do_exit()
        return


class Grep(Operation):
    @staticmethod
    def execute(*args, execution_status):
        flag_i = False
        flag_w = False
        flag_A = False
        n = 0
        word = None
        files = []
        result = []

        # Ищем флаги
        ind = 0
        while ind < len(args):
            arg = args[ind]
            pattern = re.compile(r"-[iwA]*")

            if not pattern.match(arg):
                if not word:
                    word = arg
                else:
                    files.append(arg)
            else:
                if "i" in arg:
                    flag_i = True

                if "w" in arg:
                    flag_w = True

                if "A" in arg:
                    if ind + 1 < len(args) and args[ind + 1].isdigit():
                        flag_A = True
                        n = int(args[ind + 1])
                        ind += 1
                    else:
                        execution_status.add_error("Valid int for -A flag wasn't provided")
                        return
            ind += 1

        if not word:
            execution_status.add_error("No word pattern for search was provided")
            return

        if not files:
            execution_status.add_error("No files for search were provided")
            return

        # Составляем регулярное выражение
        if flag_i and flag_w:
            pattern_word = re.compile(rf'(^|\s){word}($|\s)', re.IGNORECASE)
        elif flag_i:
            pattern_word = re.compile(rf'{word}', re.IGNORECASE)
        elif flag_w:
            pattern_word = re.compile(rf'(^|\s){word}($|\s)')
        else:
            pattern_word = re.compile(rf'{word}')

        # Обходим файлы
        for num_file, file_name in enumerate(files):
            try:
                with open(file_name, 'r') as file:
                    if flag_A and num_file > 0:
                        result.append("--")

                    # Число строк, которые надо вывести под строкой с найденным паттерном
                    num_strings = 0

                    for line in file:
                        line = line.rstrip()

                        if pattern_word.search(line):
                            if num_strings < 0 and flag_A:
                                result.append("--")

                            num_strings = n
                            if len(files) == 1:
                                result.append(line)
                            else:
                                result.append(file_name + ":" + line)
                        elif num_strings > 0:
                            num_strings -= 1
                            if len(files) == 1:
                                result.append(line)
                            else:
                                result.append(file_name + "-" + line)
                        else:
                            num_strings -= 1

            except FileNotFoundError:
                execution_status.add_error(f"Can't open file {file_name}")
                return

        execution_status.provide_output("\n".join(result))
        return


class ExternalCommand(Operation):
    @staticmethod
    def execute(*args, execution_status):
        command_name = args[0]
        command_args = args[1:]
        # Пробуем запустить процесс в терминале.
        # Для запуска годятся лишь процессы, от которых не ловим output (vim, nano, ...).
        # Если это делать (например, с помощью записи во временный файл, который создаем в питоне, с помощью команды
        # command | tee temp_file), то мы поймаем output, но не понятно, когда его надо выводить. И это самая
        # большая проблема, т.к. после запуска vim есть в output почти все служебная информация.
        # Нельзя просто так всегда брать и печатать все; надо проверять, но не понятно, как. Поэтому решил, что
        # самым разумным будет не ловить output вообще, ведь именно не консольные процессы (типа vim) нас
        # и интересуют.
        process = subprocess.run([f"{command_name}", *command_args], shell=True, stderr=subprocess.PIPE)
        status = process.stderr.decode('utf-8') or ""

        pattern = re.compile(f".+? {command_name}: not found\n")
        if pattern.match(status):
            execution_status.add_error(f"Command \"{command_name}\" wasn't found")
        elif status:
            execution_status.add_error("Error while running command in external terminal:\n" + status)
        return


class OperationExecutor:
    """
    Класс отвечает за выполнение переданной в текстовом виде команды.
    """

    operations_dict = {"echo": Echo,
                       "pwd": Pwd,
                       "cat": Cat,
                       "wc": Wc,
                       "exit": Exit,
                       "grep": Grep,
                       "ls": Ls,
                       "cd": Cd}

    def __init__(self):
        pass

    @staticmethod
    def execute_operation(*args, command_name, execution_status):
        if command_name in OperationExecutor.operations_dict:
            OperationExecutor.operations_dict[command_name].execute(*args, execution_status=execution_status)
            return
        else:
            ExternalCommand.execute(command_name, *args, execution_status=execution_status)
