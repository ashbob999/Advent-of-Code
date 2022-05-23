#include "../aocHelper.h"

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<array<int, 3>> points;

		// parse input
		while (*input != '\0')
		{
			array<int, 3> t;

			t[0] = numericParse<int>(input);

			// skip all spaces
			while (*input == ' ')
			{
				input++;
			}

			t[1] = numericParse<int>(input);

			// skip all spaces
			while (*input == ' ')
			{
				input++;
			}

			t[2] = numericParse<int>(input);

			points.push_back(t);

			input++; // skip '\n'
		}

		auto check = [](int v1, int v2, int v3)
		{
			array<int, 3> arr = { v1, v2, v3 };
			sort(arr.begin(), arr.end());

			if (arr[0] + arr[1] > arr[2])
			{
				return true;
			}

			return false;
		};

		// part 1
		for (auto& t : points)
		{
			if (check(t[0], t[1], t[2]))
			{
				part1++;
			}
		}

		// part 2
		for (int i = 0; i < points.size(); i += 3)
		{
			for (int j = 0; j < 3; j++)
			{
				if (check(points[i][j], points[i + 1][j], points[i + 2][j]))
				{
					part2++;
				}
			}
		}

		return { part1, part2 };
	}
};
