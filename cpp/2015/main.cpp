
#include "../aocHelper.h"

#include "day01.cpp"
#include "day02.cpp"
#include "day03.cpp"
#include "day04.cpp"
#include "day05.cpp"

using namespace std;

int main()
{
	Day01* d1 = new Day01(); // done
	Day02* d2 = new Day02(); // done
	Day03* d3 = new Day03(); // done
	Day04* d4 = new Day04(); // done slow
	Day05* d5 = new Day05(); // done

	auto cd = d4;

	vector<BaseDay*> days = {
		cd
	};

	runDays(days, { 50 });

	cd->load_input();
	auto res = cd->solve();
	cd->unload_input();
	cout << res.first << " : " << res.second << endl;
	//cout << cd->stringResult.first << endl;


	for (auto& d : days)
	{
		delete d;
	}

	return 0;
}
