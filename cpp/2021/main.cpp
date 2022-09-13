
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

using namespace std;

int main()
{
	Day01* d1 = new Day01(); // done
	Day02* d2 = new Day02(); // done
	Day03* d3 = new Day03(); // done
	Day04* d4 = new Day04(); // done
	Day05* d5 = new Day05(); // done slow
	Day06* d6 = new Day06(); // done
	Day07* d7 = new Day07(); // done
	Day08* d8 = new Day08(); // done
	Day09* d9 = new Day09(); // done
	Day10* d10 = new Day10(); // done

	auto cd = d10;

	vector<BaseDay*> days = {
		//d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24, d25
		cd
	};

	//runDays(days, { 100 });


	cd->load_input();
	auto res = cd->solve();
	cd->unload_input();
	cout << res.first << " : " << res.second << endl;
	//cout << cd->stringResult.first << " : " << cd->stringResult.second << endl;


	for (auto& d : days)
	{
		delete d;
	}

	return 0;
}
