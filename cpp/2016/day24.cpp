#include "../aocHelper.h"

// gets n-lenght combinations of an array
// from: https://stackoverflow.com/questions/9430568/generating-combinations-in-c#answer-9432150
struct combinations
{
	typedef vector<int> combination_t;

	// initialize status
	combinations(int N, int R) :
		completed(N < 1 || R > N),
		generated(0),
		N(N), R(R)
	{
		for (int c = 1; c <= R; ++c)
			curr.push_back(c);
	}

	// true while there are more solutions
	bool completed;

	// count how many generated
	int generated;

	// get current and compute next combination
	combination_t next()
	{
		combination_t ret = curr;

		// find what to increment
		completed = true;
		for (int i = R - 1; i >= 0; --i)
			if (curr[i] < N - R + i + 1)
			{
				int j = curr[i] + 1;
				while (i <= R - 1)
					curr[i++] = j++;
				completed = false;
				++generated;
				break;
			}

		return ret;
	}

private:

	int N, R;
	combination_t curr;
};

class Day24 : public BaseDay
{
public:
	Day24() : BaseDay("24") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int width = 181;
		constexpr int height = 37;

		//char grid[height][width];
		vector<vector<char>> grid;
		grid.reserve(height);

		grid.push_back({});
		grid[0].reserve(width);

		unordered_map<int, uint64_t> number_locations;

		// parse input
		int x = 0;
		int y = 0;

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				y++;
				x = 0;
				grid.push_back({});
				grid[y].reserve(width);
			}
			else
			{
				grid[y].push_back(*input);

				if (*input >= '0' && *input <= '9')
				{
					number_locations[*input - '0'] = (uint64_t) x << 32 | ((uint64_t) y & 0xffffffff);
				}

				x++;
			}

			input++;
		}

		grid.pop_back();

		auto bfs = [](uint64_t start, uint64_t end, vector<vector<char>>& grid)
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

				vector<uint64_t> adj;

				uint64_t x_pos = curr_pos >> 32;
				uint64_t y_pos = curr_pos & 0xffffffff;

				for (int y = -1; y <= 1; y += 2)
				{
					if (y_pos + y >= 0 && y_pos + y < height)
					{
						uint64_t new_pos = ((uint64_t) x_pos << 32) | ((uint64_t) (y_pos + y) & 0xffffffff);
						if (grid[y_pos + y][x_pos] != '#')
						{
							adj.push_back(new_pos);
						}
					}
				}

				for (int x = -1; x <= 1; x += 2)
				{
					if (x_pos + x >= 0 && x_pos + x < width)
					{
						uint64_t new_pos = ((uint64_t) (x_pos + x) << 32) | ((uint64_t) y_pos & 0xffffffff);
						if (grid[y_pos][x_pos + x] != '#')
						{
							adj.push_back(new_pos);
						}
					}
				}

				for (auto& ad : adj)
				{
					if (ad == end)
					{
						return curr_dist + 1;
					}
					else
					{
						if (!dists.contains(ad) || curr_dist + 1 < dists[ad])
						{
							to_check.push_back(ad);
							dists[ad] = curr_dist + 1;
						}
					}
				}
			}
		};

		vector<int> targets;
		for (auto& p : number_locations)
		{
			if (p.first != 0)
			{
				targets.push_back(p.first);
			}
		}

		int n = targets.size();
		int r = 2;

		map<pair<int, int>, int> dists;

		// get dist for all a->b locations
		combinations comb(n, r);

		while (!comb.completed)
		{
			combinations::combination_t c = comb.next();

			uint64_t start = number_locations[c[0]];
			uint64_t end = number_locations[c[1]];

			int dist = bfs(start, end, grid);
			dists[{c[0], c[1]}] = dist;
			dists[{c[1], c[0]}] = dist;
		}

		// add dists for all 0->locations
		for (auto& t : targets)
		{
			uint64_t start = number_locations[0];
			uint64_t end = number_locations[t];

			int dist = bfs(start, end, grid);
			dists[{0, t}] = dist;
			dists[{t, 0}] = dist;
		}

		// part 1
		int min_dist = 100000000;

		sort(targets.begin(), targets.end());

		do
		{
			int curr_dist = dists[{0, targets[0]}];
			for (int i = 0; i < targets.size() - 1; i++)
			{
				curr_dist += dists[{targets[i], targets[i + 1]}];
			}

			if (curr_dist < min_dist)
			{
				min_dist = curr_dist;
			}

		} while (next_permutation(targets.begin(), targets.end()));

		part1 = min_dist;

		// part 2
		min_dist = 100000000;

		sort(targets.begin(), targets.end());

		do
		{
			int curr_dist = dists[{0, targets[0]}];
			for (int i = 0; i < targets.size() - 1; i++)
			{
				curr_dist += dists[{targets[i], targets[i + 1]}];
			}
			curr_dist += dists[{targets.back(), 0}];

			if (curr_dist < min_dist)
			{
				min_dist = curr_dist;
			}

		} while (next_permutation(targets.begin(), targets.end()));

		part2 = min_dist;

		return { part1, part2 };
	}
};
