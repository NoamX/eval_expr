import sys
import re


def converter(string: str):
    try:
        return int(string)
    except ValueError:
        to_remove = string.find('.')
        if to_remove > 0:
            decimal = string[to_remove:]
            if len(decimal) == 2:
                return int(string[:to_remove])

        to_remove = string.find('e')
        if to_remove > 0:
            return float('{:.15f}'.format(float(string[:to_remove])))
        elif len(string) >= 15:
            return float('{:.15f}'.format(float(string)))

        return float(string)


class Main:
    def __init__(self, expr: str = 'None'):
        self.expr = expr

    def eval(self):
        return self.get_parentheses(self.expr)

    def get_parentheses(self, expr: str):
        p_open = expr.rfind('(')
        if p_open >= 0:
            # print('Expression :', expr)
            p_close = expr.find(')', p_open)
            in_p = expr[p_open + 1:p_close]

            # print('In parentheses :', in_p)

            new_expr = expr.replace('({})'.format(
                in_p), self.eval_high_priority(in_p))

            if new_expr.find('(') >= 0:
                return self.get_parentheses(new_expr)
            else:
                return self.eval_high_priority(new_expr)
        else:
            return self.eval_high_priority(expr)

    def eval_high_priority(self, expr: str):
        if re.search('[*/%]', expr):
            # print('Expression :', expr)
            op_pos = re.search('[*/%]', expr).span()[0]

            rest_l = None
            rest_r = None
            if re.search('[+-]', expr[1:]):
                if re.search('[+-]', expr[1:]).span()[0] - 1 != op_pos:
                    for match in re.finditer('[+-]', expr):
                        rest_pos = match.span()[1]
                        if rest_pos < op_pos:
                            rest_l = rest_pos
                        else:
                            rest_r = rest_pos - 1

            to_eval = expr[rest_l:rest_r]
            # print('To Eval :', to_eval)

            old_op_pos = None
            if re.search('[*/%]', to_eval):
                old_op_pos = re.search('[*/%]', to_eval).span()[0]

            left = to_eval[:old_op_pos]

            if re.search('[+-]', left[1:]):
                next_op_pos = re.search('[+-]', left[1:]).span()[1]
                left = left[next_op_pos:]

            op = to_eval[old_op_pos]
            right = to_eval[old_op_pos + 1:]

            rest = ''
            if re.search('[+\-*/%]', right[1:]):
                next_op_pos = re.search('[+\-*/%]', right[1:]).span()[1]
                rest = right[next_op_pos:]
                right = right[:next_op_pos]

            res = None
            if op == '*':
                res = str(converter(left) * converter(right))
            if op == '/':
                res = str(converter(left) / converter(right))
            if op == '%':
                res = str(converter(left) % converter(right))

            # print('Result :', res)

            new_expr = expr.replace(to_eval, res + rest, 1)

            if re.search('[*/%]', new_expr):
                return self.eval_high_priority(new_expr)
            else:
                return self.eval_low_priority(new_expr)
        else:
            return self.eval_low_priority(expr)

    def eval_low_priority(self, expr: str):
        if re.search('[+-]', expr[1:]):
            # print('Expression :', expr)
            op_pos = re.search('[+-]', expr[1:]).span()[1]

            left = expr[:op_pos]
            op = expr[op_pos]
            right = expr[op_pos + 1:]

            if re.search('[+-]', right[1:]):
                next_op_pos = re.search('[+-]', right[1:]).span()[1]
                right = right[:next_op_pos]

            to_eval = left + op + right
            # print('To Eval :', to_eval)

            res = None
            if op == '+':
                res = str(converter(left) + converter(right))
            if op == '-':
                res = str(converter(left) - converter(right))

            # print('Result :', res)

            new_expr = expr.replace(to_eval, res, 1)

            if re.search('[+-]', new_expr[1:]):
                return self.eval_low_priority(new_expr)
            else:
                return new_expr
        return expr


main = Main(sys.argv[1])
# main = Main("(3+5)*2")
# main = Main("(3+5)*(4-7)")
# main = Main("1+1")
# main = Main("3%2%2")
# main = Main("3*2/2")
# main = Main("3*2/2*4")
# main = Main("3*2/-2*4")
# main = Main("3.5*2/2")
# main = Main("42")
# main = Main("(42)")
# main = Main("((42))")
# main = Main("(42)*2")
# main = Main("(((3+5/2)))*2")
# main = Main("((3.343*5.454-4.54*7)/1.006+1)-1.055/((8.0434*834343.44)+3.433)%2")  # : -12.4664792825
# main = Main("((3*5-4*7)/1+1)-1/((8*8)+3)%2")
# main = Main("1+100-90*2/13%2+3405%565")
# main = Main("90*2/13%2")
# main = Main("2^8")  # to add
# main = Main("-1+2-1")
# main = Main("-1--1--1--1--1")
# main = Main("-1+-1")
# main = Main("-1-1")
# main = Main("1+1-1*3/2*(3+431+34/43*67%2)/1-1+1")
print(main.eval())
