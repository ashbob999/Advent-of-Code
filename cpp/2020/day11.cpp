#include "../aocHelper.h"

struct custom_bitset
{
	static const unsigned bits_per_value = 64;
	static const unsigned value_count = 2;
	static const uint64_t max = 0xffffffffffffffff;

	uint64_t data[value_count] = { 0, 0 };

	custom_bitset()
	{
		//data[0] = 0;
		//data[1] = 0;
	};

	custom_bitset(const custom_bitset& cb)
	{
		data[0] = cb.data[0];
		data[1] = cb.data[1];
	}

	inline void set(unsigned index)
	{
		unsigned data_index = index / bits_per_value;
		unsigned bit_index = index % bits_per_value;

		if (data_index <= value_count)
		{
			uint64_t val = (uint64_t) 1 << bit_index;

			data[data_index] |= val;
		}
	}

	inline void unset(unsigned index)
	{
		unsigned data_index = index / bits_per_value;
		unsigned bit_index = index % bits_per_value;

		if (data_index <= value_count)
		{
			uint64_t val = (uint64_t) 1 << bit_index;

			data[data_index] &= (max ^ val);
		}
	}

	inline bool get(unsigned index)
	{
		if (index < value_count * bits_per_value)
		{
			unsigned data_index = index / bits_per_value;
			unsigned bit_index = index % bits_per_value;

			uint64_t val = (uint64_t) 1 << bit_index;

			return data[data_index] & val;
		}
		return 0;
	}

	inline unsigned count()
	{
		unsigned cnt = 0;
		for (int i = 0; i < value_count; i++)
		{
			uint64_t t = data[i];
			while (t)
			{
				if (t & 1)
				{
					cnt++;
				}
				t >>= 1;
			}
		}

		return cnt;
	}
};

class Day11 : public BaseDay
{
public:
	Day11() : BaseDay("11") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		const int w = 93;
		const int h = 90;

		custom_bitset floor[h];
		custom_bitset grid[h];

		// parse input

		for (int y = 0; y < h; y++)
		{
			for (int x = 0; x < w; x++)
			{
				if (*input == 'L')
				{
					floor[y].set(x);
					// grid[y].unset(x)
				}
				else if (*input == '#')
				{
					floor[y].set(x);
					grid[y].set(x);
				}
				else if (*input == '.')
				{
					//floor[y].unset(x);
					//grid[y].unset(x);
				}
				input++;
			}
			input++;
		}

		custom_bitset tmp_grid_1[h];
		copy(grid, grid + h, tmp_grid_1);
		custom_bitset tmp_grid_2[h];
		copy(grid, grid + h, tmp_grid_2);

		// part 1

		auto check_adj_1 = [&w, &h, &floor, &grid, &tmp_grid_1](int x, int y, int& changed)
		{
			int adj = 0;

			if (y > 0 && floor[y].get(x) && grid[y - 1].get(x))
			{
				adj++;
			}
			if (y < h - 1 && floor[y + 1].get(x) && grid[y + 1].get(x))
			{
				adj++;
			}
			if (x > 0 && floor[y].get(x - 1) && grid[y].get(x - 1))
			{
				adj++;
			}
			if (x < w - 1 && floor[y].get(x + 1) && grid[y].get(x + 1))
			{
				adj++;
			}
			if (y > 0 && x > 0 && floor[y - 1].get(x - 1) && grid[y - 1].get(x - 1))
			{
				adj++;
			}
			if (y > 0 && x < w - 1 && floor[y - 1].get(x + 1) && grid[y - 1].get(x + 1))
			{
				adj++;
			}
			if (y < h - 1 && x > 0 && floor[y + 1].get(x - 1) && grid[y + 1].get(x - 1))
			{
				adj++;
			}
			if (y < h - 1 && x < w - 1 && floor[y + 1].get(x + 1) && grid[y + 1].get(x + 1))
			{
				adj++;
			}

			if (grid[y].get(x) == 0 && adj == 0)
			{
				tmp_grid_1[y].set(x);
				changed++;
			}
			if (grid[y].get(x) && adj >= 4)
			{
				tmp_grid_1[y].unset(x);
				changed++;
			}
		};

		while (true)
		{
			int changed = 0;

			copy(grid, grid + h, tmp_grid_1);

			for (int y = 0; y < h; y++)
			{
				for (int x = 0; x < w; x++)
				{
					if (floor[y].get(x))
					{
						check_adj_1(x, y, changed);
					}
				}
			}

			if (changed == 0)
			{
				break;
			}

			copy(tmp_grid_1, tmp_grid_1 + h, grid);
		}

		for (int i = 0; i < h; i++)
		{
			part1 += tmp_grid_1[i].count();
		}

		// part 2

		static constexpr pair<int, int> dirs[8] = { {0, 1}, {0, -1}, {1, 0}, {1, -1}, {1, 1}, {-1, 0}, {-1, 1}, {-1, -1} };

		copy(tmp_grid_2, tmp_grid_2 + h, grid);

		auto check_adj_2 = [&w, &h, &floor, &grid, &tmp_grid_2](int x, int y, int& changed)
		{
			int adj = 0;

			for (auto& dir : dirs)
			{
				int tmp_x = x + dir.second;
				int tmp_y = y + dir.first;

				while (tmp_x >= 0 && tmp_y >= 0 && tmp_x < w && tmp_y < h)
				{
					if (floor[tmp_y].get(tmp_x))
					{
						if (grid[tmp_y].get(tmp_x))
						{
							adj++;
						}
						break;
					}

					tmp_x += dir.second;
					tmp_y += dir.first;
				}
			}

			if (grid[y].get(x) == 0 && adj == 0)
			{
				tmp_grid_2[y].set(x);
				changed++;
			}
			if (grid[y].get(x) && adj >= 5)
			{
				tmp_grid_2[y].unset(x);
				changed++;
			}
		};

		while (true)
		{
			int changed = 0;

			copy(grid, grid + h, tmp_grid_2);

			for (int y = 0; y < h; y++)
			{
				for (int x = 0; x < w; x++)
				{
					if (floor[y].get(x))
					{
						check_adj_2(x, y, changed);
					}
				}
			}

			if (changed == 0)
			{
				break;
			}

			copy(tmp_grid_2, tmp_grid_2 + h, grid);
		}

		for (int i = 0; i < h; i++)
		{
			part2 += tmp_grid_2[i].count();
		}

		return { part1, part2 };
	}
};
