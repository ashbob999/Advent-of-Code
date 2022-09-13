#include "../aocHelper.h"

class Day09 : public BaseDay
{
public:
	Day09() : BaseDay("09") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<vector<int>> heights;

		uint32_t width = 0;
		uint32_t height = 0;

		while (*input != '\0')
		{
			heights.push_back({});
			height++;
			width = 0;

			while (*input != '\n')
			{
				int n = *input - '0';
				heights.back().push_back(n);
				input++;
				width++;
			}

			input++; // skip '\n'
		}

		vector<pair<uint32_t, uint32_t>> low_points;

		// part 1
		constexpr array<array<int, 2>, 4> adj = { { {0, 1}, {0, -1}, {1, 0}, {-1, 0} } };

		auto check_adj = [&](uint32_t x, uint32_t y)
		{
			int low_count = 0;
			int adj_count = 0;

			for (auto& ad : adj)
			{
				uint32_t nx = x + ad[0];
				uint32_t ny = y + ad[1];

				if (nx >= 0 && nx < width && ny >= 0 && ny < height)
				{
					adj_count++;
					if (heights[y][x] < heights[ny][nx])
					{
						low_count++;
					}
				}
			}

			return low_count == adj_count;
		};

		for (uint32_t y = 0; y < height; y++)
		{
			for (uint32_t x = 0; x < height; x++)
			{
				if (check_adj(x, y))
				{
					low_points.push_back({ x, y });
					part1 += 1 + heights[y][x];
				}
			}
		}

		// part 2
		auto get_adj = [&](uint64_t pos)
		{
			vector<uint64_t> ad;

			for (auto& a : adj)
			{
				uint32_t nx = (pos >> 32) + a[0];
				uint32_t ny = (pos & 0xffffffff) + a[1];

				if (nx >= 0 && nx < width && ny >= 0 && ny < height)
				{
					ad.push_back((uint64_t) nx << 32 | ny);
				}
			}

			return ad;
		};

		auto get_basin = [&](uint64_t pos)
		{
			unordered_set<uint64_t> basin;
			basin.insert(pos);

			deque<uint64_t> to_check;
			to_check.push_back(pos);

			unordered_set<uint64_t> checked;

			while (to_check.size() > 0)
			{
				uint64_t curr_pos = to_check.front();
				to_check.pop_front();

				checked.insert(curr_pos);

				int level = heights[curr_pos & 0xffffffff][curr_pos >> 32];

				for (auto& np : get_adj(curr_pos))
				{
					if (!checked.contains(np))
					{
						int n_level = heights[np & 0xffffffff][np >> 32];
						if (n_level > level && n_level < 9)
						{
							basin.insert(np);
							to_check.push_back(np);
						}
					}
				}
			}

			return basin;
		};

		vector<unordered_set<uint64_t>> basins;

		for (auto& lp : low_points)
		{
			basins.push_back(get_basin((uint64_t) lp.first << 32 | lp.second));
		}

		sort(basins.begin(), basins.end(), [](const unordered_set<uint64_t>& a, const unordered_set<uint64_t>& b)
		{
			return a.size() > b.size();
		});

		part2 = 1;
		for (int i = 0; i < 3; i++)
		{
			part2 *= basins[i].size();
		}

		return { part1, part2 };
	}
};
