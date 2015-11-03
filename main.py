from argparse import ArgumentParser
from mul import Multiplication
from solver import solve


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('col_mult')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False)
    args = parser.parse_args()
    return args.col_mult, args.verbose


def print_env(env):
    s = ""
    counter = 1
    for k in sorted(env["first"].keys()):
        s += "{:>12}".format("X{:02}: {:>5}, ".format(counter, env["first"][k]))
        counter += 1
    for k in sorted(env["second"].keys()):
        s += "{:>12}".format("X{:02}: {:>5}, ".format(counter, env["second"][k]))
        counter += 1
    print s


def parse_col_mult(s):
    separated = s.split("|")
    a1, a2 = separated[0].split(" ")
    rs = separated[1].split(" ")
    return a1, a2, rs, separated[-1]


if __name__ == '__main__':
    col_mult, is_verbose = parse_args()
    first, second, rows, answer = parse_col_mult(col_mult)
    print first, second, rows, answer
    mul = Multiplication(first, second, rows, answer)
    print "Solving..."
    print mul
    solved_env = solve(mul, is_verbose)
    print "Answer:"
    solved = Multiplication(first, second, rows, answer, solved_env)
    print solved
