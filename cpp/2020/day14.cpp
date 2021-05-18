#include "../aocHelper.h"

class Day14 : public BaseDay
{
public:
	Day14() : BaseDay("14") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_map<long long, long long> mem1;
		unordered_map<long long, long long> mem2;

		long long mask_ignore;
		long long mask_bits;

		auto solve1 = [&mem1, &mask_ignore, &mask_bits](long long address, long long data)
		{
			for (long long i = 0, v = 1LL << 35; i < 36; i++, v >>= 1)
			{
				if (mask_ignore & v) // X
				{
					continue;
				}
				else if (mask_bits & v) // 1
				{
					data |= v;
				}
				else // 0
				{
					data &= ~v;
				}
			}

			mem1[address] = data;
		};

		auto solve2 = [&mem2, &mask_ignore, &mask_bits](long long address, long long data)
		{
			vector<long long> x_indexes;

			for (long long i = 0, v = 1LL << 35; i < 36; i++, v >>= 1)
			{
				if (mask_ignore & v) // X
				{
					x_indexes.push_back(i);
				}
				else if (mask_bits & v) // 1
				{
					address |= v;
				}
				else // 0
				{
					continue;
				}
			}

			long long max = (1LL << (x_indexes.size()));
			for (long long c = 0; c < max; c++)
			{
				long long val = address;

				for (long long i = 0, v = max >> 1; i < x_indexes.size(); i++, v >>= 1)
				{
					if ((c >> (x_indexes.size() - 1 - i)) & 1)
					{
						val &= ~(1LL << (35 - x_indexes[i]));
					}
					else
					{
						val |= 1LL << (35 - x_indexes[i]);
					}
				}

				mem2[val] = data;
			}
		};

		// parse input

		while (*input != '\0')
		{
			input++;
			if (*input == 'a') // mask
			{
				input += 6;
				mask_ignore = 0;
				mask_bits = 0;

				for (long long i = 0, v = 1LL << 35; i < 36; i++, v >>= 1)
				{
					if (*input == '0')
					{
					}
					else if (*input == '1')
					{
						mask_bits |= v;
					}
					else if (*input == 'X')
					{
						mask_ignore |= v;
					}
					input++;
				}
			}
			else // mem
			{
				input += 3;

				long long address = numericParse<long long>(input);
				input += 4;
				long long data = numericParse<long long>(input);

				solve1(address, data);
				solve2(address, data);
			}
			input++;
		}

		for (auto& p : mem1)
		{
			part1 += p.second;
		}

		for (auto& p : mem2)
		{
			part2 += p.second;
		}

		return { part1, part2 };
	}
};
