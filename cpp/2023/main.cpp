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
#include "day24.cpp"

using namespace std;

int main()
{
	Day01 d1{};	 // done
	Day02 d2{};	 // done
	Day03 d3{};	 // done
	Day04 d4{};	 // done
	Day05 d5{};	 // done
	Day06 d6{};	 // done
	Day07 d7{};	 // done
	Day08 d8{};	 // done
	Day09 d9{};	 // done
	Day10 d10{}; // done slow
	Day11 d11{}; // done
	Day12 d12{}; // done slow
	Day24 d24{}; // done slow

	auto&& cd = d12;

	vector<BaseDay*> days = {// &d1, &d2, &d3, &d4, &d5, &d6, &d7, &d8, &d9, &d10, &d11, &d12, &d13, &d14, &d15, &d16,
							 // &d17, &d18, &d19, &d20, &d21, &d22, &d23, &d24, &d25
							 &cd};

	//runDays(days, {1000});

	cd.load_input();
	auto res = cd.solve();
	cd.unload_input();
	cout << res.first << " : " << res.second << endl;
	// cout << cd->stringResult.first << " : " << cd->stringResult.second << endl;
	// cout << cd->stringResult.second << endl;

	return 0;
}
