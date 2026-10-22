def calculate(data):
    num1 = float(data['num1'])
    opt = data['opt']
    num2 = float(data['num2'])

    match opt:
        case "+":
            result = num1 + num2
        case "-":
            result = num1 - num2
        case "*":
            result = num1 * num2
        case "/":
            try:
                result = num1 / num2
            except ZeroDivisionError:
                result = 0

    return result
