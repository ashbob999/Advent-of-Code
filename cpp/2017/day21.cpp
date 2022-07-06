#include "../aocHelper.h"

class Day21 : public BaseDay
{
public:
	Day21() : BaseDay("21") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct rule
		{
			vector<vector<bool>> before;
			vector<vector<bool>> after;
		};

		vector<rule> rules;

		vector<vector<bool>> start_pattern = { {false, true, false}, {false, false, true}, {true, true, true} };

		auto flip = [](vector<vector<bool>> patt, int dir)
		{
			vector<vector<bool>> patt_res = patt;
			if (dir == 0) // ver
			{
				for (int y = 0; y < patt_res.size(); y++)
				{
					patt_res[y] = patt[patt_res.size() - y - 1];
				}
			}
			else if (dir == 1) // hor
			{
				for (auto& r : patt_res)
				{
					reverse(r.begin(), r.end());
				}
			}

			return patt_res;
		};

		auto transpose = [](vector<vector<bool>> patt)
		{
			vector<vector<bool>> patt_res = patt;

			for (int y = 0; y < patt_res.size(); y++)
			{
				for (int x = 0; x < patt_res[0].size(); x++)
				{
					patt_res[y][x] = patt[x][y];
				}
			}
			return patt_res;
		};

		auto rotate = [&flip, &transpose](vector<vector<bool>> patt, int dir)
		{
			if (dir == 0)
			{
				return patt;
			}
			else if (dir == 90)
			{
				return flip(transpose(patt), 1);
			}
		};

		// parse input
		while (*input != '\0')
		{
			rule r;

			r.before.push_back({});

			while (*input != ' ')
			{
				if (*input == '/')
				{
					r.before.push_back({});
				}
				else
				{
					if (*input == '#')
					{
						r.before.back().push_back(true);
					}
					else
					{
						r.before.back().push_back(false);
					}
				}
				input++;
			}

			input += 4; // skip " => "

			r.after.push_back({});

			while (*input != '\n')
			{
				if (*input == '/')
				{
					r.after.push_back({});
				}
				else
				{
					if (*input == '#')
					{
						r.after.back().push_back(true);
					}
					else
					{
						r.after.back().push_back(false);
					}
				}
				input++;
			}

			rules.push_back(r);
			rules.emplace_back(flip(r.before, 1), r.after);
			rules.emplace_back(flip(r.before, 0), r.after);
			rules.emplace_back(flip(flip(r.before, 1), 0), r.after);

			vector<vector<bool>> rot = rotate(r.before, 90);
			rules.emplace_back(rot, r.after);
			rules.emplace_back(flip(rot, 1), r.after);
			rules.emplace_back(flip(rot, 0), r.after);
			rules.emplace_back(flip(flip(rot, 1), 0), r.after);

			input++; // skip '\n'
		}

		auto iterate = [&rules](vector<vector<bool>>& grid)
		{
			vector<vector<bool>> new_grid;

			if (grid.size() % 2 == 0) // split into 2x2
			{
				new_grid.resize((grid.size() / 2) * 3);
				for (int y = 0; y < grid.size() / 2; y++)
				{
					for (int x = 0; x < grid.size() / 2; x++)
					{
						// replaces 2x2 grid with 3x3 grid
						vector<vector<bool>> mini_grid;
						mini_grid.resize(2);
						for (int i = 0; i < 2; i++)
						{
							mini_grid[i].resize(2);
							for (int j = 0; j < 2; j++)
							{
								mini_grid[i][j] = grid[y * 2 + i][x * 2 + j];
							}
						}

						vector<vector<bool>> out_grid;
						for (auto& r : rules)
						{
							if (r.before == mini_grid)
							{
								out_grid = r.after;
								break;
							}
						}

						for (int y2 = 0; y2 < 3; y2++)
						{
							int y_pos = y * 3 + y2;
							new_grid[y_pos].insert(new_grid[y_pos].end(), out_grid[y2].begin(), out_grid[y2].end());
						}
					}
				}
			}
			else // split into 3x3
			{
				new_grid.resize((grid.size() / 3) * 4);
				for (int y = 0; y < grid.size() / 3; y++)
				{
					for (int x = 0; x < grid.size() / 3; x++)
					{
						// replaces 3x3 grid with 4x4 grid
						vector<vector<bool>> mini_grid;
						mini_grid.resize(3);
						for (int i = 0; i < 3; i++)
						{
							mini_grid[i].resize(3);
							for (int j = 0; j < 3; j++)
							{
								mini_grid[i][j] = grid[y * 3 + i][x * 3 + j];
							}
						}

						vector<vector<bool>> out_grid;
						for (auto& r : rules)
						{
							if (r.before == mini_grid)
							{
								out_grid = r.after;
								break;
							}
						}

						for (int y2 = 0; y2 < 4; y2++)
						{
							int y_pos = y * 4 + y2;
							new_grid[y_pos].insert(new_grid[y_pos].end(), out_grid[y2].begin(), out_grid[y2].end());
						}
					}
				}
			}

			return new_grid;
		};

		// part 1
		vector<vector<bool>> patt = start_pattern;

		for (int i = 0; i < 5; i++)
		{
			patt = iterate(patt);
		}

		for (auto& r : patt)
		{
			for (auto v : r)
			{
				if (v)
				{
					part1++;
				}
			}
		}

		// part 2
		//patt = start_pattern;

		for (int i = 0; i < 18 - 5; i++)
		{
			patt = iterate(patt);
		}

		for (auto& r : patt)
		{
			for (auto v : r)
			{
				if (v)
				{
					part2++;
				}
			}
		}

		return { part1, part2 };
	}
};
