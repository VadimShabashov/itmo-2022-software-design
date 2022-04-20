from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Cat


class TestCat:
    cat = Cat()

    def test_cat_previous_output(self):
        execution_status = ExecutionStatus()
        text = ("Cats around\n"
                "and it's amazing\n"
                "!!!")
        execution_status.provide_output(text)
        self.cat.execute(execution_status=execution_status)
        assert execution_status.output == text

    def test_cat_empty(self):
        execution_status = ExecutionStatus()
        self.cat.execute(execution_status=execution_status)
        assert execution_status.output is None
        assert execution_status.errors == ["Command \"cat\" got zero arguments"]

    def test_cat_existing_files(self):
        execution_status = ExecutionStatus()
        texts = []
        resources_dir = "./test/operations/resources/cat/"
        file_names = ["text1.txt", "text2.txt", "text3.txt"]
        files_path = []
        for file_name in file_names:
            file_path = resources_dir + file_name
            files_path.append(file_path)

            with open(file_path, "r") as file:
                texts.append(file.read())

        self.cat.execute(*files_path, execution_status=execution_status)
        assert execution_status.output == "\n".join(texts)
        assert not execution_status.errors

    def test_cat_nonexistent_files(self):
        execution_status = ExecutionStatus()
        file_name = "nonexistent_file.txt"

        self.cat.execute(file_name, execution_status=execution_status)
        assert execution_status.output is None
        assert execution_status.errors == [f"cat: {file_name}: No such file or directory"]
