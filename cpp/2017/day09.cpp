#include "../aocHelper.h"

class Day09 : public BaseDay
{
public:
	Day09() : BaseDay("09") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		string stream;

		// parse input
		while (*input != '\n')
		{
			stream += *input;
			input++;
		}

		auto calc_score = [](string& stream)
		{
			int score = 0;
			int level = 1;

			int garbage_count = 0;
			bool in_garbage = false;

			int i = 0;
			while (i < stream.size())
			{
				if (!in_garbage && stream[i] == '{')
				{
					score += level;
					level++;
				}
				else if (!in_garbage && stream[i] == '}')
				{
					level--;
				}
				else if (!in_garbage && stream[i] == '<')
				{
					in_garbage = true;
				}
				else if (stream[i] == '>')
				{
					in_garbage = false;
				}
				else if (in_garbage && stream[i] == '!')
				{
					i++;
				}
				else if (in_garbage)
				{
					garbage_count++;
				}

				i++;
			}

			return pair<int, int>{ score, garbage_count };
		};

		pair<int, int> res = calc_score(stream);

		// part 1
		part1 = res.first;

		// part 2
		part2 = res.second;

		return { part1, part2 };
	}
};
