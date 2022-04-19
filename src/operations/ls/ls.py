from src.operations.operation import Operation


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
