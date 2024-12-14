#include "../aocHelper.h"

#include <execution>

namespace
{
	/*
	MSVC is dumb and won't convert this switch into a jump table, instead it has a jump for each case (which is slow)
	So there is a version 2 which is an implementaion of how gcc optimises the switch
	*/
	inline uint8_t card_to_rank(char c)
	{
		switch (c)
		{
			case '2':
				return 2;
			case '3':
				return 3;
			case '4':
				return 4;
			case '5':
				return 5;
			case '6':
				return 6;
			case '7':
				return 7;
			case '8':
				return 8;
			case '9':
				return 9;
			case 'T':
				return 10;
			case 'J':
				return 11;
			case 'Q':
				return 12;
			case 'K':
				return 13;
			case 'A':
				return 14;
			default:
				return 0;
		}
	}

	constexpr std::array<uint8_t, 35> create_lookup_table()
	{
		std::array<uint8_t, 35> lookup{};

		constexpr std::array<char, 13> cards{
			'2',
			'3',
			'4',
			'5',
			'6',
			'7',
			'8',
			'9',
			'T',
			'J',
			'Q',
			'K',
			'A',
		};

		for (int i = 0; i < cards.size(); i++)
		{
			uint8_t c = static_cast<uint8_t>(cards[i]) - 50;
			lookup[c] = i + 2;
		}

		return lookup;
	}

	inline uint8_t card_to_rank_2(char c)
	{
		c -= 50;

		if (c <= 34)
		{
			constexpr std::array<uint8_t, 35> lookup = create_lookup_table();
			return lookup[c];
		}

		return 0;
	}
}

class Day07 : public BaseDay
{
public:
	Day07() : BaseDay("07") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::pair<std::array<uint8_t, 5>, uint16_t>> hands;

		while (*input != '\0')
		{
			std::array<char, 5> cards;

			std::memcpy(cards.data(), input, 5 * sizeof(char));

			input += 6; // skip '_____ '

			uint16_t bid = numericParse<uint16_t>(input);

			std::array<uint8_t, 5> hand{
				card_to_rank_2(cards[0]),
				card_to_rank_2(cards[1]),
				card_to_rank_2(cards[2]),
				card_to_rank_2(cards[3]),
				card_to_rank_2(cards[4])};

			hands.push_back({hand, bid});

			input++; // skip '\n'
		}

		// part 1
		const auto p1_rank = [](const std::array<uint8_t, 5> hand)
		{
			std::array<uint8_t, 16> counts{};
			counts[hand[0]]++;
			counts[hand[1]]++;
			counts[hand[2]]++;
			counts[hand[3]]++;
			counts[hand[4]]++;

			uint8_t uniqueCount = 0;
			for (auto& count : counts)
			{
				if (count != 0)
				{
					uniqueCount++;
				}
			}

			// index = number of card of any type
			// value: how many times we had index number of cards
			std::array<uint8_t, 6> cardNumbers{};
			for (auto& count : counts)
			{
				cardNumbers[count]++;
			}

			if (uniqueCount == 1)
			{
				return 7; // 5 kind
			}

			if (uniqueCount == 2)
			{
				if (cardNumbers[4] != 0)
				{
					return 6; // 4 kind
				}
				else
				{
					return 5; // full house
				}
			}

			if (cardNumbers[3] != 0)
			{
				return 4; // 3 kind
			}

			if (cardNumbers[2] != 0)
			{
				if (cardNumbers[2] == 2)
				{
					return 3; // 2 pair
				}
				else
				{
					return 2; // 1 pair
				}
			}

			if (uniqueCount == 5)
			{
				return 1; // high card
			}

#if defined(_MSC_VER) && !defined(__clang__) // MSVC
			__assume(false);
#else // GCC, Clang
			__builtin_unreachable();
#endif
		};

		std::vector<std::pair<uint8_t, std::pair<std::array<uint8_t, 5>, uint16_t>>> ranks;
		ranks.reserve(hands.size());

		for (auto& hand : hands)
		{
			ranks.push_back({p1_rank(hand.first), hand});
		}

		std::sort(std::execution::unseq, ranks.begin(), ranks.end());
		for (int i = 0; i < ranks.size(); i++)
		{
			part1 += ranks[i].second.second * (i + 1);
		}

		// part 2
		const auto p2_rank = [&p1_rank](const std::array<uint8_t, 5>& hand)
		{
			std::array<uint8_t, 16> counts{};

			int jokers = 0;
			for (int i = 0; i < 5; i++)
			{
				if (hand[i] == 11)
				{
					jokers++;
				}
				else
				{
					counts[hand[i]]++;
				}
			}

			if (jokers == 0)
			{
				return p1_rank(hand);
			}

			if (jokers == 5)
			{
				return 7; // 5 kind
			}

			if (jokers == 4)
			{
				return 7; // 5 kind
			}

			// index = number of card of any type
			// value: how many times we had index number of cards
			std::array<uint8_t, 6> cardNumbers{};
			for (auto& count : counts)
			{
				cardNumbers[count]++;
			}

			if (jokers == 3)
			{
				if (cardNumbers[2] != 0)
				{
					return 7; // 5 kind
				}
				else
				{
					return 6; // 4 kind
				}
			}

			if (jokers == 2)
			{
				if (cardNumbers[3] != 0)
				{
					return 7; // 5 kind
				}
				if (cardNumbers[2] != 0)
				{
					return 6; // 4 kind
				}
				return 4; // 3 kind
			}

			if (jokers == 1)
			{
				if (cardNumbers[4] != 0)
				{
					return 7; // 5 kind
				}
				if (cardNumbers[3] != 0)
				{
					return 6; // 4 kind
				}
				if (cardNumbers[2] != 0)
				{
					if (cardNumbers[2] == 2)
					{
						return 5; // full house
					}
					else
					{
						return 4; // 3 kind
					}
				}
				return 2; // 1 pair
			}

#if defined(_MSC_VER) && !defined(__clang__) // MSVC
			__assume(false);
#else // GCC, Clang
			__builtin_unreachable();
#endif
		};

		ranks.clear();

		for (auto& hand : hands)
		{
			auto new_hand = hand;
			for (int i = 0; i < 5; i++)
			{
				if (new_hand.first[i] == 11)
				{
					new_hand.first[i] = 0;
				}
			}
			ranks.push_back({p2_rank(hand.first), std::move(new_hand)});
		}

		std::sort(std::execution::unseq, ranks.begin(), ranks.end());
		for (int i = 0; i < ranks.size(); i++)
		{
			part2 += ranks[i].second.second * (i + 1);
		}

		return {part1, part2};
	}
};
