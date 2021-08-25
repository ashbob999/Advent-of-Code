#include "../aocHelper.h"

class Day09 : public BaseDay
{
public:
	Day09() : BaseDay("09")
	{}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_map<uint32_t, unordered_map<uint32_t, uint32_t>> distances;

		// parse input;
		while (*input != '\0')
		{
			char *start = input;
			int length = 0;

			while (*input != ' ')
			{
				input++;
				length++;
			}

			uint32_t p1 = 0;

			for (int i = 0; i < 4 && i < length; i++)
			{
				p1 |= (uint8_t) (*(start + i)) << i * 8;
			}

			input += 4;// skip ' to '

			start = input; // reset start
			length = 0; // reset length

			while (*input != ' ')
			{
				input++;
				length++;
			}

			uint32_t p2 = 0;

			for (int i = 0; i < 4 && i < length; i++)
			{
				p2 |= (uint8_t) (*(start + i)) << i * 8;
			}

			input += 3; // skip " = "

			uint32_t dist = numericParse<uint32_t>(input);

			distances[p1][p2] = dist;
			distances[p2][p1] = dist;

			input++; // skip \n
		}

		function<uint32_t(uint32_t, unordered_set<uint32_t>,
		                  uint32_t const &(uint32_t const &, uint32_t const &),
		                  uint32_t)> get_dist;
		get_dist = [&distances, &get_dist](uint32_t curr, unordered_set<uint32_t> visited,
		                                   uint32_t const &(*cmp)(uint32_t const &, uint32_t const &),
		                                   uint32_t start_dist) -> uint32_t
		{
			uint32_t total_dist = start_dist;
			visited.insert(curr);

			if (visited.size() == distances.size())
			{
				return 0;
			}

			for (auto &p : distances[curr])
			{
				auto f = visited.find(p.first);
				if (f == visited.end())
				{
					unordered_set<uint32_t> vc{ visited };

					uint32_t dist = get_dist(p.first, vc, cmp, start_dist) + p.second;
					total_dist = cmp(total_dist, dist);
				}
			}

			return total_dist;
		};

		// part 1
		uint32_t dist = 100000000000;

		for (auto &p : distances)
		{
			dist = min(dist, get_dist(p.first, {}, min<uint32_t>, 100000000000));
		}
		part1 = dist;

		// part 2
		dist = 0;

		for (auto &p : distances)
		{
			dist = max(dist, get_dist(p.first, {}, max<uint32_t>, 0));
		}
		part2 = dist;

		return { part1, part2 };
	}
};
