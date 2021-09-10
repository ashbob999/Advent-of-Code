
#include "../aocHelper.h"

#include "day01.cpp"
#include "day02.cpp"
#include "day03.cpp"
#include "day04.cpp"
#include "day05.cpp"
#include "day06.cpp"
#include "day07.cpp"
#include "day08.cpp"
#include "day09.cpp"
#include "day10.cpp"
#include "day11.cpp"
#include "day12.cpp"
#include "day13.cpp"
#include "day14.cpp"
#include "day15.cpp"

using namespace std;

int main()
{
	Day01* d1 = new Day01(); // done
	Day02* d2 = new Day02(); // done
	Day03* d3 = new Day03(); // done
	Day04* d4 = new Day04(); // done slow
	Day05* d5 = new Day05(); // done
	Day06* d6 = new Day06(); // done
	Day07* d7 = new Day07(); // done
	Day08* d8 = new Day08(); // done
	Day09* d9 = new Day09(); // done slow
	Day10* d10 = new Day10(); // done slow
	Day11* d11 = new Day11(); // done
	Day12* d12 = new Day12(); // done
	Day13* d13 = new Day13(); // done slow
	Day14* d14 = new Day14(); // done
	Day15* d15 = new Day15(); // 

	auto cd = d15;

	vector<BaseDay*> days = {
			cd
	};

	runDays(days, { 1000 });

	cd->load_input();
	auto res = cd->solve();
	cd->unload_input();
	cout << res.first << " : " << res.second << endl;
	// cout << cd->stringResult.first << " : " << cd->stringResult.second << endl;

	for (auto& d : days)
	{
		delete d;
	}

	return 0;
}
