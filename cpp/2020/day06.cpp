#include "../aocHelper.h"

class Day06 : public BaseDay
{
public:
	Day06() : BaseDay("06") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		bitset<26> set1;
		bitset<26> set2;

		bitset<26> line;
		bool first = true;

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				part1 += set1.count();
				part2 += set2.count();

				set1.reset();
				set2.reset();

				first = true;

				input++;
			}
			else
			{
				line.set(*input - 'a');
				input++;

				if (*input == '\n') // end of line
				{
					set1 |= line;

					if (first)
					{
						set2 |= line;
						first = false;
					}
					else
					{
						set2 &= line;
					}

					line.reset();
					input++;
				}
			}
		}

		part1 += set1.count();
		part2 += set2.count();

		return { part1, part2 };
	}
};
