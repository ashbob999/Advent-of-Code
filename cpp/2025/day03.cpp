#include "../aocHelper.h"

inline void convertToNums(const char* input, uint8_t* output)
{
	const __m256i zeroChars = _mm256_set1_epi8('0');

	__m256i vec = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input));

	__m256i res = _mm256_sub_epi8(vec, zeroChars);

	_mm256_storeu_si256(reinterpret_cast<__m256i*>(output), res);
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
			std::array<uint8_t, TargetLength + 1> maxLine{};

			for (uint8_t index = 0; index < Length; index++)
			{
				auto& v = line[index];

				maxLine.back() = v;

				for (uint8_t i = 1; i < maxLine.size(); i++)
				{
					auto& prev = maxLine[i - 1];
					auto& curr = maxLine[i];

					if (prev < curr)
					{
						std::copy(maxLine.begin() + (i), maxLine.end(), maxLine.begin() + (i - 1));
						maxLine.back() = v;

						break;
					}
				}
			}

			long long total = 0;
			for (uint8_t i = 0; i < TargetLength; i++)
			{
				total *= 10;
				total += maxLine[i];
			}

			part2 += total;
		}

		return {part1, part2};
	}
};
