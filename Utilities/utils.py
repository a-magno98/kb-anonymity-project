import sys

#try to convert string to value, otherwise throw an exception 
def string_toValue(value: str, raise_ex=False):
    try:
        return int(value)
    except ValueError:
        return ValueError
            
#try to convert value to string, otherwise throw an exception
def value_toString(value: int):
    try:
        return str(value)
    except ValueError:
        return ValueError

#prints a log message
def _log(content, enabled=True, endl=True):
    if enabled:
        if endl:
            print(content)
        else:
            sys.stdout.write('\r' + content)
