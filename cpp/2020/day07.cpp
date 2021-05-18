#include "../aocHelper.h"

class Day07 : public BaseDay
{
public:
	Day07() : BaseDay("07") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_map<string, int> bags;

		/*unordered_*/map<int, unordered_map<int, int>> rules;

		auto readWord = [](char*& str, string& s)
		{
			while (*str >= 'a' && *str <= 'z')
			{
				s += *str;
				str++;
			}
		};

		auto get_col_id = [&](string& colour)
		{
			auto it = bags.find(colour);
			if (it != bags.end())
			{
				return it->second;
			}
			auto inserted = bags.insert({ colour, bags.size() });
			return inserted.first->second;
		};

		string s;

		// parse input
		while (*input != '\0')
		{
			s = "";
			// read bag colour
			readWord(input, s);
			s += ' ';
			input++;
			readWord(input, s);

			input += 14;

			// get bag id
			int col_id = get_col_id(s);
			//cout << s << endl;

			while (*input != '\n')
			{
				if (*input == 'n')
				{
					while (*input != '\n')
					{
						input++;
					}
					break;
				}

				int amount = numericParse<int>(input);
				input++;

				s = "";
				readWord(input, s);
				input++;
				s += ' ';
				readWord(input, s);

				input += 4;

				if (*input == 's')
				{
					input++;
				}
				if (*input == ',')
				{
					input += 1;
				}
				else if (*input == '.')
				{
					input++;
				}

				//cout << "i " << int(*input) << endl;

				int c_id = get_col_id(s);

				//cout << s << " : " << amount << endl;
				rules[col_id].insert({ c_id, amount });
			}
			//cout << endl;
			input++;
		}

		int shinyGold_id = bags["shiny gold"];

		// part 1

		int* mem = new int[bags.size()];
		fill(mem, mem + bags.size(), -1);

		function<int(int, int)> solve1;
		solve1 = [&](int curr, int tar)
		{
			if (mem[curr] != -1)
			{
				return mem[curr];
			}

			int count = 0;
			for (auto& p : rules[curr])
			{
				if (p.first == tar)
				{
					mem[curr] = 1;
					return 1;
				}
				else
				{
					count |= solve1(p.first, tar);
				}
			}

			mem[curr] = count;
			return count;
		};

		for (int i = 0; i < bags.size(); i++)
		{
			if (solve1(i, shinyGold_id))
			{
				part1++;
			}
		}



		// part 2
		fill(mem, mem + bags.size(), -1);

		function<int(int)> solve2;
		solve2 = [&](int curr)
		{
			if (mem[curr] != -1)
			{
				return mem[curr];
			}

			int total = 0;
			for (auto& p : rules[curr])
			{
				total += p.second;
				total += p.second * solve2(p.first);
			}

			mem[curr] = total;
			return total;
		};

		part2 = solve2(shinyGold_id);

		delete[] mem;

		return { part1, part2 };
	}
};
