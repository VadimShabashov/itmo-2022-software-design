import subprocess

from src.operations.operation import Operation


class ExternalCommand(Operation):
    interactive_commands = {"vim", "nano"}

    @staticmethod
    def execute(*args, execution_status):
        command_name = args[-1]
        command_args = args[:-1]

        try:
            if command_name in ExternalCommand.interactive_commands:
                subprocess.run([f"{command_name}", *command_args])
            else:
                process = subprocess.run([f"{command_name}", *command_args], stdout=subprocess.PIPE)
                execution_status.provide_output(process.stdout.decode('utf-8'))
        except OSError as e:
            execution_status.add_error(f"{e.filename}: {e.strerror}")
