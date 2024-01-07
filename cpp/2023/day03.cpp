#include "../aocHelper.h"

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int Size = 140;

		std::array<std::array<char, Size>, Size> grid;

		int x = 0;
		int y = 0;

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				x = 0;
				y++;
			}
			else
			{
				grid[y][x] = *input;
				x++;
			}

			input++;
		}

		std::array<std::array<uint16_t, Size>, Size> grid_numbers{};

		const auto is_symbol = [](char c) { return !(c >= '0' && c <= '9') && c != '.'; };
		// const auto is_mult = [](char c) { return c == '*'; };

		const auto check_symbol_around_number =
			[&grid, &is_symbol, &grid_numbers](int x, int y) -> std::tuple<int, int, bool>
		{
			int number = 0;
			int number_length = 0;
			bool has_symbol = false;

			// check left of number
			if (x > 0)
			{
				char c = grid[y][x - 1];
				if (is_symbol(c))
				{
					has_symbol = true;
				}

				// check above number
				if (!has_symbol)
				{
					if (y > 0)
					{
						char c = grid[y - 1][x - 1];
						if (is_symbol(c))
						{
							has_symbol = true;
						}
					}
				}

				// check below number
				if (!has_symbol)
				{
					if (y < Size - 1)
					{
						char c = grid[y + 1][x - 1];
						if (is_symbol(c))
						{
							has_symbol = true;
						}
					}
				}
			}

			while (x < Size)
			{
				char c = grid[y][x];

				if (c < '0' || c > '9')
				{
					break;
				}

				// check above digit
				if (!has_symbol)
				{
					if (y > 0)
					{
						char c = grid[y - 1][x];
						if (is_symbol(c))
						{
							has_symbol = true;
						}
					}
				}

				// check below digit
				if (!has_symbol)
				{
					if (y < Size - 1)
					{
						char c = grid[y + 1][x];
						if (is_symbol(c))
						{
							has_symbol = true;
						}
					}
				}

				number = number * 10 + (c - '0');
				number_length++;
				x++;
			}

			if (x < Size)
			{
				// check right of number
				if (!has_symbol)
				{
					char c = grid[y][x];
					if (is_symbol(c))
					{
						has_symbol = true;
					}
				}

				// check above number
				if (!has_symbol)
				{
					if (y > 0)
					{
						char c = grid[y - 1][x];
						if (is_symbol(c))
						{
							has_symbol = true;
						}
					}
				}

				// check below number
				if (!has_symbol)
				{
					if (y < Size - 1)
					{
						char c = grid[y + 1][x];
						if (is_symbol(c))
						{
							has_symbol = true;
						}
					}
				}
			}

			// store the grid number
			for (int i = 0; i < number_length; i++)
			{
				grid_numbers[y][x - i - 1] = number;
			}

			return {number, number_length, has_symbol};
		};

		// part 1
		for (int y = 0; y < Size; y++)
		{
			for (int x = 0; x < Size; x++)
			{
				char c = grid[y][x];
				if (c >= '0' && c <= '9')
				{
					auto [number, number_length, has_symbol] = check_symbol_around_number(x, y);
					if (has_symbol)
					{
						part1 += number;
					}
					x += number_length;
				}
			}
		}

		// part 2

		const auto check_for_numbers = [&grid, &grid_numbers](int x, int y)
		{
			// check around for 2 separate numbers

			std::array<int, 2> numbers{};
			int number_count = 0;

			for (int dy = -1; dy <= 1; dy++)
			{
				for (int dx = -1; dx <= 1; dx++)
				{
					int nx = x + dx;
					int ny = y + dy;

					int number = grid_numbers[ny][nx];
					if (number == 0)
					{
						continue;
					}

					if (number == numbers[0] || number == numbers[1])
					{
						continue;
					}

					if (number_count == 2)
					{
						return -1;
					}

					numbers[number_count] = number;
					number_count++;

					if (number_count == 2)
					{
						return numbers[0] * numbers[1];
					}
				}
			}

			if (number_count == 2)
			{
				return numbers[0] * numbers[1];
			}
			else
			{
				return -1;
			}
		};

		for (int y = 0; y < Size; y++)
		{
			for (int x = 0; x < Size; x++)
			{
				char c = grid[y][x];

				if (c == '*')
				{
					int result = check_for_numbers(x, y);

					if (result != -1)
					{
						part2 += result;
					}
				}
			}
		}

		return {part1, part2};
	}
};
