#include "../aocHelper.h"

class Day10 : public BaseDay
{
public:
	Day10() : BaseDay("10") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		const unordered_map<char, int> score_corrupt = {
			{ ')', 3 },
			{ ']', 57 },
			{ '}', 1197 },
			{ '>', 25137 },
		};

		const unordered_map<char, int> score_closing = {
			{ ')', 1 },
			{ ']', 2 },
			{ '}', 3 },
			{ '>', 4 },
		};

		const unordered_set<char> open_set = { '(', '[', '{', '<' };
		const unordered_set<char> close_set = { ')', ']', '}', '>' };

		const unordered_map<char, char> match_open = {
			{ ')', '(' },
			{ ']', '[' },
			{ '}', '{' },
			{ '>', '<' },
		};

		const unordered_map<char, char> match_close = {
			{ '(', ')' },
			{ '[', ']' },
			{ '{', '}' },
			{ '<', '>' },
		};

		vector<string> lines;

		string s;

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				lines.push_back(s);
				s = "";
			}
			else
			{
				s += *input;
			}
			input++;
		}

		// part 1
		auto check_corrupted = [&](string& line)
		{
			deque<char> stack;

			for (auto c : line)
			{
				if (open_set.contains(c))
				{
					stack.push_back(c);
				}
				else
				{
					if (stack.back() == match_open.at(c))
					{
						stack.pop_back();
					}
					else
					{
						return c;
					}
				}
			}

			return '\0';
		};

		vector<string_view> non_corrupt;

		for (auto& line : lines)
		{
			char c = check_corrupted(line);
			if (c != '\0')
			{
				part1 += score_corrupt.at(c);
			}
			else
			{
				non_corrupt.push_back(line);
			}
		}

		// part 2
		auto check_closing = [&](string_view& line)
		{
			deque<char> stack;

			for (auto c : line)
			{
				if (open_set.contains(c))
				{
					stack.push_back(c);
				}
				else
				{
					if (stack.back() == match_open.at(c))
					{
						stack.pop_back();
					}
					else
					{
						continue;
					}
				}
			}

			return stack;
		};

		auto calc_score = [&](deque<char>& ending)
		{
			long long s = 0;

			for (auto c : ending)
			{
				s *= 5;
				s += score_closing.at(c);
			}

			return s;
		};

		vector<long long> scores;

		for (auto& line : non_corrupt)
		{
			deque<char> stack = check_closing(line);
			if (stack.size() > 0)
			{
				reverse(stack.begin(), stack.end());
				for_each(stack.begin(), stack.end(), [&](char& c)
				{
					c = match_close.at(c);
				});

				scores.push_back(calc_score(stack));
			}
		}

		sort(scores.begin(), scores.end());
		int mid_i = scores.size() / 2;
		part2 = scores[mid_i];

		return { part1, part2 };
	}
};
