import re
def validate_pin(pin):
    return pin == pin.strip() and re.search("^(\d{4}|\d{6})$", pin) is not None



print(validate_pin("1234\n"))
print(validate_pin("1"))