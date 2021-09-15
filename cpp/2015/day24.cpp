#include "../aocHelper.h"

#include <immintrin.h>

class Day24 : public BaseDay
{
public:
	Day24() : BaseDay("24") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> packages;

		// parse input
		while (*input != '\0')
		{
			int p = numericParse<int>(input);

			packages.push_back(p);

			input++; // skip \n
		}

		sort(packages.begin(), packages.end());

		vector<int> bin_match_i;
		for (int i = 0; i < packages.size(); i++)
		{
			bin_match_i.push_back(1 << i);
		}

		int package_bin = (1 << packages.size()) - 1;

		function<void(int, int, int, int, vector<int>&)> get_sums;
		get_sums = [&get_sums, &packages, &bin_match_i](int s, int i, int max_sum, int used_packages, vector<int>& matches)
		{
			if (i >= packages.size())
			{
				return;
			}

			get_sums(s, i + 1, max_sum, used_packages, matches);

			if (s + packages[i] < max_sum)
			{
				get_sums(s + packages[i], i + 1, max_sum, used_packages | bin_match_i[i], matches);
			}
			else if (s + packages[i] == max_sum)
			{
				matches.push_back(used_packages | bin_match_i[i]);
			}
		};

		auto bin_to_prod = [&packages](int n)
		{
			long long prod = 1;
			int i = 0;
			while (n)
			{
				if (n & 1)
				{
					prod *= packages[i];
				}
				i++;
				n >>= 1;
			}

			return prod;
		};

		auto bin_to_sum = [&packages](int n)
		{
			long long sum = 0;
			int i = 0;
			while (n)
			{
				if (n & 1)
				{
					sum += packages[i];
				}
				i++;
				n >>= 1;
			}

			return sum;
		};

		auto cmp = [&bin_to_prod](const int& a, const int& b)
		{
			int a_cnt = _mm_popcnt_u32(a);
			int b_cnt = _mm_popcnt_u32(b);

			if (a_cnt == b_cnt)
			{
				long long a_prod = bin_to_prod(a);
				long long b_prod = bin_to_prod(b);

				return a_prod < b_prod;
			}
			return a_cnt < b_cnt;
		};

		// part 1
		vector<int> matches;
		int group_weight = accumulate(packages.begin(), packages.end(), 0) / 3;

		get_sums(0, 0, group_weight, 0, matches);

		sort(matches.begin(), matches.end(), cmp);

		for (int i = 0; i < matches.size() - 1; i++)
		{
			auto& m1 = matches[i];
			for (int j = i + 1; j < matches.size(); j++)
			{
				auto& m2 = matches[j];

				if (!(m1 & m2)) // no overlap
				{
					int m3 = (m1 | m2) ^ package_bin;

					if (bin_to_sum(m3) == group_weight)
					{
						part1 = bin_to_prod(m1);
						goto part2;
					}
				}
			}
		}

	part2:
		// part 2
		matches.clear();
		group_weight = accumulate(packages.begin(), packages.end(), 0) / 4;

		get_sums(0, 0, group_weight, 0, matches);

		sort(matches.begin(), matches.end(), cmp);

		for (int i = 0; i < matches.size() - 2; i++)
		{
			auto& m1 = matches[i];
			for (int j = i + 1; j < matches.size() - 1; j++)
			{
				auto& m2 = matches[j];
				for (int k = j + 1; k < matches.size(); k++)
				{
					auto& m3 = matches[k];

					if (!(m1 & m2) && !(m1 & m3) && !(m2 & m3)) // no overlap
					{
						int m4 = (m1 | m2 | m3) ^ package_bin;

						if (bin_to_sum(m4) == group_weight)
						{
							part2 = bin_to_prod(m1);
							goto end;
						}
					}
				}
			}
		}

	end:
		return { part1, part2 };
	}
};
