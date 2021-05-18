#include "../aocHelper.h"
#include <regex>

class Day19 : public BaseDay
{
public:
	Day19() : BaseDay("19") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		auto flags = regex_constants::ECMAScript | regex_constants::icase;
		auto match_flags = regex_constants::match_default | regex_constants::match_not_null;

		basic_regex number_pattern("[0-9]+", flags);
		basic_regex surround_or_pattern("(.*)[|](.*)", flags);
		basic_regex space_regex(" ", flags);

		unordered_map<int, string> patterns;
		vector<string> texts;

		// parse input

		// parse patterns
		while (*input != '\n')
		{
			int id = numericParse<int>(input);

			input++; // skip :
			input++; // skip space

			string s(1, '(');
			while (*input != '\n')
			{
				if (*input != '"')
				{
					s += *input;
				}

				input++;
			}

			s += ')';
			patterns.insert({ id, s });

			input++; // skip \n
		}

		input++; // skip \n

		// parse texts
		while (*input != '\0')
		{
			string s;
			while (*input != '\n')
			{
				s += *input;
				input++;
			}

			texts.push_back(s);

			input++; // skip \n
		}

		// surround | with brackets
		for (auto& k : patterns)
		{
			patterns[k.first] = regex_replace(k.second, surround_or_pattern, "($1)|($2)", match_flags);
		}

		auto expand = [&number_pattern, &patterns, &match_flags](int id)
		{
			string rule(patterns[id]);

			smatch matches;
			while (regex_search(rule, matches, number_pattern, match_flags | regex_constants::match_any))
			{
				string number_str = matches.str();
				int number = 0;
				for (int i = 0; i < number_str.length(); i++)
				{
					number *= 10;
					number += number_str[i] - '0';
				}

				rule.replace(matches.position(), number_str.length(), patterns[number]);
			}

			return rule;
		};

		patterns[42] = expand(42);
		patterns[31] = expand(31);

		// part 1
		string rule0 = "^" + expand(0) + "$";
		rule0 = regex_replace(rule0, space_regex, "", match_flags);
		basic_regex rule0_regex(rule0, flags | regex_constants::nosubs);

		for (auto& text : texts)
		{
			if (regex_match(text, rule0_regex, match_flags))
			{
				part1++;
			}
		}

		// part 2
		patterns[8] = "(42)+";
		patterns[11] = "42(42(42(42(42(42(42(42(42 31)?31)?31)?31)?31)?31)?31)?31)?31";

		rule0 = "^" + expand(0) + "$";
		rule0 = regex_replace(rule0, space_regex, "", match_flags);
		rule0_regex = basic_regex(rule0, flags | regex_constants::nosubs);

		for (auto& text : texts)
		{
			if (regex_match(text, rule0_regex, match_flags))
			{
				part2++;
			}
		}

		return { part1, part2 };
	}
};
