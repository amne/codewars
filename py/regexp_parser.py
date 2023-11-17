class RegexParser(object):
    def __init__(self):
        self.expr = None
        self.tokens = ['*', '|', '.', '(', ')']
        self.operators = ['|', '.', '*']

    def parse(self, string):
        pos = 0
        words = []
        current_word = ''
        max_nest_level = 0
        nest_level = 0
        parsing_number = 0
        parsed_numbers = 0
        while pos < len(string):

            # we have something meaningful
            if string[pos] in self.tokens:
                current_word = current_word + string[pos]
                if string[pos] == '(':
                    nest_level = nest_level + 1
                if string[pos] == ')':
                    nest_level = nest_level - 1
                    if nest_level == 0 and parsed_numbers == 0:
                        raise ValueError
                if nest_level > max_nest_level:
                    max_nest_level = nest_level
                if nest_level == 0:
                    if current_word[0] == '(':
                        current_word = current_word[1:-1]
                    words.append(current_word)
                    current_word = ''
                if nest_level < 0:
                    raise ValueError
            else:
                if current_word == '' and string[pos] == '.':
                    raise ValueError
                parsed_numbers = 1
                if nest_level == 0:
                    parsing_number = 1
                current_word = current_word + string[pos]
                # continue
            if parsing_number == 1 and nest_level == 0:
                parsing_number = 0
                words.append(current_word)
                current_word = ''
            pos = pos + 1
        if parsing_number == 1:
            words.append(current_word)
            parsing_number = 0
        if len(words) == 1:
            if max_nest_level > 0:
                return self.parse(words[0])
            else:
                return words[0]
        if nest_level > 0:
            raise ValueError
        return list(map(self.parse, words))

    def reduce(self, words):
        # print('reducing words: ', words)
        if not isinstance(words, list):
            return '' + words + ''
        if len(words) == 0:
            return ''
        if len(words) == 1:
            return self.reduce(words[0])
        operator = ''
        operator_pos = -1
        for op in self.operators:
            if op in words:
                operator = op
                if op in ['|','*']:
                    if words.count('|') > 1:
                        raise ValueError
                    operator_pos = len(words) - list(reversed(words)).index(op) - 1
                else:
                    operator_pos = words.index(op)
                break
        if operator_pos == -1:
            return '(' + ''.join(map(self.reduce, words)) + ')'
        # print('reducing words [', operator_pos, ']: ', words)
        # print('calc: ', words[0:operator_pos], ' ', operator, ' ', words[operator_pos + 1:])
        if operator == '*':
            if operator_pos == 0 or words[operator_pos - 1] == '*':
                raise ValueError
            if operator_pos - 1 > 0:
                return '(' + self.reduce(words[0:operator_pos - 1]) + self.reduce(
                    words[operator_pos - 1:operator_pos]) + operator + ')'
            else:
                return self.reduce(words[operator_pos - 1:operator_pos]) + operator
        if operator == '|':
            return '(' + self.reduce(words[0:operator_pos]) + operator + self.reduce(words[operator_pos + 1:]) + ')'
        if operator == '.':
            return '(' + self.reduce(words[0:operator_pos]) + '.' + self.reduce(words[operator_pos+1:]) + ')'

    def evaluate(self, string):
        try:
            return self.reduce(self.parse(string))
        except ValueError:
            return ''

# print(RegexParser().evaluate("23 + 35"))
# print(RegexParser().evaluate("2 + 3"))
# # print(RegexParser().parse("3 + 4 * 5"))
# print(RegexParser().evaluate("3 + 4 * 5"))
# # print(RegexParser().parse("3 * 4 + 5"))
# print(RegexParser().evaluate("3 * 4 + 5"))
# # print(RegexParser().parse("((3) + (4)) * 5"))
# print(RegexParser().evaluate("((3) + (4)) * 5"))
# print(RegexParser().evaluate("2*(2*(2*(2*1)))"))
# print(RegexParser().evaluate("3 * (4 + 7) - 6"))
# print(RegexParser().parse("(((1)*2))"))
# print(RegexParser().parse("((((((5))))))"))
# print(RegexParser().evaluate("(((1)*2))"))
# print(RegexParser().evaluate("((((((5))))))"))
# print(RegexParser().parse("127"))

# print(RegexParser().parse("2 - 3 - 4"))
# print(RegexParser().evaluate("2 - 3 - 4"))
# print(RegexParser().parse("2 + 3 * 4 / 3 - 6 / 3 * 3 + 8"))
# print(RegexParser().evaluate("2 + 3 * 4 / 3 - 6 / 3 * 3 + 8"))
# print(RegexParser().evaluate("6 / 3 * 3"))
# print(RegexParser().evaluate("6 * 3 / 3"))
# print(RegexParser().evaluate("6/3/2"))


# print(RegexParser().parse("a|b"))
# print(RegexParser().parse("a|b*"))
print(RegexParser().parse("ab*"))
# print(RegexParser().parse("(ab)*"))
# print(RegexParser().parse("(a)*"))
# print(RegexParser().parse("a(b|a)"))
# print(RegexParser().parse("a|b"))
# print(RegexParser().parse('a.*'))
# print(RegexParser().parse(''))
# print(RegexParser().parse('a|t|y'))
print(RegexParser().parse('a**'))

# print(RegexParser().evaluate("a|b"))
# print(RegexParser().evaluate("a|b*"))
print(RegexParser().evaluate("ab*"))
# print(RegexParser().evaluate("(ab)*"))
# print(RegexParser().evaluate("(a)*"))
# print(RegexParser().evaluate("a(b|a)"))
# print(RegexParser().evaluate("a|b"))
# print(RegexParser().evaluate('a.*'))
print(RegexParser().evaluate('a|t|y'))
print(RegexParser().evaluate('a**'))