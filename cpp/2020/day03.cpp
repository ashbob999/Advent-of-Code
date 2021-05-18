#include "../aocHelper.h"

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// width is 31
		const int w = 31;
		// height is 323
		const int h = 323;

		char grid[(w * h) + 1];

		int i = 0;
		bool foundW = false;

		while (*input != '\0')
		{
			if (*input != '\n')
			{
				grid[i] = *input;
				i++;
			}
			input++;
		}

		grid[i] = '\0';

		auto countTrees = [&grid, &h, &w](int dx, int dy)
		{
			int trees = 0;

			int x = 0, y = 0;
			while (y < h - 1)
			{
				x += dx;
				x %= w;
				y += dy;

				if (grid[y*w+x] == '#')
				{
					trees++;
				}
			}

			return trees;
		};

		part1 = countTrees(3, 1);
		part2 = part1 * countTrees(1, 1) * countTrees(5, 1) * countTrees(7, 1) * countTrees(1, 2);

		return { part1, part2 };
	}
};
