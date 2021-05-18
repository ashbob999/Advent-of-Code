#include "../aocHelper.h"

#include <immintrin.h>

template<>
struct std::hash<__m128i>
{
	std::size_t operator()(const __m128i& m) const
	{
		return _mm_extract_epi64(m, 0);
	}
};

template<>
struct std::equal_to<__m128i>
{
	bool operator()(const __m128i& m1, const __m128i& m2) const
	{
		return _mm_extract_epi64(m1, 0) == _mm_extract_epi64(m2, 0);
	}
};

template<int dims>
int get_adj(unordered_set<uint64_t>& grid, uint64_t pos, unordered_set<__m128i>& adj_values)
{
	int64_t pos2 = 0;
	pos2 |= pos;

	__m128i pos_128 = _mm_set_epi64x(0, pos2);

	int adj = 0;

	for (auto& av : adj_values)
	{
		__m128i val_128 = _mm_adds_epi16(pos_128, av);
		uint64_t val = _mm_extract_epi64(val_128, 0);

		if (grid.count(val) == 1)
		{
			adj++;

			if (adj > 3)
			{
				break;
			}
		}
	}

	return adj;
}

template<int dims>
int solve_gol(unordered_set<uint64_t> grid, int cycles, unordered_set<__m128i>& adj_values)
{
	auto handle_pos = [&adj_values](unordered_set<uint64_t>& grid, unordered_set<uint64_t>& next_grid, uint64_t pos)
	{
		int adj = get_adj<dims>(grid, pos, adj_values);

		if (grid.count(pos) == 1)
		{
			if (adj != 2 && adj != 3)
			{
				next_grid.erase(pos);
			}
		}
		else
		{
			if (adj == 3)
			{
				next_grid.insert(pos);
			}
		}
	};

	for (int cycle = 0; cycle < cycles; cycle++)
	{
		unordered_set<uint64_t> next_grid(grid);

		array<int16_t, 4> min_values = { 0,0,0,0 };
		array<int16_t, 4> max_values = { 0,0,0,0 };

		for (uint64_t pos : next_grid)
		{

			for (int i = 0; i < dims; i++)
			{
				int16_t v = (pos >> (16 * i)) & 0xffff;

				min_values[i] = min(min_values[i], v);
				max_values[i] = max(max_values[i], v);
			}
		}

		for (int16_t x = min_values[0] - 1; x < max_values[0] + 2; x++)
		{
			for (int16_t y = min_values[1] - 1; y < max_values[1] + 2; y++)
			{
				for (int16_t z = min_values[2] - 1; z < max_values[2] + 2; z++)
				{
					// pack x/y/x
					uint64_t val = 0;
					val |= ((int64_t) x & 0xffff) << 0;
					val |= ((int64_t) y & 0xffff) << 16;
					val |= ((int64_t) z & 0xffff) << 32;


					if (dims == 3) // 3D
					{
						handle_pos(grid, next_grid, val);
					}
					else if (dims == 4) // 4D
					{
						for (int16_t w = min_values[3] - 1; w < max_values[3] + 2; w++)
						{
							// pack w
							uint64_t val2 = val;
							val2 |= ((int64_t) w & 0xffff) << 48;


							handle_pos(grid, next_grid, val2);
						}
					}
				}
			}
		}

		grid = move(next_grid);
	}

	return grid.size();
}

class Day17 : public BaseDay
{
public:
	Day17() : BaseDay("17") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// 64 bits packed with 4x16 bits (w, z, y, x)
		// pack: ((int64_t) v & 0xffff) << 16;
		// unpack: (v >> 16) & 0xffff
		unordered_set<uint64_t> grid;

		// parse
		int16_t x = 0, y = 0;
		while (*input != '\0')
		{
			x = 0;
			while (*input != '\n')
			{
				if (*input == '#')
				{

					uint64_t val = 0;
					val |= ((int64_t) x & 0xffff) << 0;
					val |= ((int64_t) y & 0xffff) << 16;

					grid.insert(val);
				}

				x++;
				input++;
			}
			y++;
			input++;
		}

		__m128i zero = _mm_set_epi64x(0, 0);

		// part 1
		unordered_set<__m128i> dim3_adj_values;
		for (int16_t x = -1; x < 2; x++)
		{
			for (int16_t y = -1; y < 2; y++)
			{
				for (int16_t z = -1; z < 2; z++)
				{
					__m128i val = _mm_set_epi16(0, 0, 0, 0, 0, z, y, x);
					dim3_adj_values.insert(val);
				}
			}
		}

		dim3_adj_values.erase(zero);

		part1 = solve_gol<3>(grid, 6, dim3_adj_values);

		// part 2
		unordered_set<__m128i> dim4_adj_values;
		for (int16_t x = -1; x < 2; x++)
		{
			for (int16_t y = -1; y < 2; y++)
			{
				for (int16_t z = -1; z < 2; z++)
				{
					for (int16_t w = -1; w < 2; w++)
					{
						__m128i val = _mm_set_epi16(0, 0, 0, 0, w, z, y, x);
						dim4_adj_values.insert(val);
					}
				}
			}
		}

		dim4_adj_values.erase(zero);

		part2 = solve_gol<4>(grid, 6, dim4_adj_values);

		return { part1, part2 };
	}
};
