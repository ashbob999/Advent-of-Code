#include "../aocHelper.h"

class Day25 : public BaseDay
{
public:
	Day25() : BaseDay("25") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// sum of 1 -> n
		auto sum = [](long long n)
		{
			return (n * (n + 1)) / 2;
		};

		// sum of n -> n+m
		auto sum_range = [](long long n, long long m)
		{
			return (m * m + 2 * m * n + m) / 2;
		};

		constexpr int value_1 = 20151125;
		constexpr int mult = 252533;
		constexpr int mod = 33554393;

		// parse input
		input += 80; // skip 'To continue, please consult the code grid in the manual.  Enter the code at row '

		int row = numericParse<int>(input);

		input += 9; // skip ', column '

		int col = numericParse<int>(input);

		// part 1
		long long index = 1;

		// get starting row value
		// sum of 1 - n (inclusive) = (n * (n + 1)) / 2
		// sum of 2 - col (inclusive)
		// => (col*(col+1)/2 - 1

		/*
		for (int i = 2; i <= col; i++)
		{
			index += 1;
		}
		*/

		long long val = sum(col) - 1;
		index += val;

		// get starting col value
		// sum of n - m (inclusive) = sum(m) - sum(n - 1)
		// sum of col - col + row (inclusive)
		// => sum(col+row-2) - sum(col-1)

		/*
		for (int i = col; i < col + row - 1; i++)
		{
			index += i;
		}
		*/

		// index += sum(col + row - 2) - sum(col - 1)
		// index += sum(col + row - 2) - (val1 + 1 - col)
		index += sum_range(col - 1, row - 1);

		// value = value * mult % mod: x times = > value * mult ^ x % mod
		//part1 = (value_1 * pow(mult, index - 1, mod)) % mod
		long long value = value_1;
		for (long long i = 0; i < index - 1; i++)
		{
			value = (value * mult) % mod;
		}

		part1 = value;

		// part 2

		return { part1, part2 };
	}
};
