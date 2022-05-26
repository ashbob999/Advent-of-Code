#include "../aocHelper.h"

#include "vm.h"

class Day12 : public BaseDay
{
public:
	Day12() : BaseDay("12") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		VM vm{ input };

		// part 1
		vm.run();
		part1 = vm.registers['a'];

		// part 2
		vm.reset();
		vm.registers['c'] = 1;
		vm.run();
		part2 = vm.registers['a'];

		return { part1, part2 };
	}
};
