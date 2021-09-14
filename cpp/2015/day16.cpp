#include "../aocHelper.h"

class Day16 : public BaseDay
{
public:
	Day16() : BaseDay("16") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		auto char3_to_id = [](char* str) constexpr -> int
		{
			return *str | *(str + 1) << 8 | *(str + 2) << 16;
		};

		auto const_char3_to_id = [](const char* str) constexpr -> int
		{
			return *str | *(str + 1) << 8 | *(str + 2) << 16;
		};

		struct data
		{
			int length;
			int id;
		};

		unordered_map<int, data> value_to_id = {
			{ const_char3_to_id("chd"), {8,  0} }, // children
			{ const_char3_to_id("cat"), {4,  1} }, // cats
			{ const_char3_to_id("sam"), {8,  2} }, // samoyeds (dog)
			{ const_char3_to_id("pom"), {11, 3} }, // pomeranians (dog)
			{ const_char3_to_id("aki"), {6,  4} }, // akitas (dog)
			{ const_char3_to_id("viz"), {7,  5} }, // vizslas (dog)
			{ const_char3_to_id("gol"), {8,  6} }, // goldfish
			{ const_char3_to_id("tre"), {5,  7} }, // trees
			{ const_char3_to_id("car"), {4,  8} }, // cars
			{ const_char3_to_id("per"), {8,  9} } // perfumes
		};

		unordered_map<int, int> card_values = {
			{ const_char3_to_id("chd"), 3 }, // children: 3
			{ const_char3_to_id("cat"), 7 }, // cats: 7
			{ const_char3_to_id("sam"), 2 }, // samoyeds: 2
			{ const_char3_to_id("pom"), 3 }, // pomeranians: 3
			{ const_char3_to_id("aki"), 0 }, // akitas: 0
			{ const_char3_to_id("viz"), 0 }, // vizslas: 0
			{ const_char3_to_id("gol"), 5 }, // goldfish: 5
			{ const_char3_to_id("tre"), 3 }, // trees: 3
			{ const_char3_to_id("car"), 2 }, // cars: 2
			{ const_char3_to_id("per"), 1 } // perfumes: 1
		};

		vector<unordered_map<int, int>> aunts;
		aunts.reserve(500);

		// parse input
		while (*input != '\0')
		{
			input += 4; // skip 'Sue '

			int number = numericParse<int>(input);

			input += 2; // skip ': '

			aunts.push_back({});

			auto& m = aunts.back();

			// read the compunds

			while (*input != '\n')
			{

				int id = char3_to_id(input);

				data& d = value_to_id[id];

				input += d.length; // skip compound name
				input += 2; // skip': '

				int count = numericParse<int>(input);

				m[id] = count;

				if (*input == ',')
				{
					input += 2; // skip ', '
				}
			}

			input++; // skip \n
		}

		auto matches = [&card_values, &value_to_id, &const_char3_to_id](unordered_map<int, int>& values, bool use_ranges)
		{
			for (auto& p : values)
			{
				auto f = card_values.find(p.first);
				if (f == card_values.end())
				{
					return false;
				}

				if (use_ranges)
				{
					if (p.first == const_char3_to_id("cat") || p.first == const_char3_to_id("tre")) // greater than
					{
						if (p.second <= card_values[p.first])
						{
							return false;
						}
					}
					else if (p.first == const_char3_to_id("pom") || p.first == const_char3_to_id("gol")) // less than
					{
						if (p.second >= card_values[p.first])
						{
							return false;
						}
					}
					else if (card_values[p.first] != p.second)
					{
						return false;
					}
				}
				else
				{
					if (card_values[p.first] != p.second)
					{
						return false;
					}
				}
			}

			return true;
		};

		// part 1
		for (int i = 0; i < aunts.size(); i++)
		{
			if (matches(aunts[i], false))
			{
				part1 = i + 1;
				break;
			}
		}

		// part 2
		for (int i = 0; i < aunts.size(); i++)
		{
			if (matches(aunts[i], true))
			{
				part2 = i + 1;
				break;
			}
		}

		return { part1, part2 };
	}
};
