#include "../aocHelper.h"

class Day04 : public BaseDay
{
public:
	Day04() : BaseDay("04") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::string_view> grid{};

		// parse input
		while (*input != '\0')
		{
			const char* ptr = input;
			size_t length = 0;

			while (*input != '\n' && *input != '\0')
			{
				length++;
				input++;
			}

			grid.push_back(std::string_view(ptr, length));
			input++; // skip '\n'
		}

		const size_t width = grid[0].size();
		const size_t height = grid.size();

		// part 1
		const auto check = [&grid, width, height](size_t x, size_t y) -> size_t
		{
			size_t count = 0;

			static constexpr std::array<char, 4> Word{'X', 'M', 'A', 'S'};

			if (grid[y][x] != Word[0])
			{
				return 0;
			}

			// right
			if (x + 4 <= width)
			{
				constexpr int XDiff = 1;
				constexpr int YDiff = 0;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			// down
			if (y + 4 <= height)
			{
				constexpr int XDiff = 0;
				constexpr int YDiff = 1;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			// up
			if (y >= 3)
			{
				constexpr int XDiff = 0;
				constexpr int YDiff = -1;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			// left
			if (x >= 3)
			{
				constexpr int XDiff = -1;
				constexpr int YDiff = 0;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			// top left
			if (x >= 3 && y >= 3)
			{
				constexpr int XDiff = -1;
				constexpr int YDiff = -1;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			// top right
			if (x + 4 <= width && y >= 3)
			{
				constexpr int XDiff = 1;
				constexpr int YDiff = -1;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			// bottom left
			if (x >= 3 && y + 4 <= height)
			{
				constexpr int XDiff = -1;
				constexpr int YDiff = 1;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			// bottom right
			if (x + 4 <= width && y + 4 <= height)
			{
				constexpr int XDiff = 1;
				constexpr int YDiff = 1;
				if (grid[y + YDiff * 1][x + XDiff * 1] == Word[1] && grid[y + YDiff * 2][x + XDiff * 2] == Word[2] &&
					grid[y + YDiff * 3][x + XDiff * 3] == Word[3])
				{
					count++;
				}
			}

			return count;
		};

		for (size_t y = 0; y < height; y++)
		{
			for (size_t x = 0; x < width; x++)
			{
				part1 += check(x, y);
			}
		}

		// part 2
		for (size_t y = 1; y < height - 1; y++)
		{
			for (size_t x = 1; x < width - 1; x++)
			{
				if (grid[y][x] != 'A')
				{
					continue;
				}

				char topLeft = grid[y - 1][x - 1];
				char topRight = grid[y - 1][x + 1];
				char bottomLeft = grid[y + 1][x - 1];
				char bottomRight = grid[y + 1][x + 1];

				if ((topLeft == 'M' || topLeft == 'S') && (bottomRight == 'M' || bottomRight == 'S') &&
					(topLeft != bottomRight))
				{
					if ((topRight == 'M' || topRight == 'S') && (bottomLeft == 'M' || bottomLeft == 'S') &&
						(topRight != bottomLeft))
					{
						part2++;
					}
				}
			}
		}

		return {part1, part2};
	}
};
