class RailsCodec:
    """
    WEAREDISCOVEREDFLEEATONCE

    3
    W   E   C   R   L   T   E
     E R D S O E E F E A O C
      A   I   V   D   E   N
    WECRLTEERDSOEEFEAOCAIVDEN

    4
    W     I     R     E     E
     E   D S   E E   E A   C
      A E   C V   D L   T N
       R     O     F     O

    5
    W       C       L       E
     E     S O     F E     C
      A   I   V   D   E   N
       R D     E E     A O
        E       R       T

    6
    W         V         T
     E       O E       A O
      A     C   R     E   N
       R   S     E   E     C
        E I       D L       E
         D         F
    WVTEOEAOACRENRSEECEIDLEDF

    8
    W             D
     E           E F
      A         R   L
       R       E     E
        E     V       E     E
         D   O         A   C
          I C           T N
           S             O
    WDEEFARLREEEVEEDOACICTNSO



    Hello, World!
    2
    H l o _ o l !
     e l , W r d


    eldjbwkiyeipqn
    6
    e         i
     l       e p
      d     y   q
       j   i     n
        b k
         w

    pmiqevjsxgajrdkkpxaffzpsbzaunkdsfbejlrdogdorhy
    5
    p       x       p       b       f       g
     m     s g     k x     s z     s b     o d
      i   j   a   k   a   p   a   d   e   d   o
       q v     j d     f z     u k     j r     r y
        e       r       f       n       l       h

    krtjqgpkbrjhny
    8
    k
     r           y
      t         n
       j       h
        q     j
         g   r
          p b
           k
    krytnjhqjgrpbk
    """

    @staticmethod
    def transform_position(pos, length, n):
        num_valleys = length // (n * 2 - 2)
        valley_num = pos // (n * 2 - 2)
        valley_pos = pos % (n * 2 - 2)
        last_valley_pos = (length - 1) % (n * 2 - 2)
        last_hill, last_rail_num = RailsCodec.rail_num(n, last_valley_pos)
        extra_tail = 0
        if last_valley_pos and not last_hill:
            extra_tail = 1
        if last_hill:
            if (length + last_rail_num) // (n * 2 - 2) != num_valleys:
                extra_tail = 0
                num_valleys += 1

        if valley_pos == n - 1:  # we are the bottom
            encoded_pos = length - num_valleys + 1 + valley_num - 1
        elif valley_pos == 0:  # we are the top
            encoded_pos = valley_num
        else:
            hill, rail_num = RailsCodec.rail_num(n, valley_pos)
            missing_tail = 0
            add_extra_tail = 0
            if extra_tail:
                add_extra_tail = min(rail_num - 1, last_rail_num)
            else:
                missing_tail = min(rail_num, last_rail_num)

            encoded_pos = num_valleys + 1 + (rail_num - 1) * num_valleys * 2 + add_extra_tail + valley_num * 2 + hill - missing_tail

        return encoded_pos

    @staticmethod
    def rail_num(n, valley_pos):
        if valley_pos < n - 1:
            rail_num = valley_pos
            hill = 0
        else:
            rail_num = (n - 1) - (valley_pos - (n - 1))
            hill = 1
        return hill, rail_num

    @staticmethod
    def enc(string, n):
        length = len(string)
        encoded = ["_"] * length
        for i in range(length):
            encpos = RailsCodec.transform_position(i, length, n)
            encoded[encpos] = string[i]
        return "".join(encoded)

    @staticmethod
    def dec(string, n):
        length = len(string)
        decoded = ["_"] * length
        for i in range(length):
            decpos = RailsCodec.transform_position(i, length, n)
            decoded[i] = string[decpos]
        return "".join(decoded)


def encode_rail_fence_cipher(string, n):
    return RailsCodec.enc(string, n)


def decode_rail_fence_cipher(string, n):
    return RailsCodec.dec(string, n)


