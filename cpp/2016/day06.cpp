#include "../aocHelper.h"

class Day06 : public BaseDay
{
public:
	Day06() : BaseDay("06") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<unordered_map<char, int>> freq;
		freq.resize(8);

		// parse input
		int index = 0;

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				index = 0;
			}
			else
			{
				if (freq[index].contains(*input))
				{
					freq[index][*input]++;
				}
				else
				{
					freq[index][*input] = 1;
				}

				index++;
			}
			input++;
		}

		// part 1
		char p1_out[8];

		for (int i = 0; i < 8; i++)
		{
			p1_out[i] = max_element(freq[i].begin(), freq[i].end(), [&](const auto& a, const auto& b)
			{
				return a.second < b.second;
			})->first;
		}

		memcpy(this->stringResult.first, p1_out, 8);

		// part 2
		char p2_out[8];

		for (int i = 0; i < 8; i++)
		{
			p2_out[i] = min_element(freq[i].begin(), freq[i].end(), [&](const auto& a, const auto& b)
			{
				return a.second < b.second;
			})->first;
		}

		memcpy(this->stringResult.second, p2_out, 8);

		return { part1, part2 };
	}
};
