#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::array<std::array<std::array<char, 3>, 16>, 100> games{};

		int games_index = 0;

		while (*input != '\0')
		{
			auto&& game = games[games_index];

			input += 5; // skip 'Game '

			input++; // skip first digit

			if (*input != ':')
			{
				input++; // skip second digit
			}
			if (*input != ':')
			{
				input++; // skip third digit
			}

			input += 2; // skip ': '

			int hand_index = 0;

			while (*input != '\n')
			{
				char count = numericParse<char>(input);

				input++; // skip ' '

				switch (*input)
				{
					case 'r':
					{
						game[hand_index][0] = count;
						input += 3; // skip 'red'
						break;
					}
					case 'g':
					{
						game[hand_index][1] = count;
						input += 5; // skip 'green'
						break;
					}
					case 'b':
					{
						game[hand_index][2] = count;
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
						hand_index++;
						input += 2; // skip '; '
						break;
					}
				}
			}

			games_index++;

			input++; // skip '\n'
		}

		//    part 1

		constexpr char RedLimit = 12;
		constexpr char GreenLimit = 13;
		constexpr char BlueLimit = 14;

		for (int i = 0; i < games.size(); i++)
		{
			auto&& game = games[i];

			bool valid = true;

			for (auto&& hand : game)
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
				part1 += i + 1;
			}
		}

		// part 2

		for (auto&& game : games)
		{
			std::array<char, 3> min_vals{0, 0, 0};

			for (auto&& hand : game)
			{
				min_vals[0] = std::max(min_vals[0], hand[0]);
				min_vals[1] = std::max(min_vals[1], hand[1]);
				min_vals[2] = std::max(min_vals[2], hand[2]);
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