tests = [
    ("WEAREDISCOVEREDFLEEATONCE", 3, "WECRLTEERDSOEEFEAOCAIVDEN"),
    ("WEAREDISCOVEREDFLEEATONCE", 4, "WECRLTEERDSOEEFEAOCAIVDEN"),
    ("WEAREDISCOVEREDFLEEATONCE", 5, "WECRLTEERDSOEEFEAOCAIVDEN"),
    ("WEAREDISCOVEREDFLEEATONCE", 6, "WVTEOEAOACRENRSEECEIDLEDF"),
    ("WEAREDISCOVEREDFLEEATONCE", 8, "WDEEFARLREEEVEEDOACICTNSO"),
    ("Hello, World!", 2, "Hlo ol!el,Wrd"),
    ("pmiqevjsxgajrdkkpxaffzpsbzaunkdsfbejlrdogdorhy", 5, "pxpbfgmsgkxszsbodijakapadedoqvjdfzukjrryerfnlh"),
    ("eldjbwkiyeipqn", 6, "eilepdyqjinbkw"),
    ("krtjqgpkbrjhny", 8, "krytnjhqjgrpbk")
]

print("encode")
for a in tests:
    print(a[0], '[', a[1], ']=', encode_rail_fence_cipher(a[0], a[1]), ' (', a[2], ')')

print("decode")
for a in tests:
    print(a[2], '[', a[1], ']=', decode_rail_fence_cipher(a[2], a[1]), ' (', a[0], ')')
exit()

tests2 = [
    ("WEAREDISCOVEREDFLEEATONCE", 3, "WECRLTEERDSOEEFEAOCAIVDEN", 6),
    ("WEAREDISCOVEREDFLEEATONCE", 4, "WECRLTEERDSOEEFEAOCAIVDEN", 4),
    ("WEAREDISCOVEREDFLEEATONCE", 5, "WECRLTEERDSOEEFEAOCAIVDEN", 3),
    ("WEAREDISCOVEREDFLEEATONCE", 6, "WVTEOEAOACRENRSEECEIDLEDF", 2),
    ("WEAREDISCOVEREDFLEEA", 6, "WVTEOEAOACRENRSEECEIDLEDF", 0),
    ("WEAREDISCOVEREDFLEE", 6, "WVTEOEAOACRENRSEECEIDLEDF", 0),
    ("WEAREDISCOVEREDF", 6, "WVTEOEAOACRENRSEECEIDLEDF", 0),
    ("WEAREDISCOVERE", 6, "WVTEOEAOACRENRSEECEIDLEDF", 0),
    ("WEAREDISCOVEREDFLEEATONCE", 8, "WDEEFARLREEEVEEDOACICTNSO", 2),
    ("WEAREDISCOVEREDFLEEATO", 8, "WDEEFARLREEEVEEDOACICTNSO", 2),
    ("WEAREDISCOVEREDFLEEAT", 8, "WDEEFARLREEEVEEDOACICTNSO", 1),
    ("Hello, World!", 2, "Hlo ol!el,Wrd",6),
    ("pmiqevjsxgajrdkkpxaffzpsbzaunkdsfbejlrdogdorhy", 5, "pxpbfgmsgkxszsbodijakapadedoqvjdfzukjrryerfnlh", 0),
    ("", 3, "", 0),
    ("eldjbwkiyeipqn", 6, "eilepdyqjinbkw", 1)
]

for t2 in tests2:
    length = len(t2[0])
    n = t2[1]
    num_valleys = length // (n * 2 - 2)
    last_valley_pos = (length - 1) % (n * 2 - 2)
    last_hill, last_rail_num = RailsCodec.rail_num(n, last_valley_pos)
    if last_hill:
        if (length + last_rail_num) // (n*2 - 2) != num_valleys:
            num_valleys += 1
    print(t2[0], '[',length, ' // ',n, '] -- ', num_valleys, ' , ', t2[3], ' -- last: <',last_valley_pos,',',last_rail_num,',',last_hill,'>')
