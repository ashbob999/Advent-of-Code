#include "../aocHelper.h"

class Day19 : public BaseDay
{
public:
	Day19() : BaseDay("19") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<vector<char>> grid;
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
				grid.back().push_back(*input);
			}
			input++;
		}

		grid.pop_back();

		int width = grid.front().size();
		int height = grid.size();

		array<pair<int, int>, 4> adj = { {{0,-1}, {1,0}, {0,1}, {-1,0} } };

		auto solve = [&grid, &width, &height, &adj]()
		{
			int steps = 1;
			pair<int, int> start_pos{ 0, 0 };
			for (int i = 0; i < width; i++)
			{
				if (grid[0][i] == '|')
				{
					start_pos.first = i;
					break;
				}
			}

			int dir = 2; // down

			string found_chars;
			pair<int, int> curr_pos = start_pos;

			while (true)
			{
				pair<int, int> next_pos;

				switch (dir)
				{
					case 0: // up
					{
						next_pos = { curr_pos.first, curr_pos.second - 1 };
						break;
					}
					case 1: // right
					{
						next_pos = { curr_pos.first + 1, curr_pos.second };
						break;
					}
					case 2: // down
					{
						next_pos = { curr_pos.first, curr_pos.second + 1 };
						break;
					}
					case 3: // left
					{
						next_pos = { curr_pos.first - 1, curr_pos.second };
						break;
					}
				}

				if (next_pos.first >= 0 && next_pos.first < width && next_pos.second >= 0 && next_pos.second < height)
				{
					char c = grid[next_pos.second][next_pos.first];

					if (c == '|') // vertical
					{
						curr_pos = next_pos;
						steps++;
					}
					else if (c == '-') // horizontal
					{
						curr_pos = next_pos;
						steps++;
					}
					else if (c == '+') // change dir
					{
						int next_dir = -1;

						for (int i = 0; i < 4; i++)
						{
							auto& ad = adj[i];
							pair<int, int> np = { next_pos.first + ad.first, next_pos.second + ad.second };
							if (np.first >= 0 && np.first < width && np.second >= 0 && np.second < height && np != curr_pos && grid[np.second][np.first] != ' ')
							{
								next_dir = i;
								break;
							}
						}

						curr_pos = next_pos;
						dir = next_dir;
						steps++;
					}
					else if (c >= 'A' && c <= 'Z')
					{
						found_chars += c;
						curr_pos = next_pos;
						steps++;
					}
					else // end of path
					{
						break;
					}
				}
				else // out of grid
				{
					break;
				}
			}

			return pair<string, int>{ found_chars, steps };
		};

		pair<string, int> res = solve();

		// part 1
		memcpy(stringResult.first, res.first.c_str(), res.first.length());

		// part 2
		part2 = res.second;

		return { part1, part2 };
	}
};
