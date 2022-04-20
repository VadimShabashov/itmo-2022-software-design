import re

from src.operations.operation import Operation


class Grep(Operation):
    flags_pattern = re.compile(r"-[iwA]*")

    @staticmethod
    def parse_args(*args):
        flag_i = False
        flag_w = False
        flag_A = False
        n = "0"
        word = None
        files = []

        # Ищем флаги
        ind = 0
        while ind < len(args):
            arg = args[ind]

            if not Grep.flags_pattern.match(arg):
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
                    if ind + 1 < len(args):
                        flag_A = True
                        n = args[ind + 1]
                        ind += 1
                    else:
                        n = ""
            ind += 1

        return flag_i, flag_w, flag_A, n, word, files

    @staticmethod
    def check_input(word, files, n, execution_status):
        if not n:
            execution_status.add_error("grep: option requires an argument -- 'A'")
            return
        elif not n.isdigit():
            execution_status.add_error(f"grep: {n}: invalid context length argument")
            return

        if not word:
            execution_status.add_error("No word pattern for search was provided")
            return

        if not files:
            if execution_status.prev_output:
                # Т.к. массив передается по ссылке, то поменяем тот, что снаружи
                files.append(execution_status.prev_output)
            else:
                execution_status.add_error("No files for search were provided")
                return

    @staticmethod
    def get_word_pattern(word, flag_i, flag_w):
        # Составляем регулярное выражение
        if flag_i and flag_w:
            word_pattern = re.compile(rf'(^|\s){word}($|\s)', re.IGNORECASE)
        elif flag_i:
            word_pattern = re.compile(rf'{word}', re.IGNORECASE)
        elif flag_w:
            word_pattern = re.compile(rf'(^|\s){word}($|\s)')
        else:
            word_pattern = re.compile(rf'{word}')

        return word_pattern

    @staticmethod
    def execute(*args, execution_status):
        result = []

        flag_i, flag_w, flag_A, n, word, files = Grep.parse_args(*args)
        Grep.check_input(word, files, n, execution_status)

        if execution_status.errors:
            return

        word_pattern = Grep.get_word_pattern(word, flag_i, flag_w)
        context_length = int(n)

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

                        if word_pattern.search(line):
                            if num_strings < 0 and flag_A:
                                result.append("--")

                            num_strings = context_length
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
                execution_status.add_error(f"grep: {file_name}: No such file or directory")
                return

        execution_status.provide_output("\n".join(result))
