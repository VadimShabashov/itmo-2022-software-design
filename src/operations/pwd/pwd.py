import os

from src.operations.operation import Operation


class Pwd(Operation):
    @staticmethod
    def execute(*args, execution_status):
        execution_status.output = os.getcwd()
