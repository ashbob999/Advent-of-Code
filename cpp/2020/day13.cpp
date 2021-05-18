#include "../aocHelper.h"

class Day13 : public BaseDay
{
public:
	Day13() : BaseDay("13") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		using ull = unsigned long long;

		int start_time = numericParse<int>(input);
		input++;

		vector<int> bus_ids;

		while (*input != '\0')
		{
			if (*input >= '0' && *input <= '9')
			{
				bus_ids.push_back(numericParse<int>(input));
			}
			else
			{
				bus_ids.push_back(-1);
				input++;
			}

			input++;
		}

		// part 1

		int ed = start_time;

		while (true)
		{
			for (auto& bus : bus_ids)
			{
				if (bus != -1 && ed % bus == 0)
				{
					part1 = bus * (ed - start_time);
					goto part2;
				}
			}
			ed++;
		}

		// part 2
	part2:

		// modular inverse
		auto inv = [](long long a, long long m)
		{
			long long m0 = m, t, q;
			long long x0 = 0, x1 = 1;

			if (m == 1)
				return 0LL;

			// Apply extended Euclid Algorithm
			while (a > 1)
			{
				// q is quotient
				q = a / m;

				t = m;

				m = a % m, a = t;

				t = x0;

				x0 = x1 - q * x0;

				x1 = t;
			}

			// Make x1 positive
			if (x1 < 0)
				x1 += m0;

			return x1;
		};

		// Chinese remainder theorem
		auto findMinX = [&inv](vector<long long> num, vector<long long> rem, long long k)
		{
			// Compute product of all numbers
			long long prod = 1;
			for (int i = 0; i < k; i++)
				prod *= num[i];

			// Initialize result
			long long result = 0;

			// Apply above formula
			for (int i = 0; i < k; i++)
			{
				long long pp = prod / num[i];
				result += rem[i] * inv(pp, num[i]) * pp;
			}

			return result % prod;
		};

		vector<long long> m;
		vector<long long> x;

		for (int i = 0; i < bus_ids.size(); i++)
		{
			if (bus_ids[i] > -1)
			{
				m.push_back(bus_ids[i]);
				x.push_back(((-i % bus_ids[i]) + bus_ids[i]) % bus_ids[i]);
			}
		}

		part2 = findMinX(m, x, m.size());

		/*
		part 2 theory

		t % bid_1 == 0
		t + 1 % bid_2 == 0
		.......
		t + i % bid_i == 0
		*/

		return { part1, part2 };
	}
};
