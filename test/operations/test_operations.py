from src.operations.operations import Echo
from src.operations.operations import Grep
from src.operations.operations import Ls
from src.operations.operations import Cd
from src.operations.operations import Pwd


def test_echo():
    echo = Echo()
    assert echo.execute("Hello world!", "Hello!", prev_output="Goodbye world!") == ("Hello world! Hello!", "")
    assert echo.execute(prev_output="Only prev_output") == ("", "")


def test_ls():
    ls = Ls()
    out_dir = "./test/operations/test_ls"
    inner_dir = "./test/operations/test_ls/inner_dir"

    res_out, err = ls.execute(out_dir, prev_output="never mind")
    assert (set(res_out.replace("\n", " ").replace("  ", " ").split(" ")), err) ==\
           ({"inner_dir", "in1.txt", "in2.txt"}, "")

    res_inner, err = ls.execute(inner_dir, prev_output="never mind")
    assert (set(res_inner.replace("\n", " ").replace("  ", " ").split(" ")), err) ==\
           ({"in3.txt", "in4.txt", "in5.txt"}, "")


def test_cd():
    import os
    cd = Cd()
    start_dir = os.getcwd()
    cur_dir = "./test/operations/test_ls/"
    prev_cur_dir = "./test/operations/"

    cd.execute(cur_dir, prev_output="never mind")
    new_dir = os.path.abspath(os.path.basename(cur_dir))
    assert os.path.abspath(os.getcwd()) == new_dir

    cd.execute("..", prev_output="never mind")
    new_dir = os.path.abspath(os.path.basename(prev_cur_dir))
    assert os.path.abspath(os.getcwd()) == new_dir

    cd.execute(".", prev_output="never mind")
    new_dir = os.path.abspath(os.path.basename(prev_cur_dir))
    assert os.path.abspath(os.getcwd()) == new_dir

    cd.execute(start_dir, prev_output="never mind")


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
