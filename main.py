from argparse import ArgumentParser
from mushikuizan.mul import Multiplication


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('col_mult')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False)
    args = parser.parse_args()
    return args.col_mult, args.verbose


def parse_col_mult(s):
    separated = s.split("|")
    a1, a2 = separated[0].split(" ")
    rs = separated[1].split(" ")
    return a1, a2, rs, separated[-1]


if __name__ == '__main__':
    col_mult, is_verbose = parse_args()
    first, second, rows, answer = parse_col_mult(col_mult)
    mul = Multiplication(first, second, rows, answer)
    print "Solving..."
    print mul
    print "Answer:"
    mul.solve()
    print mul
