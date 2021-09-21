#include "../aocHelper.h"

class Day21 : public BaseDay
{
public:
	Day21() : BaseDay("21") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// meals[i] = pair( ings, allers )
		vector<pair<unordered_set<string>, unordered_set<string>>> meals;

		unordered_map<string, int> ings_count;
		unordered_map<string, unordered_set<string>> poss_allers;


		// input parsing
		unordered_set<string> ings;
		unordered_set<string> allers;

		string s;

		while (*input != '\0')
		{
			ings.clear();
			allers.clear();
			s = "";

			while (*input != '\n')
			{
				switch (*input)
				{
					case ' ':
					{
						ings.insert(s);
						s = "";
						input++;
						break;
					}
					case '(':
					{
						input += 10;

						while (*input != ')')
						{
							if (*input == ',')
							{
								allers.insert(s);
								s = "";
								input++;
							}
							else
							{
								s += *input;
							}
							input++;
						}
						allers.insert(s);

						break;
					}
					case ')':
					{
						input++;
						break;
					}
					default:
					{
						s += *input;
						input++;
						break;
					}
				}
			}

			input++;

			for (auto& i : ings)
			{
				auto it = ings_count.find(i);
				if (it != ings_count.end())
				{
					it->second++;
				}
				else
				{
					ings_count.insert({ i, 1 });
				}
			}

			for (auto& a : allers)
			{
				auto it = poss_allers.find(a);
				if (it != poss_allers.end())
				{
					unordered_set<string> tmp;

					for (auto& ing : ings)
					{
						const string ss = "aaa";
						auto f = it->second.find(ing);
						if (f != it->second.end())
						{
							tmp.insert(ing);
						}
					}
					it->second = tmp;
				}
				else
				{
					auto inserted = poss_allers.insert({ a, unordered_set<string>() });
					for (auto& ing : ings)
					{
						inserted.first->second.insert(ing);
					}
				}
			}

			//cout << "ings -----" << endl;
			for (auto i : ings)
			{
				//cout << i << endl;
			}

			//cout << "alers -----" << endl;
			for (auto a : allers)
			{
				//cout << a << endl;
			}

			meals.push_back({ ings, allers });

			//break;
		}

		unordered_set<string> all_ings;
		unordered_set<string> all_allers;

		for (auto& m : meals)
		{
			for (auto& i : m.first)
			{
				all_ings.insert(i);
			}
			for (auto& a : m.second)
			{
				all_allers.insert(a);
			}
		}

		for (auto& pa : poss_allers)
		{
			//cout << pa.first << " " << pa.second.size() << endl;
		}

		unordered_map<string, string> aller_match;

		for (auto& p : all_allers)
		{
			aller_match.insert({ p, "" });
		}

		// part 1
		while (true)
		{
			bool changed = false;

			for (auto& p : poss_allers)
			{
				if (p.second.size() == 1)
				{
					changed = true;

					string ing = *p.second.begin();

					aller_match[p.first] = ing;

					//cout << ing << endl;

					for (auto& p2 : poss_allers)
					{
						p2.second.erase(ing);
					}
				}
			}

			if (!changed)
			{
				break;
			}
		}

		int c_ = 0;
		for (auto& p : ings_count)
		{
			auto it = find_if(aller_match.begin(), aller_match.end(), [&p](pair<string, string> e)
			{
				return e.second == p.first;
			});

			if (it == aller_match.end())
			{
				//cout << p.first << " " << p.second << endl;
				c_ += p.second;
			}
		}

		part1 = c_;

		// part 2

		vector<string> ings_p2;

		for (auto& p : aller_match)
		{
			ings_p2.push_back(p.second);
		}

		unordered_map<string, string> rev_match;
		for (auto& p : aller_match)
		{
			rev_match.insert({ p.second, p.first });
		}

		sort(ings_p2.begin(), ings_p2.end(), [&rev_match](const string& a, const string& b)
		{
			return rev_match[a] < rev_match[b];
		});

		string res = "";
		for (auto& e : ings_p2)
		{
			res += e;
			res += ',';
		}

		res.pop_back();

		//stringResult.second = res;
		memcpy(stringResult.second, res.c_str(), res.length());

		return { part1, part2 };
	}
};
