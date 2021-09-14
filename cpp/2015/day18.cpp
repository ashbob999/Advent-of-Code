#include "../aocHelper.h"
#include "custom_bitset.hpp"

class Day18 : public BaseDay
{
public:
	Day18() : BaseDay("18") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int WIDTH = 100, HEIGHT = 100;

		custom_bitset grid[HEIGHT];
		custom_bitset tmp_grid_1[HEIGHT];
		custom_bitset tmp_grid_2[HEIGHT];

		// parse input
		for (int y = 0; y < HEIGHT; y++)
		{
			for (int x = 0; x < WIDTH; x++)
			{
				if (*input == '#')
				{
					grid[y].set(x);
				}
				input++;
			}
			input++;
		}

		static constexpr pair<int, int> dirs[8] = { {0, 1}, {0, -1}, {1, 0}, {1, -1}, {1, 1}, {-1, 0}, {-1, 1}, {-1, -1} };

		auto check_adj = [&WIDTH, &HEIGHT](int x, int y, int& changed, custom_bitset grid[HEIGHT], custom_bitset tmp_grid[HEIGHT])
		{
			int adj = 0;

			for (auto& dir : dirs)
			{
				int tmp_x = x + dir.second;
				int tmp_y = y + dir.first;

				while (tmp_x >= 0 && tmp_y >= 0 && tmp_x < WIDTH && tmp_y < HEIGHT)
				{
					if (grid[tmp_y].get(tmp_x))
					{
						adj++;
					}
					break;

					tmp_x += dir.second;
					tmp_y += dir.first;
				}
			}

			if (grid[y].get(x) == 0 && adj == 3) // off -> on
			{
				tmp_grid[y].set(x);
				changed++;
			}
			if (grid[y].get(x) && adj != 2 && adj != 3) // on -> off
			{
				tmp_grid[y].unset(x);
				changed++;
			}
		};

		auto step_gol = [&WIDTH, &HEIGHT, &check_adj](custom_bitset grid[HEIGHT], custom_bitset tmp_grid[HEIGHT])
		{
			int changed = 0;

			copy(grid, grid + HEIGHT, tmp_grid);

			for (int y = 0; y < HEIGHT; y++)
			{
				for (int x = 0; x < WIDTH; x++)
				{
					check_adj(x, y, changed, grid, tmp_grid);
				}
			}

			copy(tmp_grid, tmp_grid + HEIGHT, grid);
		};

		copy(grid, grid + HEIGHT, tmp_grid_1);
		copy(grid, grid + HEIGHT, tmp_grid_2);

		// part 1
		for (int i = 0; i < 100; i++)
		{
			step_gol(grid, tmp_grid_1);
		}

		for (int y = 0; y < HEIGHT; y++)
		{
			part1 += grid[y].count();
		}

		// part 2
		copy(tmp_grid_2, tmp_grid_2 + HEIGHT, grid);

		for (int i = 0; i < 100; i++)
		{
			grid[0].set(0);
			grid[0].set(99);
			grid[99].set(0);
			grid[99].set(99);

			step_gol(grid, tmp_grid_1);
		}

		grid[0].set(0);
		grid[0].set(99);
		grid[99].set(0);
		grid[99].set(99);

		for (int y = 0; y < HEIGHT; y++)
		{
			part2 += grid[y].count();
		}

		return { part1, part2 };
	}
};
