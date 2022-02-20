from src.parser.parser import Parser


def test_parse():
    parser = Parser({"a": '3', "b": '2'})

    # Правильно парсятся вложенные скобки
    assert parser.parse("echo \'\"cats\"\' \"\'dogs\'\"") == ([['echo', '\"cats\"', '\'dogs\'']], False)
    # Правильно парсятся пробелы (убираются)
    assert parser.parse("echo    1 2     3") == ([['echo', '1', '2', '3']], False)
    # Нет проблем с равенствами
    assert parser.parse("echo a=\'a=8\'") == ([['echo', 'a=a=8']], False)
    # Правильно подставляются значения
    assert parser.parse("echo \"$a\'$a\'\"") == ([['echo', '3\'3\'']], False)
    assert parser.parse("echo $a\"$a\"") == ([['echo', '33']], False)
    assert parser.parse("echo '\"$a\"\'") == ([['echo', '\"$a\"']], False)
    assert parser.parse("echo \"\'$a\'\"") == ([['echo', '\'3\'']], False)
    assert parser.parse("echo $a=4") == ([['echo', '3=4']], False)
    assert parser.parse("a=$b") == ([['a=2']], True)
    # Пайплайны
    assert parser.parse("a=4 | b=10|echo   \"cats| wow\"") == ([[], [], ['echo', 'cats| wow']], False)
    assert parser.parse("\'$a\'=$a|pwd \"$b\"") == ([['$a=3'], ['pwd', '2']], False)
