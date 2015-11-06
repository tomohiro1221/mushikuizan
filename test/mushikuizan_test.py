import unittest
from mushikuizan.mul import Multiplication
from mushikuizan.solver import solve


test_cases = [
    ('x7x', 'x5', ['xx9x', '1x56'], '16xxx', {"first": {0: 6, 2: 8}, "second": {0: 2}}),
    ('x7x9', 'x4x', ['3xxxx', 'xxxxx', '20367'], '2342205', {"first": {0: 6, 2: 8}, "second": {0: 3, 2: 5}})
]


class MushikuizanTest(unittest.TestCase):
    def setUp(self):
        self.mushikuizans = [(Multiplication(*test_case[:4]), test_case[4]) for test_case in test_cases]

    def testTrue(self):
        for mushikuizan, answer in self.mushikuizans:
            derived_answer = solve(mushikuizan)
            for k1 in ["first", "second"]:
                for k2, v in derived_answer[k1].items():
                    self.assertEqual(answer[k1][k2], v)


if __name__ == '__main__':
    unittest.main()
