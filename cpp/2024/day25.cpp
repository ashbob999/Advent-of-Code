#include "../aocHelper.h"

#include <cmath>
#include <immintrin.h>

class Day25 : public BaseDay
{
public:
	Day25() : BaseDay("25") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr size_t Width = 5;
		constexpr size_t Height = 7;
		constexpr size_t BytesPerGrid = (Width + 1) * Height;

		constexpr size_t Count = 500;

		constexpr size_t CountPer = Count / 2;
		static_assert(sizeof(uint64_t) * 8 == 256 / 4);
		constexpr size_t CountPerPadMul4 =
			(CountPer % 4 == 0) ? CountPer : (static_cast<size_t>(static_cast<float>(CountPer / 4.0f) + 1) * 4);
		std::array<uint64_t, CountPerPadMul4> locks{};
		std::array<uint64_t, CountPerPadMul4> keys{};

		size_t locksIndex = 0;
		size_t keysIndex = 0;

		const __m256i hashMask = _mm256_set1_epi8('#');

		constexpr uint64_t FirstRowMask = (1ull << Width) - 1;
		static_assert(FirstRowMask == 0b11111);

		static_assert(BytesPerGrid - 32 == 10);
		const __m256i blendClearMask = _mm256_set_epi8(
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0xFF,
			0xFF,
			0xFF,
			0xFF,
			0xFF,
			0xFF,
			0xFF,
			0xFF,
			0xFF,
			0xFF);

		// parse input
		while (*input != '\0')
		{
			__m256i gridLow = _mm256_loadu_si256(reinterpret_cast<__m256i*>(input));
			// Mask of higher bits, because they are outisde of the grid (assumes the input has at least 32-bytes
			// padding)
			__m256i gridHigh = _mm256_loadu_si256(reinterpret_cast<__m256i*>(input + 32));
			// Keep 10 lowest bits

			gridHigh = _mm256_blendv_epi8(_mm256_setzero_si256(), gridHigh, blendClearMask);

			int lowBits = _mm256_movemask_epi8(_mm256_cmpeq_epi8(gridLow, hashMask));
			int highBits = _mm256_movemask_epi8(_mm256_cmpeq_epi8(gridHigh, hashMask));

			uint64_t grid =
				(static_cast<uint64_t>(static_cast<uint32_t>(highBits)) << 32) | static_cast<uint32_t>(lowBits);

			bool isKey = (grid & FirstRowMask) == 0;

			if (isKey)
			{
				keys[keysIndex] = grid;
				keysIndex++;
			}
			else
			{
				locks[locksIndex] = grid;
				locksIndex++;
			}

			input += BytesPerGrid;
			input++; // skip '\n'
		}

		static_assert(CountPerPadMul4 - CountPer == 2);
		locks[CountPerPadMul4 - 2] = std::numeric_limits<uint64_t>::max();
		locks[CountPerPadMul4 - 1] = std::numeric_limits<uint64_t>::max();

		static_assert(CountPerPadMul4 % 3 == 0);
		keys[CountPerPadMul4 - 2] = std::numeric_limits<uint64_t>::max();
		keys[CountPerPadMul4 - 1] = std::numeric_limits<uint64_t>::max();

		// part 1

		static_assert(CountPer % 2 == 0);

		long long part1_1 = 0;
		long long part1_2 = 0;

		const __m256i andMask = _mm256_set1_epi64x(1);

		__m256i values1 = _mm256_setzero_si256();
		__m256i values2 = _mm256_setzero_si256();
		__m256i values3 = _mm256_setzero_si256();

		for (size_t i = 0; i < CountPerPadMul4; i += 4)
		{
			__m256i lockReg = _mm256_loadu_si256(reinterpret_cast<__m256i*>(locks.data() + i));

			for (size_t j = 0; j < CountPerPadMul4; j += 3)
			{
				__m256i keyReg1 = _mm256_set1_epi64x(keys[j]);
				__m256i keyReg2 = _mm256_set1_epi64x(keys[j + 1]);
				__m256i keyReg3 = _mm256_set1_epi64x(keys[j + 2]);

				// bitwise-& them together, 64-bit == 0 then the key fits
				__m256i res1 = _mm256_and_si256(lockReg, keyReg1);
				__m256i res2 = _mm256_and_si256(lockReg, keyReg2);
				__m256i res3 = _mm256_and_si256(lockReg, keyReg3);

				// Generate 64-bit mask of keys that fit
				__m256i fitMask1 = _mm256_cmpeq_epi64(res1, _mm256_setzero_si256());
				__m256i fitMask2 = _mm256_cmpeq_epi64(res2, _mm256_setzero_si256());
				__m256i fitMask3 = _mm256_cmpeq_epi64(res3, _mm256_setzero_si256());

				// And each 64-bit value in mask by 1
				__m256i andV1 = _mm256_and_si256(fitMask1, andMask);
				__m256i andV2 = _mm256_and_si256(fitMask2, andMask);
				__m256i andV3 = _mm256_and_si256(fitMask3, andMask);

				values1 = _mm256_add_epi64(values1, andV1);
				values2 = _mm256_add_epi64(values2, andV2);
				values3 = _mm256_add_epi64(values3, andV3);
			}
		}

		__m256i values = _mm256_add_epi64(values1, values2);
		values = _mm256_add_epi64(values, values3);
		part1 = _mm256_extract_epi64(values, 0) + _mm256_extract_epi64(values, 1) + _mm256_extract_epi64(values, 2) +
			_mm256_extract_epi64(values, 3);

		return {part1, part2};
	}
};