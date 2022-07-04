#include "../aocHelper.h"

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		int n = numericParse<int>(input);

		// part 1
		auto spiral_1 = [](int n)
		{
			pair<int, int> pos{ 0, 0 };

			int i = 1;
			int length = 0;

			while (true)
			{
				i++;
				length += 2;

				pos.first++;

				for (int j = 0; j < length - 1; j++) // right
				{
					pos.second--;
					i++;
					if (i == n)
					{
						return pos;
					}
				}

				for (int j = 0; j < length; j++) // top
				{
					pos.first--;
					i++;
					if (i == n)
					{
						return pos;
					}
				}

				for (int j = 0; j < length; j++) // left
				{
					pos.second++;
					i++;
					if (i == n)
					{
						return pos;
					}
				}

				for (int j = 0; j < length; j++) // bottom
				{
					pos.first++;
					i++;
					if (i == n)
					{
						return pos;
					}
				}
			}
		};

		auto res1 = spiral_1(n);
		part1 = abs(res1.first) + abs(res1.second);

		// part 2
		auto spiral_2 = [](int n)
		{
			pair<int, int> pos{ 0, 0 };
			map<pair<int, int>, int> locs;

			locs[pos] = 1;

			auto sum_locs = [&]()
			{
				int value = 0;
				for (int x = -1; x < 2; x++)
				{
					for (int y = -1; y < 2; y++)
					{
						if (x == 0 && y == 0)
						{
							continue;
						}

						pair<int, int> t{ pos.first + x, pos.second + y };

						if (locs.contains(t))
						{
							value += locs[t];
						}
					}
				}

				locs[pos] = value;
				return value;
			};

			int i = 1;
			int length = 0;

			while (true)
			{
				i++;
				length += 2;

				pos.first++;

				int v = sum_locs();
				if (v > n)
				{
					return v;
				}

				for (int j = 0; j < length - 1; j++) // right
				{
					pos.second--;
					i++;
					int v = sum_locs();
					if (v > n)
					{
						return v;
					}
				}

				for (int j = 0; j < length; j++) // top
				{
					pos.first--;
					i++;
					int v = sum_locs();
					if (v > n)
					{
						return v;
					}
				}

				for (int j = 0; j < length; j++) // left
				{
					pos.second++;
					i++;
					int v = sum_locs();
					if (v > n)
					{
						return v;
					}
				}

				for (int j = 0; j < length; j++) // bottom
				{
					pos.first++;
					i++;
					int v = sum_locs();
					if (v > n)
					{
						return v;
					}
				}
			}
		};

		part2 = spiral_2(n);

		return { part1, part2 };
	}
};
