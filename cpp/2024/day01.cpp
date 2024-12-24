#include "../aocHelper.h"

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<int> vals1{};
		std::vector<int> vals2{};

		vals1.reserve(1000);
		vals2.reserve(1000);

		while (*input != '\0')
		{
			int v1 = numericParse<int>(input);
			input += 3; // skip '   '
			int v2 = numericParse<int>(input);

			vals1.push_back(v1);
			vals2.push_back(v2);

			input++; // skip '\n'
		}

		std::sort(vals1.begin(), vals1.end());
		std::sort(vals2.begin(), vals2.end());

		for (size_t i = 0; i < vals1.size(); i += 8)
		{
			__m256i v1 = _mm256_loadu_epi32(vals1.data() + i);
			__m256i v2 = _mm256_loadu_epi32(vals2.data() + i);

			__m256i res = _mm256_abs_epi32(_mm256_sub_epi32(v1, v2));

			__m256i combined = _mm256_hadd_epi32(res, res);

			long long total = _mm256_extract_epi32(combined, 0) + _mm256_extract_epi32(combined, 1) +
				_mm256_extract_epi32(combined, 4) + _mm256_extract_epi32(combined, 5);

			part1 += total;
		}

		size_t i = 0;
		size_t j = 0;

		while (i < vals1.size())
		{
			int v = vals1[i];

			// skip to after v
			while (j < vals2.size() && v >= vals2[j])
			{
				if (vals2[j] == v)
				{
					part2 += v;
				}

				j++;
			}

			if (j >= vals2.size())
			{
				break;
			}

			// skip over duplicate values
			while (i < vals1.size() && vals1[i] == v)
			{
				i++;
			}
		}

		return {part1, part2};
	}
};
