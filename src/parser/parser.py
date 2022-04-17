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
        Функция заменяет $name на значение name из словаря. Если его нет, то возвращает $name.
        """
        if string[1:] in self.variables:
            return self.variables[string[1:]]
        else:
            return string

    @staticmethod
    def check_assignments(parsed_string):
        """
        Функция проверит, что: либо все команды - присваивания, либо есть хотя бы одно неприсваивание или пайплайн.
        Во втором случае в каждом пайплайне все присваивания до команд игнорируются и выкидываются, а все присваивания
        после команд остаются, т.к. могут быть проинтерпретированы как строки.
        """
        assignment_status = (len(parsed_string) == 1) and \
                             all(status for pipeline in parsed_string for (_, status) in pipeline)

        if not assignment_status:
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

            return processed_parsed_string, assignment_status
        else:
            return [[word for pipeline in parsed_string for (word, _) in pipeline]], assignment_status

    def parse(self, input_string):
        parsed_string = [[]]
        parsed_word = []
        substituted_word = []
        quote = ""
        substitution = ""

        # Проверка, что каждое слово представляет собой присваивание вида name=что-то.
        # 0, когда может можно, но еще не получили; -1, когда точно нельзя; 1, когда точно можно
        assignment_word = 0

        for char in input_string:
            # Проверка, что каждое слово - присваивание
            if (assignment_word != 1) and (char in "$\'\"| "):
                assignment_word = -1
            elif (assignment_word != -1) and (char == "="):
                assignment_word = True

            # Парсинг специальных знаков
            if (char == "$") and (quote != "\'"):
                substitution = "$"
            elif char in "=\'\"| ":
                # Делаем замену, т.к. char обрывает имя
                if substitution == "$":
                    parsed_word.append(self.substitute_variables("".join(substituted_word)))
                    substituted_word = []
                    substitution = ""

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
            if substitution == "$":
                substituted_word.append(char)
            else:
                parsed_word.append(char)

        # Если строка кончилась, на $..., то делаем эту замену
        if substitution == "$":
            parsed_word.append(self.substitute_variables("".join(substituted_word)))

        parsed_string[-1].append(("".join(parsed_word), assignment_word == 1))

        return self.check_assignments(parsed_string)
