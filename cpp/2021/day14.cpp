#include "../aocHelper.h"

class Day14 : public BaseDay
{
public:
	Day14() : BaseDay("14") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		map<pair<char, char>, char> rules;
		string poly;

		while (*input != '\n')
		{
			poly += *input;
			input++;
		}

		input += 2; // skip '\n\n'

		while (*input != '\0')
		{
			char c1 = *input;
			input++;
			char c2 = *input;
			input++;

			input += 4; // skip ' -> '

			char c3 = *input;
			input++;

			rules.insert({ { c1, c2}, c3 });

			input++; // skip '\n'
		}

		/*
		based on this
		20 is original length
		39 is length after 1 transform
		split into 2 halves (0-19 and 19-38) to stop memory overload
		each tab represents a iteration
		use memorisation or it will take forever
		20 -> 39 -> 20, 20
			20 -> 39 -> 20, 20
				20 -> 39 -> 20, 20
				20 -> 39 -> 20, 20
			20 -> 39 -> 20, 20
				20 -> 39 -> 20, 20
				20 -> 39 -> 20, 20
		*/

		map<pair<int, string>, array<long long, 26>> mem;

		function<array<long long, 26>(string& str, int, int, int)> step;
		step = [&rules, &mem, &step](string& str, int depth, int max_depth, int mid)
		{
			if (depth >= max_depth)
			{
				array<long long, 26> count{};

				for (int i = 0; i < str.size() - 1; i++)
				{
					//char c = str[i];
					//int a = str[i] - 'A';
					count[str[i] - 'A']++;
				}
				return count;
			}

			depth++;

			if (mem.contains({ depth, str }))
			{
				return mem[{ depth, str }];
			}

			string new_str;
			new_str.resize(2 * mid - 1, '-');

			int new_str_i = 0;
			for (int i = 1; i < mid; i++)
			{
				new_str[new_str_i] = str[i - 1];
				new_str[new_str_i + 1] = rules[{ str[i - 1], str[i] }];
				new_str_i += 2;
			}

			new_str.back() = str.back();

			array<long long, 26> count{};

			string s1{ new_str.begin(), new_str.begin() + mid };
			string s2{ new_str.begin() + mid - 1, new_str.end() };

			auto c1 = step(s1, depth, max_depth, mid);
			auto c2 = step(s2, depth, max_depth, mid);

			for (int i = 0; i < 26; i++)
			{
				count[i] += c1[i] + c2[i];
			}

			mem[{depth, str}] = count;

			return count;
		};

		// part 1
		auto count_p1 = step(poly, 0, 10, poly.size());

		count_p1[poly.back() - 'A']++;

		{
			int min_i = 0;
			int min_v = INT_MAX;

			int max_i = 0;
			int max_v = 0;

			for (int i = 0; i < 26; i++)
			{
				if (count_p1[i] > 0 && count_p1[i] < min_v)
				{
					min_i = i;
					min_v = count_p1[i];
				}

				if (count_p1[i] > max_v)
				{
					max_i = i;
					max_v = count_p1[i];
				}
			}

			part1 = max_v - min_v;
		}

		// part 2
		mem.clear();

		auto count_p2 = step(poly, 0, 40, poly.size());

		count_p2[poly.back() - 'A']++;

		{
			long long min_i = 0;
			long long min_v = LLONG_MAX;

			long long max_i = 0;
			long long max_v = 0;

			for (int i = 0; i < 26; i++)
			{
				if (count_p2[i] > 0LL && count_p2[i] < min_v)
				{
					min_i = i;
					min_v = count_p2[i];
				}

				if (count_p2[i] > max_v)
				{
					max_i = i;
					max_v = count_p2[i];
				}
			}

			part2 = max_v - min_v;
		}

		return { part1, part2 };
	}
};
