import unittest

"""
Un-Optimised:

Day 01: 6ms
Day 02: 200-216ms
Day 03: 203-218ms
Day 04: 2,046-2,231ms
Day 05: 15ms
Day 06: 62-93ms
Day 07: 140-156ms
Day 08: 46-62ms
Day 09: 1,431-1,546ms
Day 10: 169-184ms
Day 11: 87-108ms
Day 12: 5,225-5,236ms
Day 13: 52,636ms
Day 14: ms
Day 15: ms
Day 16: ms
Day 17: ms
Day 18: ms
"""


class DayTest(unittest.TestCase):
    @staticmethod
    def test_something():
        with open("../Day 13 - Care Package/code_13.py") as file:
            exec(file.read(), locals(), locals())
            file.close()


if __name__ == '__main__':
    unittest.main()
