#include "../aocHelper.h"

#include <immintrin.h>

class Day13 : public BaseDay
{
public:
	Day13() : BaseDay("13") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		uint64_t number = numericParse<uint64_t>(input);

		auto check = [&](uint64_t pos)
		{
			uint64_t x = (pos >> 32) & 0xffffffff;
			uint64_t y = pos & 0xffffffff;

			uint64_t res = x * x + 3 * x + 2 * x * y + y + y * y;
			res += number;

			int bit_count = _mm_popcnt_u64(res);

			if (bit_count % 2 == 0)
			{
				return true;
			}
			else
			{
				return false;
			}
		};

		auto search = [&](uint64_t start, uint64_t end)
		{
			deque<uint64_t> to_check;
			to_check.push_back(start);

			unordered_map<uint64_t, int> dists;
			dists[start] = 0;

			while (to_check.size() > 0)
			{
				uint64_t curr_pos = to_check.front();
				to_check.pop_front();

				int curr_dist = dists[curr_pos];

				uint64_t x_pos = (curr_pos >> 32) & 0xffffffff;
				uint64_t y_pos = curr_pos & 0xffffffff;

				vector<uint64_t> adj;

				int x_start = x_pos > 0 ? -1 : 1;
				for (int x = x_start; x <= 1; x += 2)
				{
					uint64_t new_pos = ((x_pos + x) << 32) | (y_pos & 0xffffffff);
					if (check(new_pos))
					{
						adj.push_back(new_pos);
					}
				}

				int y_start = y_pos > 0 ? -1 : 1;
				for (int y = y_start; y <= 1; y += 2)
				{
					uint64_t new_pos = (x_pos << 32) | ((y_pos + y) & 0xffffffff);
					if (check(new_pos))
					{
						adj.push_back(new_pos);
					}
				}

				for (auto& np : adj)
				{
					if (np == end)
					{
						return curr_dist + 1;
					}
					else
					{
						if (!dists.contains(np) || curr_dist + 1 < dists[np])
						{
							to_check.push_back(np);
							dists[np] = curr_dist + 1;
						}
					}
				}
			}

			return 0;
		};

		auto bfs = [&](uint64_t start, int limit)
		{
			deque<uint64_t> to_check;
			to_check.push_back(start);

			unordered_map<uint64_t, int> dists;
			dists[start] = 0;

			while (to_check.size() > 0)
			{
				uint64_t curr_pos = to_check.front();
				to_check.pop_front();

				int curr_dist = dists[curr_pos];

				uint64_t x_pos = (curr_pos >> 32) & 0xffffffff;
				uint64_t y_pos = curr_pos & 0xffffffff;

				vector<uint64_t> adj;

				int x_start = x_pos > 0 ? -1 : 1;
				for (int x = x_start; x <= 1; x += 2)
				{
					uint64_t new_pos = ((x_pos + x) << 32) | (y_pos & 0xffffffff);
					if (check(new_pos))
					{
						adj.push_back(new_pos);
					}
				}

				int y_start = y_pos > 0 ? -1 : 1;
				for (int y = y_start; y <= 1; y += 2)
				{
					uint64_t new_pos = (x_pos << 32) | ((y_pos + y) & 0xffffffff);
					if (check(new_pos))
					{
						adj.push_back(new_pos);
					}
				}

				for (auto& np : adj)
				{
					if (curr_dist + 1 <= limit)
					{
						if (!dists.contains(np) || curr_dist + 1 < dists[np])
						{
							to_check.push_back(np);
							dists[np] = curr_dist + 1;
						}
					}
				}
			}

			return dists.size();
		};

		// part 1
		uint64_t start_x = 1;
		uint64_t start_y = 1;

		uint64_t target_x = 31;
		uint64_t target_y = 39;

		uint64_t start_pos = (start_x << 32) | (start_y & 0xffffffff);
		uint64_t target_pos = (target_x << 32) | (target_y & 0xffffffff);

		part1 = search(start_pos, target_pos);

		// part 2
		part2 = bfs(start_pos, 50);

		return { part1, part2 };
	}
};
