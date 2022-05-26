#include "../aocHelper.h"

class Day15 : public BaseDay
{
public:
	Day15() : BaseDay("15") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct disc
		{
			long long id;
			long long positions;
			long position;
		};

		vector<disc> discs;

		// parse input
		while (*input != '\0')
		{
			input += 6; // skip "Disc #"
			long long id = numericParse<long long>(input);
			input += 5; // skip " has "
			long long positions = numericParse<long long>(input);
			input += 20; // skip " positions; at time="
			long long time = numericParse<long long>(input); // is ignored
			input += 20; // skip ", it is at position "
			long long position = numericParse<long long>(input);

			discs.emplace_back(id, positions, position);

			input += 2; // skip ".\n"
		}

		auto solve = [](vector<disc>& discs)
		{
			long long t = 0;
			while (true)
			{
				if (all_of(discs.begin(), discs.end(), [&](const disc& d)
				{
					return (t + d.id + d.position) % d.positions == 0;
				}))
				{
					return t;
				}

				t++;
			}
		};

		// part 1
		part1 = solve(discs);

		// part 2
		discs.emplace_back(discs.back().id + 1, 11, 0);
		part2 = solve(discs);

		return { part1, part2 };
	}
};
