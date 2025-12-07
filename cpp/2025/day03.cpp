#include "../aocHelper.h"

inline void convertToNums(const char* input, uint8_t* output)
{
	const __m256i zeroChars = _mm256_set1_epi8('0');

	__m256i vec = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input));

	__m256i res = _mm256_sub_epi8(vec, zeroChars);

	_mm256_storeu_si256(reinterpret_cast<__m256i*>(output), res);
}

inline __m128i bitMaskToByteMask16(int m)
{
	// https://stackoverflow.com/questions/72898737/intrinsic-inverse-to-mm-movemask-epi8
	const __m128i sel = _mm_set1_epi64x(0x8040201008040201);
	return _mm_cmpeq_epi8(
		_mm_and_si128(_mm_shuffle_epi8(_mm_cvtsi32_si128(m), _mm_set_epi64x(0x0101010101010101, 0)), sel),
		sel);
}

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// length = 100, bits = 8*100=800, ~4*256, 4*256/8 = 128
		std::vector<std::array<uint8_t, 128>> lines{};

		constexpr uint8_t Length = 100;

		while (*input != '\0')
		{
			std::array<uint8_t, 128> line{};

			convertToNums(input + 0, line.data() + 0);
			convertToNums(input + 32, line.data() + 32);
			convertToNums(input + 64, line.data() + 64);
			convertToNums(input + 96, line.data() + 96);

			std::memset(line.data() + Length, 0, line.size() - Length);

			input += Length; // skip <numbers>
			input++;		 // skip '\n'

			lines.push_back(line);
		}

		// part 1
		for (auto& line : lines)
		{
			uint8_t maxV1Index = 0;
			uint8_t maxV1 = line[maxV1Index];
			for (uint8_t i = 1; i < Length - 1; i++)
			{
				auto v = line[i];
				if (v > maxV1)
				{
					maxV1Index = i;
					maxV1 = v;
				}
			}

			const uint8_t maxV2Index = maxV1Index + 1;
			uint8_t maxV2 = line[maxV2Index];

			for (uint8_t j = maxV2Index + 1; j < Length; j++)
			{
				auto v = line[j];
				if (v > maxV2)
				{
					maxV2 = v;
				}
			}

			uint16_t total = maxV1 * 10 + maxV2;

			part1 += total;
		}

		// part 2

		constexpr uint8_t TargetLength = 12;

		for (auto& line : lines)
		{
			__m128i maxLine = _mm_setzero_si128();
			static_assert(sizeof(maxLine) == 128 / 8);
			static_assert(TargetLength + 1 <= sizeof(maxLine));

			for (uint8_t index = 0; index < Length; index++)
			{
				auto& v = line[index];

				// broadcast value
				const __m128i broadcastValue = _mm_set1_epi8(v);

				// blend into last x bytes (index >=12)
				// because there is no blend_epi8 that takes an immediate value, we use blend_epi16 instead
				maxLine = _mm_blend_epi16(maxLine, broadcastValue, 0b11000000);

				// duplicate (makes a, b)
				const __m128i duplicate = maxLine;

				// shift b right by 1 byte
				const __m128i shifted = _mm_bsrli_si128(duplicate, 1);

				// compare lt
				const __m128i compare = _mm_cmplt_epi8(maxLine, shifted);

				// get movemask
				const int movemask = _mm_movemask_epi8(compare);

				// modify movmask so zero becomes 1<<16

				// get bitindex
				const int bitIndex = _tzcnt_u32(movemask);

				const uint64_t shiftedIndex = static_cast<uint64_t>(1) << bitIndex;
				const int shiftedIndexU32 = static_cast<uint32_t>(shiftedIndex);
				// calc blend mask using index (_mm_blendv_epi8, 0=a, 1=b, bit7 per byte)
				const int newMask = (shiftedIndexU32 - 1) ^ -1;

				const __m128i mask = bitMaskToByteMask16(newMask);

				const __m128i res = _mm_blendv_epi8(maxLine, shifted, mask);

				maxLine = res;
			}

			// Load the data
			__m256i loaded256 = _mm256_zextsi128_si256(maxLine);

			// powers of 10
			// b11 = 1
			// b10 = 10
			// b9  = 100
			// b8  = 1000
			// b7  = 10000
			// b6  = 100000
			// b5  = 1000000
			// b4  = 10000000
			// b3  = 100000000
			// b2  = 1000000000
			// b1  = 10000000000
			// b0  = 100000000000

			//   10    1   10    1   10    1   10    1  100   10   10    1
			// *+ (_mm256_maddubs_epi16)
			//   b0   b1   b2   b3   b4   b5   b6   b7   b8   b9  b10  b11
			// =
			//      s0        s1        s2        s3        s4        s5
			// *+ (_mm256_madd_epi16)
			//     100         1       100         1        10         1
			// =
			//           i0                  i1                  i2
			// * (_mm256_mul_epu32)
			//    100000000               10000                   1
			// =
			//           l0                  l1                  l2

			const __m256i m0 = _mm256_setr_epi8(
				10,
				1,
				10,
				1,
				10,
				1,
				10,
				1,
				100,
				10,
				10,
				1,
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
				0);

			const __m256i values16Bit = _mm256_maddubs_epi16(loaded256, m0);

			const __m256i m1 = _mm256_setr_epi16(100, 1, 100, 1, 10, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

			const __m256i values32Bit = _mm256_madd_epi16(values16Bit, m1);

			const __m256i m2 = _mm256_setr_epi64x(100000000, 10000, 1, 0);

			// _mm256_mul_epu32 takes 64-bit numbers but only uses the lower 32-bits
			const __m256i value64Bit = _mm256_mul_epu32(_mm256_cvtepu32_epi64(_mm256_castsi256_si128(values32Bit)), m2);

			long long total = _mm256_extract_epi64(value64Bit, 0) + _mm256_extract_epi64(value64Bit, 1) +
				_mm256_extract_epi64(value64Bit, 2);

			part2 += total;
		}

		return {part1, part2};
	}
};
