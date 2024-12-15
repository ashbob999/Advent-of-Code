#include "../aocHelper.h"

class Day17 : public BaseDay
{
public:
	Day17() : BaseDay("17") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		int x_min, x_max, y_min, y_max;

		input += 15; // skip 'target area: x='
		x_min = numericParse<int>(input);
		input += 2; // skip '..'
		x_max = numericParse<int>(input);
		input += 4; // skip ', y='
		y_min = numericParse<int>(input);
		input += 2; // skip '..'
		y_max = numericParse<int>(input);

		auto calc_traj = [&](int xv, int yv)
		{
			long long max_height = 0;

			long long x = 0;
			long long y = 0;

			while (x <= x_max)
			{
				x += xv;
				y += yv;

				if (xv > 0)
				{
					xv--;
				}
				else if (xv < 0)
				{
					xv++;
				}

				yv--;

				max_height = max(max_height, y);

				if (x >= x_min && x <= x_max && y >= y_min && y <= y_max)
				{
					return pair{ true, max_height };
				}

				if (yv < 0 && y < y_min)
				{
					break;
				}
			}

			return pair{ false, 0LL };
		};

		for (int yv = -100; yv <= 100; yv++)
		{
			for (int xv = 0; xv <= x_max; xv++)
			{
				auto res = calc_traj(xv, yv);
				if (res.first)
				{
					// part 1
					part1 = max(part1, res.second);

					// part 2
					part2++;
				}
			}
		}

		return { part1, part2 };
	}
};
