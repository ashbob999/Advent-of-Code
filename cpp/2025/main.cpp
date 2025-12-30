#include "../aocHelper.h"

#include "day01.cpp"
#include "day02.cpp"
#include "day03.cpp"
#include "day12.cpp"

using namespace std;

int main()
{
	Day01 d1{};
	Day02 d2{};
	Day03 d3{};
	Day12 d12{};

	auto&& cd = d12;

	vector<BaseDay*> days = {// &d1, &d2, &d3, &d4, &d5, &d6, &d7, &d8, &d9, &d10, &d11, &d12,
							 &cd};

	 runDays(days, {100000});

	cd.load_input();
	auto res = cd.solve();
	cd.unload_input();
	cout << res.first << " : " << res.second << endl;
	// cout << cd.stringResult.first << " : " << cd.stringResult.second << endl;
	// cout << cd.stringResult.second << endl;

	return 0;
}
