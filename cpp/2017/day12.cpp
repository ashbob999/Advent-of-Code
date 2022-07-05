#include "../aocHelper.h"

class Day12 : public BaseDay
{
public:
	Day12() : BaseDay("12") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_map<int, vector<int>> pipes;

		// parse input
		while (*input != '\0')
		{
			int id = numericParse<int>(input);

			input += 5; // skip " <-> "

			pipes[id] = {};

			while (*input != '\n')
			{
				int v = numericParse<int>(input);
				pipes[id].push_back(v);

				if (*input == ',')
				{
					input += 2; // skip ", "
				}
			}

			input++; // skip '\n'
		}

		auto bfs_group = [&pipes](int target)
		{
			unordered_set<int> visited;

			deque<int> to_check;
			to_check.insert(to_check.end(), pipes[target].begin(), pipes[target].end());

			while (to_check.size() > 0)
			{
				int curr_value = to_check.front();
				to_check.pop_front();

				visited.insert(curr_value);

				for (auto& t : pipes[curr_value])
				{
					if (!visited.contains(t))
					{
						to_check.push_back(t);
					}
				}
			}

			return visited;
		};

		// part 1
		unordered_set<int> group_0 = bfs_group(0);
		part1 = group_0.size();

		// part 2
		unordered_set<int> all_values;
		for (auto& p : pipes)
		{
			all_values.insert(p.first);
		}

		while (all_values.size() > 0)
		{
			int curr_value = *all_values.begin();

			unordered_set<int> group_set = bfs_group(curr_value);

			part2++;

			for (auto& v : group_set)
			{
				all_values.erase(v);
			}
		}

		return { part1, part2 };
	}
};
