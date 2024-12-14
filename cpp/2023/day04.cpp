#include "../aocHelper.h"

class Day04 : public BaseDay
{
public:
	Day04() : BaseDay("04") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		using bitset = std::bitset<100>;

		std::array<uint32_t, 256> card_counts{};
		std::fill(card_counts.begin(), card_counts.end(), 1);

		int i = 0;

		char* p;
		numericParse<int>(p);
		numericParse<unsigned int>(p);

		while (*input != '\0')
		{
			input += 10; // skip 'Card xxx: '

			std::pair<bitset, bitset> card;

			while (*input != '|')
			{
				uint32_t number = numericParseWithLeadingSpaces<uint32_t>(input);
				input++; // skip ' '
				card.first.set(number);
			}

			input += 1; // skip '|'

			while (*input != '\n')
			{
				input++; // skip ' '
				uint32_t number = numericParseWithLeadingSpaces<uint32_t>(input);
				card.second.set(number);
			}

			// find card match
			auto matching = card.first & card.second;
			auto count = matching.count();

			// part 1
			part1 += (1 << count) >> 1;

			// part 2

			part2 += card_counts[i];
			for (int j = 0; j < count; j++)
			{
				card_counts[i + j + 1] += card_counts[i];
			}

			input++; // skip '\n'

			i++;
		}

		return {part1, part2};
	}
};
