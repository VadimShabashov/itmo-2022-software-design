from src.operations.operation import Operation


class Exit(Operation):
    @staticmethod
    def execute(*args, execution_status):
        execution_status.do_exit()
