#include "../aocHelper.h"

constexpr long long factorial(long long n)
{
	if (n <= 1)
	{
		return 1;
	}
	return n * factorial(n - 1);
}

class Day20 : public BaseDay
{
public:
	Day20() : BaseDay("20") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		static constexpr int FACTS_COUNT = 14;

		static constexpr long long facts[FACTS_COUNT] = { factorial(1), factorial(2), factorial(3), factorial(4), factorial(5), factorial(6), factorial(7), factorial(8), factorial(9), factorial(10), factorial(11), factorial(12), factorial(12), factorial(14) };

		static_assert(facts[3] == 24);

		// incorrect for n=1
		auto divisor_sum_both = [](long long n)
		{
			long long max_n = floor(sqrt(n));

			auto result = make_pair(n + 1, n + 1);

			for (long long i = 2; i <= max_n; i++)
			{
				if (n % i == 0)
				{
					result.first += i;
					if (i * 50 >= n)
					{
						result.second += i;
					}
					long long d = n / i;
					if (d != i)
					{
						result.first += d;
						if (d * 50 >= n)
						{
							result.second += d;
						}
					}
				}
			}

			return result;
		};

		auto run_both_parts = [&divisor_sum_both](long long number)
		{
			// 4 = > 1 * 10 + 2 * 10 + 4 * 10 = (1 + 2 + 4) * 10
			// divisors of 4 are 1, 2, 4
			// so 4 = > div - sum * 10
			auto min_div_sum = make_pair(number / 10, number / 11);

			auto found = make_pair(false, false);

			auto result = make_pair(0, 0);

			// given that div_sum(n!) has the highest divisor sum from 1->n!
			// we can use use div_sum(n!) to find n1 and n2 where ds(n1!) <= ds(t) <= ds(n2!)

			long long min_target = min(min_div_sum.first, min_div_sum.second);
			long long start_i = 1;

			for (int i = 0; i < FACTS_COUNT - 1; i++)
			{
				if (divisor_sum_both(facts[i]).second <= min_target && min_target < divisor_sum_both(facts[i + 1]).first)
				{
					start_i = facts[i];
					break;
				}
			}

			long long i = start_i;

			while (true)
			{
				auto s = divisor_sum_both(i);

				if (!found.first && s.first >= min_div_sum.first)
				{
					result.first = i;
					found.first = true;
				}

				if (!found.second && s.second >= min_div_sum.second)
				{
					result.second = i;
					found.second = true;
				}

				if (found.first && found.second)
				{
					break;
				}

				i++;
			}

			return result;
		};

		// parse input
		int number = numericParse<long long>(input);

		auto solution = run_both_parts(number);

		// part 1
		part1 = solution.first;

		// part 2
		part2 = solution.second;

		return { part1, part2 };
	}
};
