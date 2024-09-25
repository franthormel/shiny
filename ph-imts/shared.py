import locale

def initialize():
    locale.setlocale(locale.LC_ALL, "")

def format_currency(value):
    output = locale.currency(value, grouping=True)
    
    # Formatting a negative value encloses the output string inside parentheses.
    # Remove the parentheses and put the negative sign instead.
    if(output.startswith('(') and output.endswith(')')):
        return f"-{output[1:-1]}"
    
    return output
