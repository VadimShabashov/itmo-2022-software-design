import sys

from src.operations.operation import Operation


class Wc(Operation):
    @staticmethod
    def process_stdin(execution_status):
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

        execution_status.provide_output(" ".join(str(s) for s in statistics))

    @staticmethod
    def process_files(args, execution_status):
        outputs = []
        statistics_total = [0, 0, 0]
        for file_name in args:
            statistics = [0, 0, 0]

            try:
                with open(file_name) as file:
                    file_text = file.read()
            except FileNotFoundError:
                execution_status.add_error(f"wc: {file_name}: No such file or directory")
                continue

            for line in file_text.splitlines():
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

    @staticmethod
    def execute(*args, execution_status):
        # Либо читаем из stdin, либо из файлов
        if len(args) == 0:
            Wc.process_stdin(execution_status=execution_status)
        else:
            Wc.process_files(args, execution_status=execution_status)
