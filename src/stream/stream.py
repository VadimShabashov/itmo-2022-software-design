import sys


class Stream:
    def __init__(self, input_stream, output_stream):
        self.input_stream = input_stream
        self.output_stream = output_stream

    def welcome(self):
        if self.input_stream == sys.stdin:
            print("Bash is started. Welcome back, sir/madame!")

    def goodbye(self):
        if self.input_stream == sys.stdin:
            print("Bash is terminated. Good day, sir/madame!")

    def write_string(self, string):
        self.output_stream.write(string)
        self.output_stream.write("\n")

    def write_execution_status(self, execution_status):
        for error in execution_status.errors:
            self.write_string(error)

        if execution_status.output is not None:
            self.write_string(execution_status.output)

    def read(self):
        if self.input_stream == sys.stdin:
            return input(">>> ")
        else:
            return self.input_stream.readline().rstrip()
