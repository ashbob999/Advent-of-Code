
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
#include "day16.cpp"
#include "day17.cpp"
#include "day18.cpp"
#include "day19.cpp"
#include "day20.cpp"
#include "day21.cpp"
#include "day22.cpp"
#include "day23.cpp"
#include "day24.cpp"
#include "day25.cpp"

using namespace std;

int main()
{
	Day01* d1 = new Day01(); // done
	Day02* d2 = new Day02(); // done
	Day03* d3 = new Day03(); // done
	Day04* d4 = new Day04(); // done
	Day05* d5 = new Day05(); // done
	Day06* d6 = new Day06(); // done
	Day07* d7 = new Day07(); // done
	Day08* d8 = new Day08(); // done
	Day09* d9 = new Day09(); // done
	Day10* d10 = new Day10(); // done
	Day11* d11 = new Day11(); // done
	Day12* d12 = new Day12(); // done
	Day13* d13 = new Day13(); // done
	Day14* d14 = new Day14(); // done
	Day15* d15 = new Day15(); // done slow
	Day16* d16 = new Day16(); // done
	Day17* d17 = new Day17(); // done slow
	Day18* d18 = new Day18(); // done
	Day19* d19 = new Day19(); // done
	Day20* d20 = new Day20(); // done
	Day21* d21 = new Day21(); // done slow
	Day22* d22 = new Day22(); // done slow
	Day23* d23 = new Day23(); // done
	Day24* d24 = new Day24(); // done slow
	Day25* d25 = new Day25(); // done slow

	auto cd = d25;

	vector<BaseDay*> days = {
		//d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24, d25
		cd
	};

	//runDays(days, { 10 });


	cd->load_input();
	auto res = cd->solve();
	cd->unload_input();
	cout << res.first << " : " << res.second << endl;
	cout << cd->stringResult.first << " : " << cd->stringResult.second << endl;


	for (auto& d : days)
	{
		delete d;
	}

	return 0;
}
