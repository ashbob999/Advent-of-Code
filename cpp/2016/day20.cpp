#include "../aocHelper.h"

class Day20 : public BaseDay
{
public:
	Day20() : BaseDay("20") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<pair<uint64_t, uint64_t>> blocked_ips;

		// parse input
		while (*input != '\0')
		{
			uint64_t start = numericParse<uint64_t>(input);
			input++; // skip '-'
			uint64_t end = numericParse<uint64_t>(input);

			blocked_ips.emplace_back(start, end);
			input++; // skip '\n'
		}

		sort(blocked_ips.begin(), blocked_ips.end());

		vector<pair<uint64_t, uint64_t>> ranges;
		ranges.push_back(blocked_ips.front());

		for (auto& curr_range : blocked_ips)
		{
			auto& prev_range = ranges.back();

			if ((uint64_t) curr_range.first <= (uint64_t) prev_range.second + 1ULL)
			{
				prev_range.second = max(prev_range.second, curr_range.second);
			}
			else
			{
				ranges.push_back(curr_range);
			}
		}

		// part 1
		part1 = ranges[0].second + 1;

		// part 2
		for (int i = 0; i < ranges.size() - 1; i++)
		{
			part2 += ranges[i + 1].first - ranges[i].second - 1;
		}

		part2 += 4294967295ULL - ranges.back().second;

		return { part1, part2 };
	}
};
