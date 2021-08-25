#include "../aocHelper.h"

class Day06 : public BaseDay
{
public:
	Day06() : BaseDay("06") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

		constexpr int grid_size = 1000;
		using size_type = uint16_t;

		pair<size_type, size_type>* grid = new pair<size_type, size_type>[grid_size * grid_size];

		// parse input
		while (*input != '\0')
		{
			input++; // skip 't'

			if (*input == 'o') // toggle
			{
				input += 6;
				int lower_x = numericParse<int>(input);
				input++;
				int lower_y = numericParse<int>(input);
				input += 9;
				int upper_x = numericParse<int>(input);
				input++;
				int upper_y = numericParse<int>(input);

				// loop through squares
				for (int y = lower_y; y <= upper_y; y++)
				{
					for (int x = lower_x; x <= upper_x; x++)
					{
						// part 1: toggle flips bit
						grid[y * grid_size + x].first ^= 1;

						// part 2: toggle increases brightness by 2
						grid[y * grid_size + x].second += 2;
					}
				}
			}
			else
			{
				input += 5;

				if (*input == 'n') // turn on
				{
					input += 2;
					int lower_x = numericParse<int>(input);
					input++;
					int lower_y = numericParse<int>(input);
					input += 9;
					int upper_x = numericParse<int>(input);
					input++;
					int upper_y = numericParse<int>(input);

					// loop through squares
					for (int y = lower_y; y <= upper_y; y++)
					{
						for (int x = lower_x; x <= upper_x; x++)
						{
							// part 1: turn on sets bit to 1
							grid[y * grid_size + x].first = 1;

							// part 2: turn on increases brightness by 1
							grid[y * grid_size + x].second++;
						}
					}
				}
				else // turn off
				{
					input += 3;
					int lower_x = numericParse<int>(input);
					input++;
					int lower_y = numericParse<int>(input);
					input += 9;
					int upper_x = numericParse<int>(input);
					input++;
					int upper_y = numericParse<int>(input);

					// loop through squares
					for (int y = lower_y; y <= upper_y; y++)
					{
						for (int x = lower_x; x <= upper_x; x++)
						{
							// part 1: turn on sets bit to 0
							grid[y * grid_size + x].first = 0;

							// part 2: turn on decreases brightness by 1 (min 0)
							if (grid[y * grid_size + x].second > 0)
							{
								grid[y * grid_size + x].second--;
							}
						}
					}
				}
			}

			input++; // skip \n
		}

		// count the grid

		for (int x = 0; x < grid_size * grid_size; x++)
		{
			part1 += grid[x].first;
			part2 += grid[x].second;
		}

		delete[] grid;

		return { part1, part2 };
	}
};
