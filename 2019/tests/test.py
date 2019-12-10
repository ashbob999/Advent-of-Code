import unittest

"""
Day 01: 6ms
Day 02: 200-216ms
Day 03: 203-218ms
Day 04: 2046-2231ms
Day 05: 15ms
Day 06: 62-93ms
Day 07: 140-156ms
Day 08: 46-62ms
Day 09: 1431-1546ms
Day 10: ms
"""


class DayTest(unittest.TestCase):
    @staticmethod
    def test_something():
        with open("../Day 9 - Sensor Boost/code_09.py") as file:
            exec(file.read(), locals(), locals())
            file.close()


if __name__ == '__main__':
    unittest.main()
