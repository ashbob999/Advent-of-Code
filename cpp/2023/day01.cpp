#include "../aocHelper.h"

#include <bit>
#include <immintrin.h>

namespace
{
	uint32_t get_first_bit_set(const uint32_t value)
	{
		return std::countr_zero(value);
	}

	uint32_t clear_leftmost_set(uint32_t value)
	{
		return value & (value - 1);
	}

	// see: http://0x80.pl/articles/simd-strfind.html#generic-sse-avx2
	int fast_find(const char* str1, int length1, const char* str2, int length2)
	{
		const __m256i first = _mm256_set1_epi8(str2[0]);
		const __m256i last = _mm256_set1_epi8(str2[length2 - 1]);

		for (size_t i = 0; i < length1; i += 32)
		{
			const __m256i block_first = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(str1 + i));
			const __m256i block_last = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(str1 + i + length2 - 1));

			const __m256i eq_first = _mm256_cmpeq_epi8(first, block_first);
			const __m256i eq_last = _mm256_cmpeq_epi8(last, block_last);

			uint32_t mask = _mm256_movemask_epi8(_mm256_and_si256(eq_first, eq_last));
			while (mask != 0)
			{
				const auto bitpos = get_first_bit_set(mask);

				if (memcmp(str1 + i + bitpos + 1, str2 + 1, length2 - 2) == 0)
				{
					return i + bitpos;
				}

				mask = clear_leftmost_set(mask);
			}
		}

		return -1;
	}

	template<int LineLength>
	int fast_digit_find(const std::array<char, LineLength>& line)
	{
		/*
		zero compare mask
		blend zeros to be 255

		'0'-'9' => 48-57
		'a'-'z' => 97-122

		255 - digit
		'0'-'9' => 207-198
		'a'-'z' => 158-133

		subtract with saturation: 197
		'0'-'9' => 1-10
		'a'-'z' => 0-0

		find lowest non-zero byte
			compare > zero to get non-zero mask
			get mask of full bytes

		*/

		const __m256i zero = _mm256_setzero_si256();
		const __m256i value255 = _mm256_set1_epi8(255);
		const __m256i value197 = _mm256_set1_epi8(197);

		for (int i = 0; i < LineLength; i += 32)
		{
			__m256i bytes = _mm256_loadu_epi8(reinterpret_cast<const __m256i*>(line.data() + i));

			__m256i mask = _mm256_cmpeq_epi8(bytes, zero);
			bytes = _mm256_blendv_epi8(bytes, value255, mask);

			bytes = _mm256_sub_epi8(value255, bytes);

			bytes = _mm256_subs_epu8(bytes, value197);
			__m256i bytes2 = _mm256_sub_epi8(bytes, value197);

			__m256i non_zero_mask = _mm256_cmpgt_epi8(bytes, zero);
			uint32_t bitmask = _mm256_movemask_epi8(non_zero_mask);
			if (bitmask != 0)
			{
				return i + std::countr_zero(bitmask);
			}
		}

		return -1;
	}

	template<int LineLength>
	inline void create_reversed(const std::array<char, LineLength>& original, std::array<char, LineLength>& reversed)
	{
		static_assert(LineLength == 64);

		/*
		64 bytes = 512 bits

		split into 4 128 chunks (kept in 2 256bit regs): LL, LH, UL, UH

		swap all bytes in each (in 128bit chunks)

		permute each 256 to swap high and low (LL, LH -> LH, LL)

		store back with the 256 regs swapped (UH, UL, LH, LL)

		shift right by 64-length to remove starting nulls
		*/

		const __m256i shuffle_swap = _mm256_set_epi8(
			0,
			1,
			2,
			3,
			4,
			5,
			6,
			7,
			8,
			9,
			10,
			11,
			12,
			13,
			14,
			15,
			0,
			1,
			2,
			3,
			4,
			5,
			6,
			7,
			8,
			9,
			10,
			11,
			12,
			13,
			14,
			15);

		// load bytes 0-31
		__m256i lower = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(original.data()));
		// load bytes 31-63
		__m256i upper = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(original.data() + 32));

		// swap bytes
		lower = _mm256_shuffle_epi8(lower, shuffle_swap);
		upper = _mm256_shuffle_epi8(upper, shuffle_swap);

		// swap high/low 128 bits
		lower = _mm256_permute2x128_si256(lower, lower, 0b0000'0001);
		upper = _mm256_permute2x128_si256(upper, upper, 0b0000'0001);

		// store bytes 0-31
		_mm256_storeu_si256(reinterpret_cast<__m256i*>(reversed.data()), upper);

		// store bytes 32-63
		_mm256_storeu_si256(reinterpret_cast<__m256i*>(reversed.data() + 32), lower);
	}
}

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int LineLength = 64;
		constexpr int CharsPerReg = 256 / 8;
		static_assert(LineLength % CharsPerReg == 0);

		const auto solve_both = [&part1, &part2](
									const std::array<char, LineLength>& line,
									const std::array<char, LineLength>& reversed_line,
									int char_count)
		{
			constexpr std::array<std::pair<const char*, std::pair<int, int>>, 10> numbers = {
				{{"zero", {0, 4}},
				 {"one", {1, 3}},
				 {"two", {2, 3}},
				 {"three", {3, 5}},
				 {"four", {4, 4}},
				 {"five", {5, 4}},
				 {"six", {6, 3}},
				 {"seven", {7, 5}},
				 {"eight", {8, 5}},
				 {"nine", {9, 4}}}};

			constexpr std::array<std::pair<const char*, std::pair<int, int>>, 10> numbers_reversed = {
				{{"orez", {0, 4}},
				 {"eno", {1, 3}},
				 {"owt", {2, 3}},
				 {"eerht", {3, 5}},
				 {"ruof", {4, 4}},
				 {"evif", {5, 4}},
				 {"xis", {6, 3}},
				 {"neves", {7, 5}},
				 {"thgie", {8, 5}},
				 {"enin", {9, 4}}}};

			int v1_index = 1000;
			int v1 = 0;

			v1_index = fast_digit_find(line);
			v1 = line[v1_index] - '0';

			int v2_index = 1000;
			int v2 = 0;

			v2_index = fast_digit_find(reversed_line);
			v2 = reversed_line[v2_index] - '0';

			part1 += v1 * 10 + v2;

			for (auto&& [number, value] : numbers)
			{
				int pos1 = fast_find(line.data(), LineLength, number, value.second);

				if (pos1 != -1 && pos1 < v1_index)
				{
					v1_index = pos1;
					v1 = value.first;
				}
			}

			for (auto&& [number, value] : numbers_reversed)
			{
				int pos2 = fast_find(reversed_line.data(), LineLength, number, value.second);

				if (pos2 != -1 && pos2 < v2_index)
				{
					v2_index = pos2;
					v2 = value.first;
				}
			}

			part2 += v1 * 10 + v2;
		};

		std::array<char, LineLength> line{'\0'};
		std::array<char, LineLength> reversed_line{'\0'};
		int i = 0;

		const __m256i zero = _mm256_setzero_si256();

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				// reverse line
				create_reversed<LineLength>(line, reversed_line);

				solve_both(line, reversed_line, i);

				i = 0;

				// zero out data
				_mm256_storeu_si256((__m256i*) (line.data() + (0 * CharsPerReg)), zero);
				_mm256_storeu_si256((__m256i*) (line.data() + (1 * CharsPerReg)), zero);
			}
			else
			{
				line[i] = *input;
				i++;
			}

			input++;
		}

		// part 1

		// part 2

		return {part1, part2};
	}
};
