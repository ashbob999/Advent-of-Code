#include "../aocHelper.h"

#include <immintrin.h>

class Day18 : public BaseDay
{
public:
	Day18() : BaseDay("18") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		uint64_t low_half = 0;
		uint64_t high_half = 0;

		int row_length = 0;

		// firts populate the high half the the low half

		// parse input
		while (*input != '\n')
		{
			if (row_length >= 64)
			{
				low_half <<= 1;
			}
			else
			{
				high_half <<= 1;
			}

			if (*input == '^') // trap
			{
				if (row_length >= 64)
				{
					low_half |= 1;
				}
				else
				{
					high_half |= 1;
				}
			}
			else // safe
			{
			}
			row_length++;
			input++;
		}

		low_half <<= 128 - row_length;

		uint64_t high_safe_xor_mask = row_length >= 64 ? 0xffffffffffffffff : (1 << row_length) - 1;
		uint64_t low_safe_xor_mask = row_length >= 64 ? 0xffffffffffffffff : (1 << row_length - 63) - 1;
		low_safe_xor_mask <<= 128 - row_length;

		int p1_rows = 40;
		int p2_rows = 400000;
		long long count = 0;

		count += _mm_popcnt_u64(high_half ^ high_safe_xor_mask);
		count += _mm_popcnt_u64(low_half ^ low_safe_xor_mask);

		/*
		row = .^^.^.^^^^
		. = safe
		^ = trap

		rules:
			^^. = trap
			.^^ = trap
			^.. = trap
			..^ = trap

			... = safe
			^^^ = safe
			.^. = safe
			^.^ = safe

		can use bit manipulation
			. = 0
			^ = 1

		and with 101 to remove middle bit

		traps:
			100
			001

		safe:
			000
			101

		then safe becomes left xor right == 0
		 and trap becomes left xor right == 1

		therefore the next row is caluclated by:
			(row << 1) ^ (row >> 1)
		*/

		// part 1
		int i = 1;
		for (; i < p1_rows; i++)
		{
			uint64_t left_high = (high_half << 1) | (low_half >> 63);
			uint64_t left_low = (low_half << 1);

			uint64_t right_high = high_half >> 1;
			uint64_t right_low = ((low_half >> 1) & low_safe_xor_mask) | (high_half << 63);

			high_half = left_high ^ right_high;
			low_half = left_low ^ right_low;

			count += _mm_popcnt_u64(high_half ^ high_safe_xor_mask);
			count += _mm_popcnt_u64(low_half ^ low_safe_xor_mask);
		}

		part1 = count;

		for (; i < p2_rows; i++)
		{
			uint64_t left_high = (high_half << 1) | (low_half >> 63);
			uint64_t left_low = (low_half << 1);

			uint64_t right_high = high_half >> 1;
			uint64_t right_low = ((low_half >> 1) & low_safe_xor_mask) | (high_half << 63);

			high_half = left_high ^ right_high;
			low_half = left_low ^ right_low;

			count += _mm_popcnt_u64(high_half ^ high_safe_xor_mask);
			count += _mm_popcnt_u64(low_half ^ low_safe_xor_mask);
		}

		part2 = count;

		return { part1, part2 };
	}
};
