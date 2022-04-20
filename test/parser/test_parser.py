from src.parser.parser import Parser


class TestParser:
    parser = Parser({"a": '3', "b": '2'})

    def test_parser_quotes(self):
        # Правильно парсятся вложенные скобки
        parsed_string, parse_status = self.parser.parse("echo \'\"cats\"\' \"\'dogs\'\"")
        assert parsed_string == [['echo', '\"cats\"', '\'dogs\'']]
        assert not parse_status

    def test_parser_spaces(self):
        # Правильно парсятся пробелы (убираются)
        parsed_string, parse_status = self.parser.parse("echo    1 2     3")
        assert parsed_string == [['echo', '1', '2', '3']]
        assert not parse_status

    def test_parser_non_assignment(self):
        # Нет неправильных присваиваний
        parsed_string, parse_status = self.parser.parse("echo a=\'a=8\'")
        assert parsed_string == [['echo', 'a=a=8']]
        assert not parse_status

    def test_parser_substitution_nested_quotes(self):
        # Правильно подставляются значения
        parsed_string, parse_status = self.parser.parse("echo \"$a\'$a\'\"")
        assert parsed_string == [['echo', '3\'3\'']]
        assert not parse_status

    def test_parser_substitution_double_quotes(self):
        # Правильно подставляются значения
        parsed_string, parse_status = self.parser.parse("echo $a\"$a\"")
        assert parsed_string == [['echo', '33']]
        assert not parse_status

    def test_parser_substitution_nested_quotes_reverse_order(self):
        # Правильно подставляются значения
        parsed_string, parse_status = self.parser.parse("echo '\"$a\"\'")
        assert parsed_string == [['echo', '\"$a\"']]
        assert not parse_status

    def test_parser_substitution_before_assignment(self):
        # Правильно подставляются значения
        parsed_string, parse_status = self.parser.parse("echo $a=4")
        assert parsed_string == [['echo', '3=4']]
        assert not parse_status

    def test_parser_substitution_after_assignment(self):
        # Правильно подставляются значения
        parsed_string, parse_status = self.parser.parse("echo a=$b")
        assert parsed_string == [['echo', 'a=2']]
        assert not parse_status

    def test_parser_simple_pipeline(self):
        parsed_string, parse_status = self.parser.parse("\'$a\'=$a|pwd \"$b\"")
        assert parsed_string == [['$a=3'], ['pwd', '2']]
        assert not parse_status

    def test_parser_pipeline_assignments(self):
        # Пайплайн с равенствами
        parsed_string, parse_status = self.parser.parse("a=4 | b=10|echo   \"cats| wow\"")
        assert parsed_string == [[], [], ['echo', 'cats| wow']]
        assert not parse_status

    def test_parser_unclosed_double_quote(self):
        parsed_string, parse_status = self.parser.parse("echo \"x + cats")
        assert parsed_string == [[]]
        assert parse_status == f"Quote \" wasn't closed"

    def test_parser_unclosed_single_quote(self):
        parsed_string, parse_status = self.parser.parse("echo \'x + cats")
        assert parsed_string == [[]]
        assert parse_status == f"Quote \' wasn't closed"

    def test_parser_empty_pipe(self):
        parsed_string, parse_status = self.parser.parse("echo cats | ")
        assert parsed_string == [[]]
        assert parse_status == "Empty pipe was provided"
