#include "../aocHelper.h"

class Day04 : public BaseDay
{
public:
	Day04() : BaseDay("04") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<vector<string>> passwords;

		passwords.push_back({});

		string str;

		// parse input
		while (*input != '\0')
		{
			if (*input == '\n')
			{
				passwords.back().push_back(str);
				str = "";
				passwords.push_back({});
			}
			else if (*input == ' ')
			{
				passwords.back().push_back(str);
				str = "";
			}
			else
			{
				str += *input;
			}

			input++;
		}

		passwords.pop_back();

		// part 1
		for (auto& pass : passwords)
		{
			unordered_set<string> pass_set;

			for (auto& w : pass)
			{
				pass_set.insert(w);
			}

			if (pass_set.size() == pass.size())
			{
				part1++;
			}
		}

		// part 2
		for (auto& pass : passwords)
		{
			unordered_set<string> pass_set;

			for (auto& w : pass)
			{
				sort(w.begin(), w.end());
				pass_set.insert(w);
			}

			if (pass_set.size() == pass.size())
			{
				part2++;
			}
		}

		return { part1, part2 };
	}
};
