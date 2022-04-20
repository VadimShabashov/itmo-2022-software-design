from src.operations.execution_status.execution_status import ExecutionStatus
from src.operations.operation_executor import Grep


class TestGrep:
    grep = Grep()

    def test_grep_without_flags(self):
        execution_status = ExecutionStatus()

        expected_output = "dogs are lame and cats are great"
        self.grep.execute('cats', './test/operations/resources/grep/1.txt', execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_grep_with_i_flag(self):
        execution_status = ExecutionStatus()

        expected_output = ("Cats everywhere!\n"
                           "CatsDogs cool\n"
                           "dogs are lame and cats are great")
        self.grep.execute('-i', 'cats', './test/operations/resources/grep/1.txt', execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_grep_with_w_flag(self):
        execution_status = ExecutionStatus()

        expected_output = "dogs are lame and cats are great"
        self.grep.execute('-w', 'cats', './test/operations/resources/grep/1.txt', execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_grep_with_A_flag(self):
        execution_status = ExecutionStatus()

        expected_output = ("ds cats everywhere!\n"
                           "What rg if cat was the king\n"
                           ".\n"
                           "--\n"
                           "dogs are lame and cats are great")
        self.grep.execute('-A', '2', 'cats', './test/operations/resources/grep/2.txt', execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_grep_all_flags(self):
        execution_status = ExecutionStatus()

        expected_output = ("Cats everywhere!\n"
                           "What if cat was the king\n"
                           "."
                           "\n"
                           "."
                           "\n."
                           "\n"
                           "--\n"
                           "dogs are lame and cats are great")
        self.grep.execute('-iwA', '4', 'cats',
                          './test/operations/resources/grep/1.txt',
                          execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors

    def test_grep_several_files(self):
        execution_status = ExecutionStatus()
        expected_output = ("./test/operations/resources/grep/1.txt:Cats everywhere!\n"
                           "./test/operations/resources/grep/1.txt-What if cat was the king\n"
                           "./test/operations/resources/grep/1.txt-.\n--\n"
                           "./test/operations/resources/grep/1.txt:CatsDogs cool\n"
                           "./test/operations/resources/grep/1.txt:dogs are lame and cats are great\n--\n"
                           "./test/operations/resources/grep/2.txt:ds cats everywhere!\n"
                           "./test/operations/resources/grep/2.txt-What rg if cat was the king\n"
                           "./test/operations/resources/grep/2.txt-.\n--\n"
                           "./test/operations/resources/grep/2.txt:rgrg CatsDogs cool\n"
                           "./test/operations/resources/grep/2.txt:dogs are lame and cats are great")
        self.grep.execute("-iA", "2", "cats", "./test/operations/resources/grep/1.txt",
                          "./test/operations/resources/grep/2.txt", execution_status=execution_status)
        assert execution_status.output == expected_output
        assert not execution_status.errors
