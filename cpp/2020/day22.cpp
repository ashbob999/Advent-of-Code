#include "../aocHelper.h"

class Day22 : public BaseDay
{
public:
	Day22() : BaseDay("22") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		list<int> player1;
		list<int> player2;

		// parse input
		// player 1
		input += 10; // skip Player 1:
		while (*input != '\n')
		{
			player1.push_back(numericParse<int>(input));
			input++;
		}

		// player 2
		input++; // skip newline
		input += 10; // skip Player 2:
		while (*input != '\0')
		{
			player2.push_back(numericParse<int>(input));
			input++;
		}

		struct result
		{
			int winner;
			array<list<int>, 2> decks;
			result(int w, array<list<int>, 2>& d) : winner(w), decks(d) {}
		};

		// part 1

		auto solve_p1 = [](list<int>& p1, list<int>& p2)
		{
			int winner;

			array<list<int>, 2> decks = {p1, p2};

			while (true)
			{
				int p1_card = decks[0].front();
				decks[0].pop_front();

				int p2_card = decks[1].front();
				decks[1].pop_front();

				if (p1_card > p2_card)
				{
					decks[0].push_back(p1_card);
					decks[0].push_back(p2_card);
				}
				else
				{
					decks[1].push_back(p2_card);
					decks[1].push_back(p1_card);
				}

				if (decks[0].size() == 0)
				{
					winner = 1;
					break;
				}
				else if (decks[1].size() == 0)
				{
					winner = 0;
					break;
				}
			}

			return result{ winner, decks };
		};

		auto res = solve_p1(player1, player2);

		int winner = res.winner;
		auto decks = res.decks;

		int i_mult = decks[winner].size();
		for (auto it = decks[winner].begin(); it != decks[winner].end(); ++it, i_mult--)
		{
			part1 += *it * i_mult;
		}

		// part 2

		function<result(list<int>&, list<int>&)> solve_p2;
		solve_p2 = [&solve_p2](list<int>& p1, list<int>& p2)
		{
			array<list<int>, 2> decks = { p1, p2 };

			int iterations = 0;

			while (true)
			{
				iterations++;

				if (iterations > 2000)
				{
					array<list<int>, 2> tmp;
					return result{ 0, tmp };
				}

				int winner;

				int p1_card = decks[0].front();
				decks[0].pop_front();

				int p2_card = decks[1].front();
				decks[1].pop_front();

				if (decks[0].size() >= p1_card && decks[1].size() >= p2_card)
				{
					list<int> p1_trim(decks[0].begin(), next(decks[0].begin(), p1_card));
					list<int> p2_trim(decks[1].begin(), next(decks[1].begin(), p2_card));
					auto res = solve_p2(p1_trim, p2_trim);

					winner = res.winner;
				}
				else
				{
					if (p1_card > p2_card)
					{
						winner = 0;
					}
					else
					{
						winner = 1;
					}
				}

				if (winner == 0)
				{
					decks[0].push_back(p1_card);
					decks[0].push_back(p2_card);
				}
				else if (winner == 1)
				{
					decks[1].push_back(p2_card);
					decks[1].push_back(p1_card);
				}

				if (decks[0].size() == 0)
				{
					return result{ winner, decks };
				}
				else if (decks[1].size() == 0)
				{
					return result{ winner, decks };
				}
			}
		};

		res = solve_p2(player1, player2);
		
		winner = res.winner;
		decks = res.decks;

		i_mult = decks[winner].size();
		for (auto it = decks[winner].begin(); it != decks[winner].end(); ++it, i_mult--)
		{
			part2 += *it * i_mult;
		}
		
		return { part1, part2 };
	}
};
