#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<vector<int>> grid;

		grid.push_back({});

		// parse input
		while (*input != '\0')
		{
			if (*input == '\n')
			{
				grid.push_back({});
				input++;
			}
			else if (*input >= '0' && *input <= '9')
			{
				int n = numericParse<int>(input);
				grid.back().push_back(n);
			}
			else
			{
				input++;
			}
		}

		grid.pop_back();

		// part 1
		for (int y = 0; y < grid.size(); y++)
		{
			auto p = minmax_element(grid[y].begin(), grid[y].end());
			part1 += *p.second - *p.first;
		}

		// part 2
		auto get_div = [](vector<int>& arr)
		{
			for (int i = 0; i < arr.size(); i++)
			{
				for (int j = i + 1; j < arr.size(); j++)
				{
					if (arr[i] % arr[j] == 0)
					{
						return arr[i] / arr[j];
					}
				}
			}

			return 0;
		};

		for (int y = 0; y < grid.size(); y++)
		{
			sort(grid[y].begin(), grid[y].end(), greater<>());

			part2 += get_div(grid[y]);
		}

		return { part1, part2 };
	}
};
