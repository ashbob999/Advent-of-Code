#include "../aocHelper.h"

class Day09 : public BaseDay
{
public:
	Day09() : BaseDay("09") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		function<long long(char*, int, bool)> decompress;
		decompress = [&](char* data, int length, bool recursive)
		{
			long long char_count = 0;

			int i = 0;

			while (i < length)
			{
				if (data[i] >= 'A' && data[i] <= 'Z')
				{
					char_count++;
					i++;
				}
				else if (data[i] == '(')
				{
					// find next ')'
					int end_index = i + 1;
					while (data[end_index] != ')')
					{
						end_index++;
					}

					char* cp = data + i + 1;
					long long count = numericParse<long long>(cp);
					cp++;
					long long times = numericParse<long long>(cp);
					i += end_index - i + 1;

					if (recursive)
					{
						char_count += decompress(data + i, count, recursive) * times;
					}
					else
					{
						char_count += count * times;
					}

					i += count;
				}
				else
				{
					i++;
				}
			}

			return char_count;
		};

		// part 1
		part1 = decompress(input, this->length, false);

		// part 2
		part2 = decompress(input, this->length, true);

		return { part1, part2 };
	}
};
