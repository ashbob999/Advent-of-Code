#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		enum class Dir
		{
			Forward,
			Down,
			Up,
		};

		vector<pair<Dir, int>> moves;

		while (*input != '\0')
		{
			Dir dir;

			if (*input == 'f') // forward
			{
				dir = Dir::Forward;
				input += 8; // skip 'forward '
			}
			else if (*input == 'd') // down
			{
				dir = Dir::Down;
				input += 5; // skip 'down '
			}
			else // up
			{
				dir = Dir::Up;
				input += 3; // skip 'up '
			}

			int amount = numericParse<int>(input);

			moves.push_back({ dir, amount });

			input++; // skip '\n'
		}

		// part 1
		int hor = 0;
		int dep = 0;

		for (auto& m : moves)
		{
			switch (m.first)
			{
				case Dir::Forward:
				{
					hor += m.second;
					break;
				}
				case Dir::Down:
				{
					dep += m.second;
					break;
				}
				case Dir::Up:
				{
					dep -= m.second;
					break;
				}
			}
		}

		part1 = hor * dep;

		// part 2
		hor = 0;
		dep = 0;
		int aim = 0;

		for (auto& m : moves)
		{
			switch (m.first)
			{
				case Dir::Forward:
				{
					hor += m.second;
					dep += aim * m.second;
					break;
				}
				case Dir::Down:
				{
					aim += m.second;
					break;
				}
				case Dir::Up:
				{
					aim -= m.second;
					break;
				}
			}
		}

		part2 = hor * dep;

		return { part1, part2 };
	}
};
