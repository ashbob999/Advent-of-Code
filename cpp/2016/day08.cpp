#include "../aocHelper.h"

#include <immintrin.h>

const static std::unordered_map<uint64_t, char> char_mapping{ {
  {0x19297A52, 'A'}, {0x392E4A5C, 'B'}, {0x1928424C, 'C'},
  {0x39294A5C, 'D'}, {0x3D0E421E, 'E'}, {0x3D0E4210, 'F'},
  {0x19285A4E, 'G'}, {0x252F4A52, 'H'}, {0x1C42108E, 'I'},
  {0x0C210A4C, 'J'}, {0x254C5292, 'K'}, {0x2108421E, 'L'},
  {0x19294A4C, 'O'}, {0x39297210, 'P'}, {0x39297292, 'R'},
  {0x1D08305C, 'S'}, {0x1C421084, 'T'}, {0x25294A4C, 'U'},
  {0x23151084, 'Y'}, {0x3C22221E, 'Z'}
} };

class Day08 : public BaseDay
{
public:
	Day08() : BaseDay("08") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// grid is 50 wide by 6 tall
		array<uint64_t, 6> grid{};
		constexpr uint64_t grid_width = 50;
		constexpr uint64_t grid_height = 6;
		constexpr uint64_t char_width = 5;
		constexpr uint64_t char_height = 5;
		constexpr uint64_t char_count = grid_width / char_width;

		auto rect = [&](uint64_t width, uint64_t height)
		{
			uint64_t on_mask = (1ULL << width) - 1ULL;
			on_mask <<= grid_width - width;

			for (int i = 0; i < height; i++)
			{
				grid[i] |= on_mask;
			}
		};

		auto rotate_column = [&](uint64_t index, uint64_t count)
		{
			uint8_t bits[grid_height]{ 0 };

			// extract bits
			uint64_t shift_amount = grid_width - index - 1;

			for (int i = 0; i < grid_height; i++)
			{
				if ((grid[i] >> shift_amount & 1) == 1)
				{
					bits[i] = 1;
				}
			}

			// do rotate
			uint8_t new_bits[grid_height]{ 0 };

			for (int i = 0; i < grid_height; i++)
			{
				int index = (i + count) % grid_height;
				new_bits[index] = bits[i];
			}

			// insert bits
			uint64_t mask = 1ULL << shift_amount;
			uint64_t clear_mask = ~mask;

			for (int i = 0; i < grid_height; i++)
			{
				// clear the bits
				grid[i] &= clear_mask;

				if (new_bits[i] == 1)
				{
					// set bit
					grid[i] |= mask;
				}
			}
		};

		auto rotate_row = [&](uint64_t index, uint64_t count)
		{
			// value << count | value >> (32 - count);
			// right circular shift
			// also have to shift the right bits left as well to compensate for the extra 14 empty bits

			uint64_t og_value = grid[index];

			uint64_t shifted = og_value >> count | og_value << (64ULL - count);
			uint64_t keep_mask = ((1ULL << grid_width) - 1ULL) >> count;
			uint64_t top_bits = shifted & (keep_mask ^ 0xffffffffffffffff);
			top_bits >>= 64 - grid_width; // >>= 14

			uint64_t result = (shifted & keep_mask) | top_bits;
			grid[index] = result;
		};

		// parse input
		while (*input != '\0')
		{
			input++; // skip 'r'
			if (*input == 'e') // rect
			{
				input += 4; // skip "ect "
				uint64_t width = (uint64_t) numericParse<int>(input);
				input++; // skip 'x'
				uint64_t height = (uint64_t) numericParse<int>(input);

				rect(width, height);
			}
			else // rotate
			{
				input += 6; // skip "otate "
				if (*input == 'r') // row
				{
					input += 6; // skip "row y="
					uint64_t row = (uint64_t) numericParse<int>(input);
					input += 4; // skip " by "
					uint64_t count = (uint64_t) numericParse<int>(input);

					rotate_row(row, count);
				}
				else // column
				{
					input += 9; // skip "column x="
					uint64_t column = (uint64_t) numericParse<int>(input);
					input += 4; // skip " by "
					uint64_t count = (uint64_t) numericParse<int>(input);

					rotate_column(column, count);
				}
			}
			input++; // skip '\n'
		}

		// part 1
		part1 += _mm_popcnt_u64(grid[0]);
		part1 += _mm_popcnt_u64(grid[1]);
		part1 += _mm_popcnt_u64(grid[2]);
		part1 += _mm_popcnt_u64(grid[3]);
		part1 += _mm_popcnt_u64(grid[4]);
		part1 += _mm_popcnt_u64(grid[5]);

		// part 2
		char p1_out[char_count]{ '\0' };

		constexpr uint64_t mask = (1 << char_width) - 1;

		for (int i = 0; i < char_count; i++)
		{
			uint64_t shift_amount = (char_count - i - 1) * char_width;

			uint64_t char_value = 0;

			for (int r = 0; r < grid_height; r++)
			{
				char_value <<= char_width;
				char_value |= (grid[r] >> shift_amount) & mask;
			}

			p1_out[i] = char_mapping.at(char_value);
		}

		memcpy(this->stringResult.second, p1_out, char_count);

		return { part1, part2 };
	}
};
