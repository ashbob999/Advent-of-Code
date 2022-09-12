#include "../aocHelper.h"

class Day04 : public BaseDay
{
public:
	Day04() : BaseDay("04") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int card_size = 5;
		using bingo_card = array<array<int, card_size>, card_size>;
		using mark_card = array<array<bool, card_size>, card_size>;

		vector<int> numbers;
		vector<bingo_card> cards;

		while (*input != '\n')
		{
			int n = numericParse<int>(input);
			numbers.push_back(n);
			input++;
		}

		input++; // skip '\n'

		while (*input != '\0')
		{
			bingo_card card;

			for (int i = 0; i < card_size; i++)
			{
				for (int j = 0; j < card_size; j++)
				{
					if (*input == ' ')
					{
						input++;
					}

					int n = numericParse<int>(input);
					card[i][j] = n;

					input++;
				}
			}

			cards.push_back(card);

			input++; // skip '\n'
		}

		auto calc_score = [](bingo_card& card, mark_card& marked_card, int last_num)
		{
			int score = 0;

			for (int y = 0; y < card_size; y++)
			{
				for (int x = 0; x < card_size; x++)
				{
					if (marked_card[y][x] == false)
					{
						score += card[y][x];
					}
				}
			}

			return score * last_num;
		};

		// part 1
		auto solve_part1 = [&]()
		{
			vector<mark_card> marked_cards;
			marked_cards.resize(cards.size());

			int num_i = 0;
			while (num_i < numbers.size())
			{
				int num = numbers[num_i];

				for (int card_i = 0; card_i < cards.size(); card_i++)
				{
					bingo_card& card = cards[card_i];

					for (int y = 0; y < card_size; y++)
					{
						for (int x = 0; x < card_size; x++)
						{
							if (card[y][x] == num)
							{
								marked_cards[card_i][y][x] = true;
							}
						}
					}
				}

				for (int card_i = 0; card_i < cards.size(); card_i++)
				{
					mark_card& marked_card = marked_cards[card_i];

					// check horizontal
					for (int y = 0; y < card_size; y++)
					{
						bool bingo = true;
						for (int x = 0; x < card_size; x++)
						{
							if (marked_card[y][x] == false)
							{
								bingo = false;
								break;
							}
						}

						if (bingo)
						{
							return calc_score(cards[card_i], marked_card, num);
						}
					}

					// check vertical
					for (int x = 0; x < card_size; x++)
					{
						bool bingo = true;
						for (int y = 0; y < card_size; y++)
						{
							if (marked_card[y][x] == false)
							{
								bingo = false;
								break;
							}
						}

						if (bingo)
						{
							return calc_score(cards[card_i], marked_card, num);
						}
					}
				}

				num_i++;
			}

			return 0;
		};

		part1 = solve_part1();

		// part 2
		auto solve_part2 = [&]()
		{
			vector<mark_card> marked_cards;
			marked_cards.resize(cards.size());
			vector<int> won;

			int num_i = 0;
			while (num_i < numbers.size())
			{
				if (won.size() == cards.size())
				{
					break;
				}

				int num = numbers[num_i];

				for (int card_i = 0; card_i < cards.size(); card_i++)
				{
					bingo_card& card = cards[card_i];

					for (int y = 0; y < card_size; y++)
					{
						for (int x = 0; x < card_size; x++)
						{
							if (card[y][x] == num)
							{
								marked_cards[card_i][y][x] = true;
							}
						}
					}
				}

				for (int card_i = 0; card_i < cards.size(); card_i++)
				{
					mark_card& marked_card = marked_cards[card_i];

					if (find(won.begin(), won.end(), card_i) != won.end())
					{
						continue;
					}

					// check horizontal
					for (int y = 0; y < card_size; y++)
					{
						bool bingo = true;
						for (int x = 0; x < card_size; x++)
						{
							if (marked_card[y][x] == false)
							{
								bingo = false;
								break;
							}
						}

						if (bingo)
						{
							won.push_back(card_i);
							break;
						}
					}

					if (won.size() > 0 && won.back() == card_i)
					{
						continue;
					}

					// check vertical
					for (int x = 0; x < card_size; x++)
					{
						bool bingo = true;
						for (int y = 0; y < card_size; y++)
						{
							if (marked_card[y][x] == false)
							{
								bingo = false;
								break;
							}
						}

						if (bingo)
						{
							won.push_back(card_i);
							break;
						}
					}
				}

				num_i++;
			}

			int last_i = won.back();
			return calc_score(cards[last_i], marked_cards[last_i], numbers[num_i - 1]);
		};

		part2 = solve_part2();

		return { part1, part2 };
	}
};
