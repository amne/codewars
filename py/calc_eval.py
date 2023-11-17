class TreeNode(object):
    def __init__(self):
        self.node = ''
        self.left = None
        self.right = None

    def walk(self):
        pass


class Calculator(object):
    def __init__(self):
        self.expr = None
        self.tokens = ['*', '/', '+', '-', '(', ')']
        self.operators = ['+', '-', '*', '/']

    def parse(self, string):
        pos = 0
        words = []
        current_word = ''
        max_nest_level = 0
        nest_level = 0
        parsing_number = 0
        parsed_numbers = 0
        while pos < len(string):
            if string[pos] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                if current_word == '' and string[pos] == '.':
                    raise ValueError
                parsed_numbers = 1
                if nest_level == 0:
                    parsing_number = 1
                current_word = current_word + string[pos]
                pos = pos + 1
                continue
            if parsing_number == 1 and nest_level == 0:
                parsing_number = 0
                words.append(current_word)
                current_word = ''

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
            pos = pos + 1
        if parsing_number == 1:
            words.append(current_word)
            parsing_number = 0
        if len(words) == 1:
            if max_nest_level > 0:
                return self.parse(words[0])
            else:
                return words[0]
        return list(map(self.parse, words))

    def reduce(self, words):
        # print('reducing words: ', words)
        if not isinstance(words, list):
            return float(words)
        if len(words) == 1:
            return self.reduce(words[0])
        operator = ''
        operator_pos = -1
        for op in self.operators:
            if op in words:
                operator = op
                if op in ['-', '/']:
                    operator_pos = len(words) - list(reversed(words)).index(op) - 1
                else:
                    operator_pos = words.index(op)
                break
        if operator_pos == -1:
            raise ValueError
        # print('reducing words [', operator_pos, ']: ', words)
        # print('calc: ', words[0:operator_pos], ' ', operator, ' ', words[operator_pos + 1:])
        if operator == '+':
            return float(self.reduce(words[0:operator_pos])) + float(self.reduce(words[operator_pos + 1:]))
        if operator == '-':
            return float(self.reduce(words[0:operator_pos])) - float(self.reduce(words[operator_pos + 1:]))
        if operator == '*':
            return float(self.reduce(words[0:operator_pos])) * float(self.reduce(words[operator_pos + 1:]))
        if operator == '/':
            return float(self.reduce(words[0:operator_pos])) / float(self.reduce(words[operator_pos + 1:]))

    def evaluate(self, string):
        return self.reduce(self.parse(string))


# print(Calculator().evaluate("23 + 35"))
# print(Calculator().evaluate("2 + 3"))
# # print(Calculator().parse("3 + 4 * 5"))
# print(Calculator().evaluate("3 + 4 * 5"))
# # print(Calculator().parse("3 * 4 + 5"))
# print(Calculator().evaluate("3 * 4 + 5"))
# # print(Calculator().parse("((3) + (4)) * 5"))
# print(Calculator().evaluate("((3) + (4)) * 5"))
# print(Calculator().evaluate("2*(2*(2*(2*1)))"))
# print(Calculator().evaluate("3 * (4 + 7) - 6"))
# print(Calculator().parse("(((1)*2))"))
# print(Calculator().parse("((((((5))))))"))
# print(Calculator().evaluate("(((1)*2))"))
# print(Calculator().evaluate("((((((5))))))"))
# print(Calculator().parse("127"))

# print(Calculator().parse("2 - 3 - 4"))
print(Calculator().evaluate("2 - 3 - 4"))
# print(Calculator().parse("2 + 3 * 4 / 3 - 6 / 3 * 3 + 8"))
# print(Calculator().evaluate("2 + 3 * 4 / 3 - 6 / 3 * 3 + 8"))
# print(Calculator().evaluate("6 / 3 * 3"))
# print(Calculator().evaluate("6 * 3 / 3"))
print(Calculator().evaluate("6/3/2"))
