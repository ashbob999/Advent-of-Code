#include "../aocHelper.h"

class Day07 : public BaseDay
{
public:
	Day07() : BaseDay("07") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct ip_address
		{
			vector<string> sequences;
			vector<string> hypernets;
		};

		vector<ip_address> ip_addresses;

		// parse input
		string text;
		ip_address curr_ip;

		while (*input != '\0')
		{
			if (*input == '[')
			{
				curr_ip.sequences.push_back(text);
				text = "";
			}
			else if (*input == ']')
			{
				curr_ip.hypernets.push_back(text);
				text = "";
			}
			else if (*input == '\n')
			{
				curr_ip.sequences.push_back(text);
				ip_addresses.push_back(curr_ip);
				curr_ip = ip_address{};
				text = "";
			}
			else
			{
				text += *input;
			}
			input++;
		}

		auto check_abba = [&](const string& s)
		{
			if (s.length() < 4)
			{
				return false;
			}

			for (int i = 0; i < s.length() - 3; i++)
			{
				if (s[i] != s[i + 1] && s[i] == s[i + 3] && s[i + 1] == s[i + 2])
				{
					return true;
				}
			}

			return false;
		};

		auto check_aba = [&](const string& s)
		{
			vector<string> found;

			if (s.length() < 3)
			{
				return found;
			}

			for (int i = 0; i < s.length() - 2; i++)
			{
				if (s[i] == s[i + 2] && s[i] != s[i + 1])
				{
					found.emplace_back(&s[i], &s[i + 3]);
				}
			}

			return found;
		};

		// part 1
		for (auto& ip : ip_addresses)
		{
			if (any_of(ip.sequences.begin(), ip.sequences.end(), check_abba))
			{
				if (none_of(ip.hypernets.begin(), ip.hypernets.end(), check_abba))
				{
					part1++;
				}
			}
		}

		// part 2
		for (auto& ip : ip_addresses)
		{
			bool correct = false;
			unordered_set<string> abas;

			for (auto& s : ip.sequences)
			{
				auto abas_ = check_aba(s);
				for (auto& aba : abas_)
				{
					abas.insert(aba);
				}
			}

			for (auto& aba : abas)
			{
				string bab;
				bab += aba[1];
				bab += aba[0];
				bab += aba[1];

				for (auto& h : ip.hypernets)
				{
					auto babs = check_aba(h);
					auto f = find(babs.begin(), babs.end(), bab);
					if (f != babs.end())
					{
						correct = true;
					}
				}

				if (correct)
				{
					break;
				}
			}

			if (correct)
			{
				part2++;
			}
		}

		return { part1, part2 };
	}
};
