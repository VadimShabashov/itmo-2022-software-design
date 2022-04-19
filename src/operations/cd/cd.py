import os
from pathlib import Path

from src.operations.operation import Operation


class Cd(Operation):
    @staticmethod
    def execute(*args, execution_status, current_directory=None):
        list_args = list(args)
        if len(list_args) > 1:
            execution_status.add_error("ls get only zero or one argument")
            return

        if len(list_args) == 0:
            os.chdir(str(Path.home()))
            return

        path = list_args[0]
        try:
            os.chdir(path)
        except FileNotFoundError:
            execution_status.add_error(f"cd: {path}: No such file or directory")
