#include "../aocHelper.h"

class Day11 : public BaseDay
{
public:
	Day11() : BaseDay("11") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int width = 10;
		constexpr int height = 10;

		using data = array<array<uint8_t, 10>, 10>;

		data grid{};

		for (int y = 0; y < height; y++)
		{
			for (int x = 0; x < width; x++)
			{
				grid[y][x] = *input - '0';
				input++;
			}
			input++; // skip '\n'
		}

		constexpr array<pair<int, int>, 8> dirs = { {
			{0, -1},
			{0, 1},
			{1, 0},
			{-1, 0},
			{1, 1},
			{-1, -1},
			{1, -1},
			{-1, 1},
		} };

		// part 1
		auto step = [&](data grid)
		{
			unordered_set<uint16_t> nines;

			for (uint8_t y = 0; y < height; y++)
			{
				for (uint8_t x = 0; x < width; x++)
				{
					if (grid[y][x] > 9)
					{
						nines.insert(x << 8 | y);
					}
					else
					{
						grid[y][x]++;

						if (grid[y][x] > 9)
						{
							nines.insert(x << 8 | y);
						}
					}
				}
			}

			unordered_set<uint16_t> flashed;

			while (nines.size() > 0)
			{
				uint16_t curr = *nines.begin();
				nines.erase(nines.begin());

				flashed.insert(curr);

				for (auto& dir : dirs)
				{
					uint8_t nx = (curr >> 8) + dir.first;
					uint8_t ny = (curr & 0xff) + dir.second;

					if (nx >= 0 && nx < width && ny >= 0 && ny < height)
					{
						grid[ny][nx]++;

						if (grid[ny][nx] > 9 && !flashed.contains(nx << 8 | ny))
						{
							nines.insert(nx << 8 | ny);
						}
					}
				}
			}

			int count = 0;

			for (int y = 0; y < height; y++)
			{
				for (int x = 0; x < width; x++)
				{
					if (grid[y][x] > 9)
					{
						grid[y][x] = 0;
						count++;
					}
				}
			}

			return pair<data, int>{ grid, count };
		};

		data grid_p1 = grid;
		for (int i = 0; i < 100; i++)
		{
			auto res = step(grid_p1);
			grid_p1 = res.first;
			part1 += res.second;
		}

		// part 2
		data grid_p2 = grid;
		int i = 0;
		while (true)
		{
			auto res = step(grid_p2);
			grid_p2 = res.first;

			if (res.second == width * height)
			{
				break;
			}

			i++;
		}

		part2 = i;

		return { part1, part2 };
	}
};
