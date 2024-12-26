#include "../aocHelper.h"

class Day14 : public BaseDay
{
public:
	Day14() : BaseDay("14") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		static constexpr int Width = 101;
		static constexpr int Height = 103;

		static constexpr size_t RobotCount = (static_cast<int>(500 / 8.0) + 1) * 8;
		std::array<std::array<int, RobotCount>, 4> robots;

		size_t i = 0;

		while (*input != '\0')
		{
			input += 2; // skip 'p='

			int x = numericParse<unsigned int>(input);
			input++; // skip ','
			int y = numericParse<unsigned int>(input);

			input += 3; // skip ' v='

			int vx = numericParse<int>(input);
			input++; // skip ','
			int vy = numericParse<int>(input);

			robots[0][i] = x;
			robots[1][i] = y;
			robots[2][i] = vx;
			robots[3][i] = vy;

			i++;

			input++;
		}

		if (i < RobotCount)
		{
			std::fill(robots[0].begin() + i, robots[0].end(), Width / 2);
			std::fill(robots[1].begin() + i, robots[1].end(), Height);
			std::fill(robots[2].begin() + i, robots[2].end(), 0);
			std::fill(robots[3].begin() + i, robots[3].end(), 0);
		}

		// part 1
		std::array<long long, 4> quads{};

		// int j = i;

		for (size_t i = 0; i < RobotCount; i++)
		{
			int x = robots[0][i] + 100 * robots[2][i];
			int y = robots[1][i] + 100 * robots[3][i];

			x = x % Width;
			if (x < 0)
			{
				x += Width;
			}

			y = y % Height;
			if (y < 0)
			{
				y += Height;
			}

			if (x < Width / 2)
			{
				if (y < Height / 2)
				{
					quads[0]++;
				}
				else if (y > Height / 2)
				{
					quads[1]++;
				}
			}
			else if (x > Width / 2)
			{
				if (y < Height / 2)
				{
					quads[2]++;
				}
				else if (y > Height / 2)
				{
					quads[3]++;
				}
			}
		}

		part1 = quads[0] * quads[1] * quads[2] * quads[3];

		// part 2

		size_t min_i = Width * Height;
		size_t min_v = std::numeric_limits<size_t>::max();

		static constexpr size_t Bits = (static_cast<int>(Width * Height / 256.0) + 1) * 256;
		std::bitset<Bits> grid{};

		for (size_t i = 1; i < Width * Height; i++)
		{
			grid.reset();

			for (size_t j = 0; j < RobotCount; j++)
			{
				int x = robots[0][j] + i * robots[2][j];
				int y = robots[1][j] + i * robots[3][j];

				x = x % Width;
				if (x < 0)
				{
					x += Width;
				}

				y = y % Height;
				if (y < 0)
				{
					y += Height;
				}

				grid.set(y * Width + x);
			}

			size_t diff = 0;

			for (int j = 0; j < Width * Height - 1; j++)
			{
				if (grid.test(j) != grid.test(j + 1))
				{
					diff++;
				}
			}

			if (diff < min_v)
			{
				min_i = i;
				min_v = diff;

				if (diff < RobotCount)
				{
					break;
				}
			}
		}

		part2 = min_i;

		return {part1, part2};
	}
};
