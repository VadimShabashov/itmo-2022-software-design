class Operation:
    """
    Этот класс играет роль интерфейса, от которого наследуются все операторы bash.
    Операторы переопределяют метод execute.
    """

    @staticmethod
    def execute(*args, execution_status):
        pass
