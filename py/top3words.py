def top_3_words(text):
    pos = 0
    chars = list(map(chr, range(ord('a'), ord('z')+1))) + list(map(chr, range(ord('A'), ord('Z')+1))) + ["'"]
    current_word = ''
    words = {}

    while pos < len(text):
        # print('text[pos] = "', text[pos], '"')
        if text[pos] in chars:
            current_word = current_word + text[pos]
        else:
            if current_word.strip("'") != '':
                # print('current_word = "', current_word, '"; words=', words)
                if current_word.lower() in words.keys():
                    words[current_word.lower()] = words[current_word.lower()] + 1
                else:
                    words[current_word.lower()] = 1
            current_word = ''
        pos = pos + 1

    if current_word.strip("'") != '':
        # print('current_word = "', current_word, '"; words=', words)
        if current_word.lower() in words.keys():
            words[current_word.lower()] = words[current_word] + 1
        else:
            words[current_word.lower()] = 0

    return list(map(lambda a: a[0], sorted(words.items(), key=lambda x: x[1], reverse=True)))[:3]


# print(top_3_words('a a a b c c d d d d e e e e e'))
print(top_3_words("e e e e DDD ddd DdD: ddd ddd aa aA Aa, bb cc cC e e e"))
