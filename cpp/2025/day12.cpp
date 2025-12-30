#include "../aocHelper.h"

class Day12 : public BaseDay
{
public:
	Day12() : BaseDay("12") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		const __m256i inputLineMask = _mm256_setr_epi8(
			0x00, // <index>
			0x00, // ':'
			0x00, // '\n'
			0xFF,
			0xFF,
			0xFF,
			0x00, // '\n'
			0xFF,
			0xFF,
			0xFF,
			0x00, // '\n'
			0xFF,
			0xFF,
			0xFF,
			0x00, // '\n'
			0x00, // '\n'
			0x00, // <index>
			0x00, // ':'
			0x00, // '\n'
			0xFF,
			0xFF,
			0xFF,
			0x00, // '\n'
			0xFF,
			0xFF,
			0xFF,
			0x00, // '\n'
			0xFF,
			0xFF,
			0xFF,
			0x00, // '\n'
			0x00  // '\n'
		);

		const __m256i validSquare = _mm256_set1_epi8('#');

		const auto parseStartSection = [&inputLineMask, &validSquare](const char* input) -> std::pair<int16_t, int16_t>
		{
			const __m256i inputLine = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input));

			const __m256i masked = _mm256_and_si256(inputLine, inputLineMask);

			const __m256i valid = _mm256_cmpeq_epi8(masked, validSquare);

			const int bitmask = _mm256_movemask_epi8(valid);

			return {_mm_popcnt_u32(bitmask & 0x0000'FFFF), _mm_popcnt_u32(bitmask & 0xFFFF'0000)};
		};

		const auto [count0, count1] = parseStartSection(input);
		input += 32;
		const auto [count2, count3] = parseStartSection(input);
		input += 32;
		const auto [count4, count5] = parseStartSection(input);
		input += 32;

		const __m128i counts = _mm_setr_epi16(count0, count1, count2, count3, count4, count5, 0, 0);

		while (*input != '\0')
		{
			int width = numericParse<uint32_t>(input);

			__m128i newCounts = counts;
			newCounts = _mm_insert_epi16(newCounts, width, 6);

			input++; // skip 'x'

			// load the data line
			const __m256i dataLine = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input));

			// step 1: (shuffle low 128-bit lane)
			const __m128i lowLane = _mm256_castsi256_si128(dataLine);

			// source: abcdefghijklmnop
			// target: abefhiklno******
			const __m128i lowLaneShuffleControl = _mm_setr_epi8(
				0x04, // -> e (idx 4)
				0x05, // -> f (idx 5)
				0x07, // -> h (idx 7)
				0x08, // -> i (idx 8)
				0x0A, // -> k (idx 10)
				0x0B, // -> l (idx 11)
				0x0D, // -> n (idx 13)
				0x0E, // -> o (idx 14)
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0x00, // -> a (idx 0)
				0x01, // -> b (idx 1)
				0xFF, // -> 0
				0xFF  // -> 0
			);

			const __m128i lowLaneShuffled = _mm_shuffle_epi8(lowLane, lowLaneShuffleControl);

			// step 2: (shuffle high 128-bit lane)
			const __m128i highLane = _mm256_extracti128_si256(dataLine, 1);

			// source: ABCDEFGHIJKLMNOP
			// target: **********ABDE**
			const __m128i highLaneShuffleControl = _mm_setr_epi8(
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0x00, // -> A (idx 0)
				0x01, // -> B (idx 1)
				0x03, // -> D (idx 3)
				0x04, // -> E (idx 4)
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF, // -> 0
				0xFF  // -> 0
			);

			const __m128i highLaneShuffled = _mm_shuffle_epi8(highLane, highLaneShuffleControl);

			// step 3: (blend the two 128-bit lanes)

			// source:
			//     A = abefhiklno******
			//     B = **********ABDE**
			// target: abefhiklnoABDE**
			const __m128i blendControl = _mm_setr_epi8(
				0x00, // -> A
				0x00, // -> A
				0x00, // -> A
				0x00, // -> A
				0x00, // -> A
				0x00, // -> A
				0x00, // -> A
				0x00, // -> A
				0xFF, // -> B
				0xFF, // -> B
				0xFF, // -> B
				0xFF, // -> B
				0x00, // -> A
				0x00, // -> A
				0x00, // -> A
				0x00  // -> A
			);

			const __m128i blended = _mm_blendv_epi8(lowLaneShuffled, highLaneShuffled, blendControl);

			// expand the bytes into 16-bit values
			const __m256i values = _mm256_cvtepu8_epi16(blended);

			// values are: ABCDEFGHIJKLXY**
			// where:
			//		XY are the height of the grid
			//		ABCDEFGHIJKL are the required counts for each grid

			// convert the values into actual numbers
			const __m128i valuesAsNumbers = _mm_subs_epu16(blended, _mm_set1_epi8('0'));

			// convert the pairs of values into a single value
			const __m128i multPow10 = _mm_setr_epi8(10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 0, 0);

			const __m128i numbers = _mm_maddubs_epi16(valuesAsNumbers, multPow10);
			// numbers = 16-bit numbers, 0-5 = grid required counts, 6 = height, 7 = not used

			// multiply by grid counts
			const __m128i result = _mm_madd_epi16(numbers, newCounts);
			// result = 32-bit numbers, 0-2 = partial total required grid counts, 3 = area

			int pc1 = _mm_extract_epi32(result, 0);
			int pc2 = _mm_extract_epi32(result, 1);
			int pc3 = _mm_extract_epi32(result, 2);
			int area = _mm_extract_epi32(result, 3);

			if (pc1 + pc2 + pc3 <= area)
			{
				part1++;
			}

			input += 21; // skip whole line
			input++;	 // skip '\n'
		}

		return {part1, part2};
	}
};
