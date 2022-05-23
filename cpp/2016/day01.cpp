#include "../aocHelper.h"

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<std::pair<bool, int32_t>> dirs;

		// parse input
		while (*input != '\0')
		{
			pair<bool, int32_t> dir;

			if (*input == 'L')
			{
				dir.first = true;
			}
			else
			{
				dir.first = false;
			}

			input++;

			dir.second = numericParse<int32_t>(input);

			dirs.push_back(dir);

			if (*input == '\n')
			{
				break;
			}
			input += 2; // skip ", "
		}

		// cheaty hack because packing wouldn't work
		union
		{
			int32_t ind[2] = { 0,0 };
			uint64_t mixed;
		} pos;

		// part 1
		pos = { 0, 0 };
		int facing = 0;

		for (auto& dir : dirs)
		{
			if (dir.first)
			{
				facing--;
			}
			else
			{
				facing++;
			}

			facing %= 4;
			facing += (facing < 0) ? 4 : 0;

			int index = 1;

			if (facing % 2 == 0)
			{
				index = 0;
			}

			int sign = -1;

			if (facing <= 1)
			{
				sign = 1;
			}

			pos.ind[index] += dir.second * sign;
		}

		part1 = abs(pos.ind[0]) + abs(pos.ind[1]);

		// part 2
		pos = { 0, 0 };
		facing = 0;
		unordered_set<uint64_t> visited;
		visited.insert(pos.mixed);

		for (auto& dir : dirs)
		{
			if (dir.first)
			{
				facing--;
			}
			else
			{
				facing++;
			}

			facing %= 4;
			facing += (facing < 0) ? 4 : 0;

			int index = 1;

			if (facing % 2 == 0)
			{
				index = 0;
			}

			int sign = -1;

			if (facing <= 1)
			{
				sign = 1;
			}

			bool found = false;

			for (int i = 0; i < dir.second; i++)
			{
				pos.ind[index] += sign;
				if (visited.contains(pos.mixed))
				{
					found = true;
					break;
				}
				else
				{
					visited.insert(pos.mixed);
				}
			}

			if (found)
			{
				break;
			}
		}

		part2 = abs(pos.ind[0]) + abs(pos.ind[1]);

		return { part1, part2 };
	}
};
