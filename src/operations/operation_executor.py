from src.operations.cat.cat import Cat
from src.operations.cd.cd import Cd
from src.operations.echo.echo import Echo
from src.operations.exit.exit import Exit
from src.operations.external_command.external_command import ExternalCommand
from src.operations.grep.grep import Grep
from src.operations.ls.ls import Ls
from src.operations.pwd.pwd import Pwd
from src.operations.wc.wc import Wc


class OperationExecutor:
    """
    Класс отвечает за передачу выполнения текстовой команды конкретному классу.
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
        else:
            ExternalCommand.execute(*args, command_name, execution_status=execution_status)
