#include "../aocHelper.h"

class Day13 : public BaseDay
{
public:
	Day13() : BaseDay("13") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<pair<int, int>> points;
		unordered_set<uint64_t> grid;

		enum class axis
		{
			X,
			Y,
		};

		vector<pair<axis, int>> folds;

		while (*input != '\n')
		{
			uint32_t n1 = numericParse<uint32_t>(input);
			input++; // skip ','
			uint32_t n2 = numericParse<uint32_t>(input);

			points.push_back({ n1, n2 });
			grid.insert((uint64_t) n1 << 32 | n2);

			input++; // skip '\n'
		}

		input++; // skip '\n'

		while (*input != '\0')
		{
			input += 11; // skip 'fold along '
			axis ax;
			if (*input == 'x')
			{
				ax = axis::X;
			}
			else
			{
				ax = axis::Y;
			}

			input++;
			input++; // skip '='

			int n = numericParse<int>(input);

			folds.push_back({ ax, n });

			input++; // skip '\n'
		}

		auto fold = [](unordered_set<uint64_t>& grid, pair<axis, int> fold)
		{
			unordered_set<uint64_t> folded_grid;

			int line = fold.second;

			switch (fold.first)
			{
				case axis::Y: // fold up
				{
					for (auto& p : grid)
					{
						if ((p & 0xffffffff) > line)
						{
							uint32_t y = p & 0xffffffff;
							uint32_t new_y = y - (y - line) * 2;
							folded_grid.insert((p & 0xffffffff00000000) | new_y);
						}
						else
						{
							folded_grid.insert(p);
						}
					}
					break;
				}
				case axis::X: // fold left
				{
					for (auto& p : grid)
					{
						if (((p & 0xffffffff00000000) >> 32) > line)
						{
							uint32_t x = (p & 0xffffffff00000000) >> 32;
							uint32_t new_x = x - (x - line) * 2;
							folded_grid.insert(((uint64_t) new_x << 32) | (p & 0xffffffff));
						}
						else
						{
							folded_grid.insert(p);
						}
					}
					break;
				}
			}

			return folded_grid;
		};

		// part 1
		unordered_set<uint64_t> folded_grid = grid;
		folded_grid = fold(folded_grid, folds[0]);

		part1 = folded_grid.size();

		// part 2

		for (auto it = folds.begin() + 1; it != folds.end(); it++)
		{
			folded_grid = fold(folded_grid, *it);
		}

		uint64_t max_x = 0;
		uint64_t max_y = 0;

		for (auto& p : folded_grid)
		{
			max_x = max(max_x, p >> 32);
			max_y = max(max_y, p & 0xffffffff);
		}

		bool** char_grid = new bool* [max_y + 1];

		for (int i = 0; i <= max_y; i++)
		{
			char_grid[i] = new bool[max_x + 1]{ false };
		}

		for (auto& p : folded_grid)
		{
			uint64_t x = p >> 32;
			uint64_t y = p & 0xffffffff;

			char_grid[y][x] = true;
		}

		int i = 0;
		for (int y = 0; y <= max_y; y++)
		{
			for (int x = 0; x <= max_x; x++)
			{
				if (char_grid[y][x])
				{
					this->stringResult.second[i] = '*';
				}
				else
				{
					this->stringResult.second[i] = ' ';
				}
				i++;
			}

			this->stringResult.second[i] = '\n';
			i++;
		}

		return { part1, part2 };
	}
};
