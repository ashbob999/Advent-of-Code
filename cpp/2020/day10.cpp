#include "../aocHelper.h"

class Day10 : public BaseDay
{
public:
	Day10() : BaseDay("10") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> data;

		int n;

		while ((n = numericParse<int>(input)))
		{
			data.push_back(n);
		}

		sort(data.begin(), data.end());

		// part 1

		int a[4] = { 0, 0, 0, 0 };

		a[data[0]]++;

		for (int i = 0; i < data.size() - 1; i++)
		{
			a[data[i + 1] - data[i]]++;
		}

		a[3]++;

		part1 = a[1] * a[3];

		// part 2

		data.push_back(data.back() + 3);

		long long ways[200] = { 1 };

		for (auto& v : data)
		{
			long long s = 0;
			if (v > 0)
			{
				s += ways[v - 1];
			}
			if (v > 1)
			{
				s += ways[v - 2];
			}
			if (v > 2)
			{
				s += ways[v - 3];
			}

			ways[v] = s;
		}

		part2 = ways[data.back()];

		return { part1, part2 };
	}
};
