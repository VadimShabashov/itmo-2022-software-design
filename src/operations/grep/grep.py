import re

from src.operations.operation import Operation


class Grep(Operation):
    @staticmethod
    def execute(*args, execution_status):  # noqa: C901
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
