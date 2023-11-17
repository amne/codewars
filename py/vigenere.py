class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.key = [c for c in key]
        self.alphabet = [c for c in alphabet]
        pass

    def enc_char(self, char, textpos):
        if char in self.alphabet:
            return self.alphabet[(self.alphabet.index(char) + self.alphabet.index(self.key[textpos % len(self.key)])) % len(self.alphabet)]
        return char

    def dec_char(self, char, textpos):
        if char in self.alphabet:
            return self.alphabet[(self.alphabet.index(char) - self.alphabet.index(self.key[textpos % len(self.key)])) % len(self.alphabet)]
        return char

    def encode(self, text):
        return ''.join([self.enc_char(c,i) for i, c in enumerate(text)])

    def decode(self, text):
        return ''.join([self.dec_char(c, i) for i, c in enumerate(text)])



abc = "abcdefghijklmnopqrstuvwxyz"
key = "password"
c = VigenereCipher(key, abc)

print(c.enc_char('c', 0))
print(c.encode('codewars'))