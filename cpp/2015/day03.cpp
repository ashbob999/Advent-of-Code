#include "../aocHelper.h"

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

		struct position
		{
			int x;
			int y;
		};

		auto handle_move = [](position& pos, char c)
		{
			if (c == '^')
			{
				pos.y++;
			}
			else if (c == 'v')
			{
				pos.y--;
			}
			else if (c == '<')
			{
				pos.x--;
			}
			else if (c == '>')
			{
				pos.x++;
			}
		};

		auto merge = [](position pos)
		{
			return (pos.x << 16) | (pos.y & 0xFFFF);
		};

		unordered_set<int> locations_1;
		unordered_set<int> locations_2;

		position santa_1{ 0,0 };
		locations_1.insert(0);

		position santa_2{ 0,0 };
		position robot{ 0,0 };
		bool is_santa = true;
		locations_2.insert(0);

		while (*input != '\0')
		{
			char c = *input;

			// part 1
			handle_move(santa_1, c);
			locations_1.insert(merge(santa_1));

			// part 2
			handle_move((is_santa ? santa_2 : robot), c);
			locations_2.insert(merge(is_santa ? santa_2 : robot));
			is_santa ^= 1;

			input++; // skip: \n
		}

		part1 = locations_1.size();
		part2 = locations_2.size();

		return { part1, part2 };
	}
};
