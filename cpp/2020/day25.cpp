#include "../aocHelper.h"

class Day25 : public BaseDay
{
public:
	Day25() : BaseDay("25") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		long long card_key = numericParse<long long>(input);
		long long door_key = numericParse<long long>(input);

		/*
		(((1 * s % p) * s % p) * s % p)
		1 * s ^ 3 % 3
		*/

		long long p = 20201227;

		auto find_loop = [&p](long long key)
		{
			long long l = 1;
			long long b = 7;
			while (b != key)
			{
				b = (b * 7) % p;
				l++;
			}
			return l;
		};

		auto enc = [&p](long long key, long long loop)
		{
			long long v = 1;
			for (long long i = 0; i < loop; i++)
			{
				v = (v * key) % p;
			}
			return v;
		};

		// part 1
		long long card_loop = find_loop(card_key);
		long long enc_key = enc(door_key, card_loop);

		part1 = enc_key;

		return { part1, part2 };
	}
};