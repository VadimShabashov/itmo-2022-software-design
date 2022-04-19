from src.operations.operation import Operation


class Echo(Operation):
    @staticmethod
    def execute(*args, execution_status):
        execution_status.provide_output(" ".join(args))
