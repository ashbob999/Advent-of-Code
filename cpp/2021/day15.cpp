#include "../aocHelper.h"
#include <queue>

class Day15 : public BaseDay
{
public:
	Day15() : BaseDay("15") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<vector<int>> grid;
		grid.push_back({});

		// parse input
		while (*input != '\0')
		{
			if (*input == '\n')
			{
				grid.push_back({});
			}
			else
			{
				int n = *input - '0';
				grid.back().push_back(n);
			}

			input++;
		}

		grid.pop_back();

		int width = grid[0].size();
		int height = grid.size();

		static constexpr array<pair<int, int>, 4> dirs = { { {0, 1}, {0, -1}, {-1, 0}, {1, 0} } };

		auto create_path = [](unordered_map<uint32_t, uint32_t>& came_from, uint32_t current) -> vector<uint32_t>
		{
			vector<uint32_t> path = { current };

			while (came_from.contains(current))
			{
				current = came_from[current];
				path.insert(path.begin(), current);
			}

			return path;
		};

		auto h_func = [](uint32_t pos)
		{
			return (pos >> 16) + (pos & 0xffff);
		};

		auto a_star = [&h_func, &create_path](vector<vector<int>>& grid, uint32_t start, uint32_t end)->vector<uint32_t>
		{
			int width = grid[0].size();
			int height = grid.size();

			unordered_set<uint32_t> in_heap;
			priority_queue<pair<int, uint32_t>, vector<pair<int, uint32_t>>, std::greater<>> heap;

			in_heap.insert(start);
			heap.push({ 0, start });

			unordered_map<uint32_t, uint32_t> came_from;

			unordered_map<uint32_t, int> g_score;
			g_score[start] = 0;

			unordered_map<uint32_t, int> f_score;
			f_score[start] = h_func(start);

			while (heap.size() > 0)
			{
				auto [curr_dist, curr] = heap.top();
				heap.pop();
				in_heap.erase(curr);

				if (curr == end)
				{
					return create_path(came_from, curr);
				}

				int x = (curr >> 16);
				int y = (curr & 0xffff);

				for (auto& dir : dirs)
				{
					int nx = x + dir.first;
					int ny = y + dir.second;

					if (nx >= 0 && nx < width && ny >= 0 && ny < height)
					{
						int tg_score = g_score[curr] + grid[ny][nx];

						uint32_t pos = ((uint32_t) nx << 16) | ((uint32_t) ny & 0xffff);

						if (!g_score.contains(pos) || tg_score < g_score[pos])
						{
							came_from[pos] = curr;

							g_score[pos] = tg_score;

							f_score[pos] = tg_score + h_func(pos);

							if (!in_heap.contains(pos))
							{
								heap.push({ f_score[pos], pos });
								in_heap.insert(pos);
							}
						}
					}
				}
			}

			return {};
		};

		auto calc_risk = [&a_star](vector<vector<int>>& grid, pair<int, int> start, pair<int, int> end)
		{
			int risk = 0;

			uint32_t start_pos = (start.first << 16) | (start.second & 0xffff);
			uint32_t end_pos = (end.first << 16) | (end.second & 0xffff);

			auto path = a_star(grid, start_pos, end_pos);

			for (auto& p : path)
			{
				if (p != start_pos)
				{
					int x = p >> 16;
					int y = p & 0xffff;
					risk += grid[y][x];
				}
			}

			return risk;
		};

		// part 1
		part1 = calc_risk(grid, { 0, 0 }, { width - 1, height - 1 });

		// part 2
		vector<vector<int>> grid5x5;
		grid5x5.resize(height * 5);

		for (int y = 0; y < height * 5; y++)
		{
			grid5x5[y].resize(width * 5);
		}

		for (int y = 0; y < 5; y++)
		{
			for (int x = 0; x < 5; x++)
			{
				int inc = x + y;

				for (int yp = 0; yp < height; yp++)
				{
					for (int xp = 0; xp < width; xp++)
					{
						if (grid[yp][xp] + inc > 9)
						{
							grid5x5[height * y + yp][width * x + xp] = 1 + (grid[yp][xp] + inc) % 10;
						}
						else
						{
							grid5x5[height * y + yp][width * x + xp] = grid[yp][xp] + inc;
						}

					}
				}
			}
		}

		part2 = calc_risk(grid5x5, { 0, 0 }, { width * 5 - 1, height * 5 - 1 });

		return { part1, part2 };
	}
};
