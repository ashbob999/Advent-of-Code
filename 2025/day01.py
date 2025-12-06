# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day01.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[str, 1, Merge([int]), 0, ""], "\n"])


def part1():
    c = 50
    z = 0
    for d, i in data:
      if d == "L":
          c -= i
      else:
          c += i
          
      c = c % 100
          
      if c == 0:
          z += 1
          
    return z


def part2():
    c = 50
    z = 0
    for d, i in data:
      for _ in range(i):
          if d == "L":
              c -= 1
          else:
              c += 1
              
          c = c % 100
              
          if c == 0:
              z += 1
          
    return z


p1()
p2()
