#include "../aocHelper.h"

#include "vm.h"

class Day25 : public BaseDay
{
public:
	Day25() : BaseDay("25") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		VM vm{ input };

		int input_number = vm.instructions[2].values[0].second;
		
		// part 1
		/*
			from looking at the input operations the number passed to function 7
			needs to consist of a alternating binary pattern starting with 0
			e.g. 1010 or 1010101010101010

			function 2 calculates a minimum number to start with
			a = answer + input_number * 7
			where the input_number is the number given on line 3 of the input
			e.g. cpy 365 b

			then once we have calculated that number
			we can find the next largest number that has the alternating pattern
			then subtract the two for the answer
		*/

		input_number *= 7;

		int min_value = 2; // 0b10
		while (min_value < input_number)
		{
			min_value <<= 2;
			min_value |= 2; // 0b10
		}

		part1 = min_value - input_number;

		return { part1, part2 };
	}
};
