#include "../aocHelper.h"

#include <random>

class Day19 : public BaseDay
{
public:
	Day19() : BaseDay("19") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct data
		{
			string before;
			string after;
		};

		string molecule;
		vector<data> replacements;

		// parse input
		while (true)
		{
			string before;

			while (*input != ' ')
			{
				before += *input;
				input++;
			}

			input += 4; // skip ' => '

			string after;

			while (*input != '\n')
			{
				after += *input;
				input++;
			}

			replacements.push_back({ before, after });

			input++; // skip \n

			if (*input == '\n')
			{
				break;
			}
		}

		input++; // skip \n

		while (*input != '\n')
		{
			molecule += *input;
			input++;
		}

		// part 1
		unordered_set<string> poss;

		for (int i = 0; i < molecule.length(); i++)
		{
			for (auto& rep : replacements)
			{
				if (molecule.length() - i >= rep.before.length() && strncmp(molecule.c_str() + i, rep.before.c_str(), rep.before.length()) == 0)
				{
					string s{ molecule };
					s.replace(i, rep.before.length(), rep.after);
					poss.insert(s);
				}
			}
		}

		part1 = poss.size();

		// part 2

		string curr = molecule;
		string  target{ 'e' };

		srand(0);

		while (curr.compare(target) != 0)
		{
			int index = rand() % replacements.size();

			auto& rep = replacements[index];

			auto f = curr.find(rep.after);
			if (f != string::npos)
			{
				curr.replace(f, rep.after.length(), rep.before);
				part2++;
			}
		}

		return { part1, part2 };
	}
};
