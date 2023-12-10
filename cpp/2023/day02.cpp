#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::pair<int, std::vector<std::array<char, 3>>>> games;

		while (*input != '\0')
		{
			std::pair<char, std::vector<std::array<char, 3>>> game;

			input += 5; // skip 'Game '

			char id = numericParse<char>(input);
			game.first = id;

			input += 2; // skip ': '

			game.second.push_back({});

			while (*input != '\n')
			{
				char count = numericParse<char>(input);

				input++; // skip ' '

				switch (*input)
				{
					case 'r':
					{
						game.second.back()[0] = count;
						input += 3; // skip 'red'
						break;
					}
					case 'g':
					{
						game.second.back()[1] = count;
						input += 5; // skip 'green'
						break;
					}
					case 'b':
					{
						game.second.back()[2] = count;
						input += 4; // skip 'blue'
						break;
					}
				}

				switch (*input)
				{
					case ',':
					{
						input += 2; // skip ', '
						break;
					}
					case ';':
					{
						game.second.push_back({});
						input += 2; // skip '; '
						break;
					}
				}
			}

			games.push_back(std::move(game));

			input++; // skip '\n'
		}

		// part 1

		constexpr char RedLimit = 12;
		constexpr char GreenLimit = 13;
		constexpr char BlueLimit = 14;

		for (auto&& game : games)
		{
			bool valid = true;

			for (auto&& hand : game.second)
			{
				if (hand[0] > RedLimit)
				{
					valid = false;
					break;
				}

				if (hand[1] > GreenLimit)
				{
					valid = false;
					break;
				}

				if (hand[2] > BlueLimit)
				{
					valid = false;
					break;
				}
			}

			if (valid)
			{
				part1 += game.first;
			}
		}

		// part 2

		for (auto&& game : games)
		{
			std::array<char, 3> min_vals{0, 0, 0};

			for (auto&& hand : game.second)
			{
				if (hand[0] != 0)
				{
					min_vals[0] = std::max(min_vals[0], hand[0]);
				}

				if (hand[1] != 0)
				{
					min_vals[1] = std::max(min_vals[1], hand[1]);
				}

				if (hand[2] != 0)
				{
					min_vals[2] = std::max(min_vals[2], hand[2]);
				}
			}

			int value = 1;
			if (min_vals[0] != 0)
			{
				value *= min_vals[0];
			}

			if (min_vals[1] != 0)
			{
				value *= min_vals[1];
			}

			if (min_vals[2] != 0)
			{
				value *= min_vals[2];
			}

			part2 += value;
		}

		return {part1, part2};
	}
};
