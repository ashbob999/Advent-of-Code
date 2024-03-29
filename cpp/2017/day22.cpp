#include "../aocHelper.h"

class Day22 : public BaseDay
{
public:
	Day22() : BaseDay("22") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_set<uint32_t> points;

		int width;
		int height;

		// parse input

		int x = 0;
		int y = 0;
		while (*input != '\0')
		{
			if (*input == '\n')
			{
				width = x;
				y++;
				x = 0;
			}
			else
			{
				if (*input == '#')
				{
					points.insert((uint32_t) (x + 30'000) << 16 | (uint32_t) (y + 30'000));
				}
				x++;
			}
			input++;
		}

		height = y;

		// part 1
		unordered_set<uint32_t> p1_inf_points = points;
		pair<uint32_t, uint32_t> p1_pos = { (width / 2) + 30'000, (height / 2) + 30'000 };
		int p1_dir = 0; // up

		for (int i = 0; i < 10'000; i++)
		{
			uint32_t pos = p1_pos.first << 16 | p1_pos.second;
			if (p1_inf_points.contains(pos)) // turn right
			{
				p1_dir++;
				if (p1_dir == 4)
				{
					p1_dir = 0;
				}

				// clean
				p1_inf_points.erase(pos);
			}
			else // turn left
			{
				p1_dir--;
				if (p1_dir == -1)
				{
					p1_dir = 3;
				}

				// infect
				p1_inf_points.insert(pos);
				part1++;
			}

			// move
			switch (p1_dir)
			{
				case 0: // up
				{
					p1_pos.second--;
					break;
				}
				case 1: // right
				{
					p1_pos.first++;
					break;
				}
				case 2: // down
				{
					p1_pos.second++;
					break;
				}
				case 3: // left
				{
					p1_pos.first--;
					break;
				}
			}
		}

		// part 2
		unordered_map<uint32_t, int> p2_inf_points;
		for (auto& p : points)
		{
			p2_inf_points.insert({ p, 2 });
		}
		pair<uint32_t, uint32_t> p2_pos = { (width / 2) + 30'000, (height / 2) + 30'000 };
		int p2_dir = 0; // up

		for (int i = 0; i < 10'000'000; i++)
		{
			uint32_t pos = p2_pos.first << 16 | p2_pos.second;
			if (!p2_inf_points.contains(pos))
			{
				p2_inf_points.insert({ pos, 0 }); // clean
			}

			int state = p2_inf_points[pos];

			switch (state)
			{
				case 0: // clean, turn left
				{
					p2_dir--;
					if (p2_dir == -1)
					{
						p2_dir = 3;
					}

					// clean -> weakened
					p2_inf_points[pos] = 1;

					break;
				}
				case 1: // weakened, carry on
				{
					// weakened -> infected
					p2_inf_points[pos] = 2;
					part2++;

					break;
				}
				case 2: // infected, turn right
				{
					p2_dir++;
					if (p2_dir == 4)
					{
						p2_dir = 0;
					}

					// infected -> flagged
					p2_inf_points[pos] = 3;

					break;
				}
				case 3: // flagged, reverse dir
				{
					p2_dir -= 2;
					if (p2_dir < 0)
					{
						p2_dir += 4;
					}

					// flagged -> clean
					p2_inf_points[pos] = 0;

					break;
				}
			}

			// move
			switch (p2_dir)
			{
				case 0: // up
				{
					p2_pos.second--;
					break;
				}
				case 1: // right
				{
					p2_pos.first++;
					break;
				}
				case 2: // down
				{
					p2_pos.second++;
					break;
				}
				case 3: // left
				{
					p2_pos.first--;
					break;
				}
			}
		}

		return { part1, part2 };
	}
};
