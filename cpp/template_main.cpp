#include "../aocHelper.h"

#include "day01.cpp"

using namespace std;

int main()
{
	Day01 d1{};

	auto&& cd = d1;

	vector<BaseDay*> days = {// &d1, &d2, &d3, &d4, &d5, &d6, &d7, &d8, &d9, &d10, &d11, &d12,
							 &cd};

	// runDays(days, {1000});

	cd.load_input();
	auto res = cd.solve();
	cd.unload_input();
	cout << res.first << " : " << res.second << endl;
	// cout << cd.stringResult.first << " : " << cd.stringResult.second << endl;
	// cout << cd.stringResult.second << endl;

	return 0;
}
