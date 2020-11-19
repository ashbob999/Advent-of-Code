# Advent-of-Code
All solutions to the Advent of Code days. (That I've completed)

All code is written in Python3

to generate current day files:
```shell script
python generate.py
```

options:
```shell script
-y (--year)
-d (--day)
-s (--session)
-i (--input)
-o (--overwire)
-a (--all)
```
`--year` specifies the year to generate the file for. (default: current year)

`--day` specifies the day to generate. (default: current day)

`--session` whether or not to add the session loading code to the day file (default: false). The session variable
 should be located in a `.env` file, located in the root folder.

`--input` whether or not to create te input file. (default: false)

`--overwrite` whether or not the overwrite the existing day file. (default: false)

`--all` Sets `--session --input --overwrite` to true. (default: false)

to run day file:
```shell script
cd 2019/
python dayXX.py
```