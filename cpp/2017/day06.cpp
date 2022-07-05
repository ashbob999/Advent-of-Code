#include "../aocHelper.h"

class Day06 : public BaseDay
{
public:
	Day06() : BaseDay("06") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		array<uint32_t, 16> memory;
		uint32_t i = 0;

		// parse input
		while (*input != '\n')
		{
			if (*input >= '0' && *input <= '9')
			{
				uint32_t n = numericParse<uint32_t>(input);
				memory[i] = n;
				i++;
			}
			else
			{
				input++;
			}
		}

		auto hash_mem = [](array<uint32_t, 16>& mem) -> uint64_t
		{
			uint64_t value = 0;

			for (int i = 0; i < 16; i++)
			{
				if (mem[i] > 0b1111)
				{
					cout << "error" << endl;
					return (uint64_t) 0;
				}
				value <<= 4;
				value |= mem[i] & 0b1111;
			}

			return value;
		};

		// part 1
		array<uint32_t, 16> p1_memory;
		copy(memory.begin(), memory.end(), p1_memory.begin());

		unordered_set<uint64_t> p1_states;
		p1_states.insert(hash_mem(p1_memory));
		int p1_count = 0;

		while (true)
		{
			p1_count++;

			auto max_value = max_element(p1_memory.begin(), p1_memory.end());

			uint32_t size = *max_value;
			uint32_t index = 0;
			for (i = 0; i < 16; i++)
			{
				if (p1_memory[i] == size)
				{
					index = i;
					break;
				}
			}

			p1_memory[index] = 0;

			for (uint32_t i = 1; i < size + 1; i++)
			{
				p1_memory[(index + i) % 16]++;
			}

			uint64_t hv = hash_mem(p1_memory);
			if (p1_states.contains(hv))
			{
				part1 = p1_count;
				break;
			}

			p1_states.insert(hv);
		}

		// part 2
		array<uint32_t, 16> p2_memory;
		copy(memory.begin(), memory.end(), p2_memory.begin());

		unordered_map<uint64_t, uint32_t> p2_states;
		p2_states.insert({ hash_mem(p2_memory), 0 });
		int p2_count = 0;

		while (true)
		{
			p2_count++;

			auto max_value = max_element(p2_memory.begin(), p2_memory.end());

			uint32_t size = *max_value;
			uint32_t index = 0;
			for (i = 0; i < 16; i++)
			{
				if (p2_memory[i] == size)
				{
					index = i;
					break;
				}
			}

			p2_memory[index] = 0;

			for (uint32_t i = 1; i < size + 1; i++)
			{
				p2_memory[(index + i) % 16]++;
			}

			uint64_t hv = hash_mem(p2_memory);
			if (p2_states.contains(hv))
			{
				part2 = p2_count - p2_states[hv];
				break;
			}

			p2_states.insert({ hv, p2_count });
		}

		return { part1, part2 };
	}
};
