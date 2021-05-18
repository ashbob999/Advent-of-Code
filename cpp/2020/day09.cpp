#include "../aocHelper.h"

class Day09 : public BaseDay
{
public:
	Day09() : BaseDay("09") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		long long n;

		vector<long long> data;

		deque<long long> pre;

		unordered_set<long long> pre_set;

		for (int i = 0; i < 25; i++)
		{
			int n = numericParse<long long>(input);

			data.push_back(n);
			pre.push_back(n);
			pre_set.insert(n);
		}

		while ((n = numericParse<long long>(input)))
		{
			data.push_back(n);

			bool valid = false;

			for (auto& v : pre_set)
			{
				long long res = n - v;
				if (res != v && pre_set.count(res))
				{
					valid = true;
					break;
				}
			}

			if (!valid)
			{
				part1 = n;
				goto section2;
			}

			pre_set.erase(pre.front());
			pre_set.insert(n);

			pre.pop_front();
			pre.push_back(n);
		}

	section2:

		int max_len = 0, max_i = 0;
		int i = 0, j = 0;
		long long s = data.front();

		while (i < data.size())
		{
			if (s < part1)
			{
				j++;
				if (j < data.size())
				{
					s += data[j];
				}
			}
			else if (s > part1)
			{
				s -= data[i];
				i++;
			}
			else
			{
				if (j - i + 1 > max_len)
				{
					max_len = j - i + 1;
					max_i = i;
				}

				s -= data[i];
				i++;
			}
		}

		long long min = *min_element(data.begin() + max_i, data.begin() + max_i + max_len);
		long long max = *max_element(data.begin() + max_i, data.begin() + max_i + max_len);

		part2 = min + max;

		return { part1, part2 };
	}
};
