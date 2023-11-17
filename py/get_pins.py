def get_pins(observed):
    pin = [int(x) for x in observed]
    # print('pin=', pin)
    expansion = [[0, 8], [4, 2, 1], [5, 3, 2, 1], [6, 3, 2], [7, 5, 4, 1], [8, 6, 5, 4, 2], [9, 6, 5, 3], [8, 7, 4],
                 [0, 9, 8, 7, 5], [9, 8, 6]]
    init_stack = list(map(lambda x: len(expansion[x]) - 1, pin))
    stack = init_stack.copy()

    ret = []

    k = 0
    stack[k] = stack[k] + 1
    while k < len(pin):
        stack[k] = stack[k] - 1
        if stack[k] < 0:
            stack[k] = init_stack[k]
            k = k + 1
            continue
        current_pin = [expansion[x][stack[i]] for i, x in enumerate(pin)]
        # print('current_pin=', current_pin)
        # print('stack,k=', stack, k)
        k = 0

        ret.append("".join(list(map(lambda x: str(x), current_pin))))

    return ret


print(sorted(list(map(lambda x: "".join(x), get_pins("11")))))
