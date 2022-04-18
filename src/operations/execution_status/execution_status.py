class ExecutionStatus:
    def __init__(self):
        self.exit = False
        self.prev_output = None
        self.output = None
        self.errors = []

    def make_prev_output(self):
        self.prev_output = self.output
        self.output = None

    def add_error(self, error):
        self.errors.append(error)

    def provide_output(self, output):
        self.output = output

    def do_exit(self):
        self.exit = True

    def undo_exit(self):
        self.exit = False
