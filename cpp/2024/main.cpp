#include "../aocHelper.h"

#include "day01.cpp"
#include "day14.cpp"
#include "day25.cpp"

using namespace std;

int main()
{
	Day01 d1{};
	Day14 d14{};
	Day25 d25{};

	auto&& cd = d25;

	vector<BaseDay*> days = {// &d1, &d2, &d3, &d4, &d5, &d6, &d7, &d8, &d9, &d10, &d11, &d12, &d13, &d14, &d15, &d16,
							 // &d17, &d18, &d19, &d20, &d21, &d22, &d23, &d24, &d25
							 &cd};

	runDays(days, {200000});

	cd.load_input();
	auto res = cd.solve();
	cd.unload_input();
	cout << res.first << " : " << res.second << endl;
	// cout << cd.stringResult.first << " : " << cd.stringResult.second << endl;
	// cout << cd.stringResult.second << endl;

	return 0;
}
