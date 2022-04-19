class ExecutionStatus:
    """
    Класс, который передает информацию между командами в пайплайне.
    """
    def __init__(self):
        self.exit = False  # Если команда была exit
        self.prev_output = None  # Вывод предыдущей команды
        self.output = None  # Вывод текущей команды
        self.errors = []  # Ошибки, случившиеся при выполнении текущей команды

    def make_prev_output(self):
        """
        Перемещает текущий вывод в предыдущий. Используется при переходе к следующей команде в пайплайне
        """
        self.prev_output = self.output
        self.output = None

    def add_error(self, error):
        """
        Добавление ошибки
        """
        self.errors.append(error)

    def provide_output(self, output):
        """
        Добавление результата
        """
        self.output = output

    def do_exit(self):
        """
        Установка флага выхода
        """
        self.exit = True

    def undo_exit(self):
        """
        Снятие флага выхода (нужно, если exit был не последним в пайплайне)
        """
        self.exit = False
