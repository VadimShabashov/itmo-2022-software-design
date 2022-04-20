class Parser:
    """
    Класс отвечает за распарсивание переданной строки.
    """

    def __init__(self, default_dict=None):
        # Словарь по умолчанию будет полезен при тестировании
        if default_dict:
            self.variables = default_dict
        else:
            self.variables = {}

    def substitute_variables(self, string):
        """
        Функция заменяет $name на значение name из словаря. Если его нет, то возвращает пустую строку.
        """
        if string[1:] in self.variables:
            return self.variables[string[1:]]
        else:
            return ""

    @staticmethod
    def check_assignments(parsed_string):
        """
        Функция проверит, что: либо все команды - присваивания, либо есть хотя бы одно неприсваивание или пайплайн.
        """
        return (len(parsed_string) == 1) and \
            all(status for pipeline in parsed_string for (_, status) in pipeline)

    @staticmethod
    def eliminate_assignments(parsed_string):
        """
        В каждом пайплайне все присваивания до команд игнорируются и выкидываются, а все присваивания
        после команд остаются, т.к. могут быть проинтерпретированы как строки.
        """

        processed_parsed_string = []

        for pipeline in parsed_string:
            # Удаляем все присваивания, пока не получим первое неприсваивание в пайплайне
            pipeline_status = True
            processed_parsed_string.append([])

            for (word, status) in pipeline:
                pipeline_status = pipeline_status and status

                if pipeline_status:
                    pass
                else:
                    processed_parsed_string[-1].append(word)

        return processed_parsed_string

    def apply_assignments(self, parsed_string):
        """
        Применяем присваивания, если выполнен предикат check_assignments
        """
        assignment_status = self.check_assignments(parsed_string)
        if assignment_status:
            for expression in [word for pipeline in parsed_string for (word, _) in pipeline]:
                # Т.к. первый знак равенства отвечает за присваивание
                var_name, var_value = expression.split("=", maxsplit=1)
                self.variables[var_name] = var_value

            return [[]]  # Т.к. выполнили все присваивания, а больше команд не осталось

        else:
            processed_string = self.eliminate_assignments(parsed_string)
            return processed_string

    def parse(self, input_string):
        parsed_string = [[]]
        parsed_word = []  # Слово, которое парсим в данный момент
        substituted_word = []  # Слово, начавшееся с $, и в котором поэтому будем делать замену
        quote = ""  # Статус открытой кавычки ("" - если ни одна не открыта; также бывает "'" и """)
        substitution = False

        # Проверка, что слово представляет собой присваивание вида name=что-то.
        # 0, когда пока не знаем; -1, когда точно нельзя; 1, когда точно можно
        assignment_word = 0

        for char in input_string:
            # Проверка, что слово - присваивание
            if (assignment_word != 1) and (char in "$\'\"| "):
                assignment_word = -1
            elif (assignment_word != -1) and (char == "="):
                assignment_word = 1

            # Парсинг специальных знаков
            if (char == "$") and (quote != "\'"):
                if substitution:
                    parsed_word.append(self.substitute_variables("".join(substituted_word)))
                    substituted_word = []

                substitution = True

            elif char in "=\'\"| ":
                # Делаем замену, т.к. char обрывает имя
                if substitution:
                    parsed_word.append(self.substitute_variables("".join(substituted_word)))
                    substituted_word = []
                    substitution = False

                # Определяем, что делать в случае специальных символов: кавычки, |, и пробел
                if char == "\'":
                    if quote == "\'":
                        quote = ""
                        continue
                    elif quote == "\"":
                        pass
                    else:
                        quote = "\'"
                        continue

                elif char == "\"":
                    if quote == "\"":
                        quote = ""
                        continue
                    elif quote == "\'":
                        pass
                    else:
                        quote = "\""
                        continue

                elif char in "| ":
                    if (quote != "\'") and (quote != "\""):
                        if parsed_word:
                            parsed_string[-1].append(("".join(parsed_word), assignment_word == 1))
                            parsed_word = []

                        if char == "|":
                            parsed_string.append([])

                        assignment_word = 0
                        continue

            # Либо увеличиваем имя переменной для замены, либо добавляем в общее слово
            if substitution:
                substituted_word.append(char)
            else:
                parsed_word.append(char)

        # Если строка кончилась, на $..., то делаем эту замену
        if substitution:
            parsed_word.append(self.substitute_variables("".join(substituted_word)))

        if parsed_word:
            parsed_string[-1].append(("".join(parsed_word), assignment_word == 1))

        if quote != "":
            return [[]], f"Quote {quote} wasn't closed"
        elif (len(parsed_string) > 1) and any(len(pipe) == 0 for pipe in parsed_string):
            return [[]], "Empty pipe was provided"
        else:
            return self.apply_assignments(parsed_string), ""
