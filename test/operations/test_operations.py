from src.operations.operations import Echo
from src.operations.operations import Grep


def test_echo():
    echo = Echo()
    assert echo.execute("Hello world!", "Hello!", prev_output="Goodbye world!") == ("Hello world! Hello!", "")
    assert echo.execute(prev_output="Only prev_output") == ("", "")


def test_grep(monkeypatch):
    grep = Grep()

    expected_output1 = ("Cats everywhere!\nWhat if cat was the king\n.\n.\n.\n--\ndogs are lame and cats are great", "")
    obtained_output1 = grep.execute('-iwA', '4', 'cats', './test/operations/test_grep/1.txt', prev_output="")
    assert obtained_output1 == expected_output1

    expected_output2 = ("./test/operations/test_grep/1.txt:Cats everywhere!\n"
                        "./test/operations/test_grep/1.txt-What if cat was the king\n"
                        "./test/operations/test_grep/1.txt-.\n--\n"
                        "./test/operations/test_grep/1.txt:CatsDogs cool\n"
                        "./test/operations/test_grep/1.txt:dogs are lame and cats are great\n--\n"
                        "./test/operations/test_grep/2.txt:ds cats everywhere!\n"
                        "./test/operations/test_grep/2.txt-What rg if cat was the king\n"
                        "./test/operations/test_grep/2.txt-.\n--\n"
                        "./test/operations/test_grep/2.txt:rgrg CatsDogs cool\n"
                        "./test/operations/test_grep/2.txt:dogs are lame and cats are great", "")
    obtained_output2 = grep.execute("-iA", "2", "cats", "./test/operations/test_grep/1.txt",
                                    "./test/operations/test_grep/2.txt", prev_output="")
    assert obtained_output2 == expected_output2
