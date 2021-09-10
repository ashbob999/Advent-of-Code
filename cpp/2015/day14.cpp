#include "../aocHelper.h"

class Day14 : public BaseDay
{
public:
	Day14() : BaseDay("14") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct info
		{
			int speed;
			int time;
			int rest;
			int interval;
			int dist_per_interval;
		};

		vector<info> deer_info;

		struct data
		{
			int time = 0;
			int dist = 0;
			bool is_moving = true;
			int points = 0;
		};

		// parse input
		while (*input != '\0')
		{
			string name;

			while (*input != ' ')
			{
				name += *input;
				input++;
			}

			input += 9; // skip ' can fly '

			info i;

			i.speed = numericParse<int>(input);

			input += 10; // skip ' km\s for '

			i.time = numericParse<int>(input);

			input += 33; // skip ' seconds, but then must rest for '

			i.rest = numericParse<int>(input);

			input += 10; // skip ' seconds.\n'

			i.interval = i.time + i.rest;
			i.dist_per_interval = i.speed * i.time;

			// assume no other input line has a reindeer of the same name
			deer_info.push_back(i);
		}

		// part 1
		auto solve_part1 = [&deer_info](int seconds)
		{
			int max_dist = 0;

			for (auto& stats : deer_info)
			{
				//auto& stats = p.second;

				int full_cycles = seconds / stats.interval;
				int rem = stats.interval % seconds;

				int dist = full_cycles * stats.dist_per_interval;

				if (stats.time >= rem) // still flying
				{
					dist += rem * stats.speed;
				}
				else // resting
				{
					dist += stats.dist_per_interval;
				}

				max_dist = max(max_dist, dist);
			}

			return max_dist;
		};

		part1 = solve_part1(2503);

		// part 2
		auto solve_part2 = [&deer_info](int seconds)
		{
			vector<data> deers(deer_info.size());

			for (int i = 0; i < seconds; i++)
			{
				for (int index=0;index<deers.size();index++)
				{
					auto& deer = deers[index];

					if (deer.is_moving) // moving
					{
						deer.time++;
						deer.dist += deer_info[index].speed;

						if (deer.time == deer_info[index].time)
						{
							deer.time = 0;
							deer.is_moving = false; // now resting
						}
					}
					else // resting
					{
						deer.time++;

						if (deer.time == deer_info[index].rest)
						{
							deer.time = 0;
							deer.is_moving = true; // now moving
						}
					}
				}

				// get deers with max distance
				auto it = max_element(deers.begin(), deers.end(), [](const auto& p1, const auto& p2)
				{
					return p1.dist < p2.dist;
				});

				int max_dist = it->dist;

				for_each(deers.begin(), deers.end(), [&max_dist](auto& p)
				{
					if (p.dist == max_dist)
					{
						p.points++;
					}
				});
			}

			auto it = max_element(deers.begin(), deers.end(), [](const auto& p1, const auto& p2)
			{
				return p1.points < p2.points;
			});

			return it->points;
		};

		part2 = solve_part2(2503);

		return { part1, part2 };
	}
};
