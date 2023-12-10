
#include "../aocHelper.h"

#include "day01.cpp" // dones
#include "day02.cpp"
#include "day03.cpp"

using namespace std;

int main()
{
	Day01* d1 = new Day01(); // done
	Day02* d2 = new Day02(); // done

	auto cd = d2;

	vector<BaseDay*> days = {// d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19,
							 // d20, d21, d22, d23, d24, d25
							 cd};

	// runDays(days, {1000});

	cd->load_input();
	auto res = cd->solve();
	cd->unload_input();
	cout << res.first << " : " << res.second << endl;
	// cout << cd->stringResult.first << " : " << cd->stringResult.second << endl;
	// cout << cd->stringResult.second << endl;

	for (auto& d : days)
	{
		delete d;
	}

	return 0;
}
