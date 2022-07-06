#include "../aocHelper.h"

class Day24 : public BaseDay
{
public:
	Day24() : BaseDay("24") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_set<uint64_t> ports;

		// parse input
		while (*input != '\0')
		{
			uint64_t v1 = numericParse<uint64_t>(input);
			input++; // skip '/'
			uint64_t v2 = numericParse<uint64_t>(input);

			ports.insert(v1 << 32 | v2);

			input++; // skip '\n'
		}

		// part 1
		function < uint64_t(uint64_t, uint64_t, unordered_set<uint64_t>&)> find_strongest;
		find_strongest = [&find_strongest](uint64_t last_port_id, uint64_t curr_strength, unordered_set<uint64_t>& ports_left) -> uint64_t
		{
			uint64_t max_strength = curr_strength;

			for (auto& port : ports_left)
			{
				uint64_t next_port_id;
				bool found = false;
				if ((port >> 32) == last_port_id)
				{
					found = true;
					next_port_id = port & 0xffffffff;
				}
				else if ((port & 0xffffffff) == last_port_id)
				{
					found = true;
					next_port_id = port >> 32;
				}

				if (found)
				{
					unordered_set<uint64_t> n_ports = ports_left;
					n_ports.erase(port);
					uint64_t strength = find_strongest(next_port_id, curr_strength + last_port_id + next_port_id, n_ports);

					max_strength = max(max_strength, strength);
				}
			}

			return max_strength;
		};

		part1 = find_strongest(0, 0, ports);

		// part 2
		function<pair<uint64_t, uint64_t>(uint64_t, uint64_t, uint64_t, unordered_set<uint64_t>&)> find_longest;
		find_longest = [&find_longest](uint64_t last_port_id, uint64_t curr_length, uint64_t curr_strength, unordered_set<uint64_t>& ports_left) -> pair<uint64_t, uint64_t>
		{
			pair<uint64_t, uint64_t> max_strength = { curr_length, curr_strength };

			for (auto& port : ports_left)
			{
				uint64_t next_port_id;
				bool found = false;
				if ((port >> 32) == last_port_id)
				{
					found = true;
					next_port_id = port & 0xffffffff;
				}
				else if ((port & 0xffffffff) == last_port_id)
				{
					found = true;
					next_port_id = port >> 32;
				}

				if (found)
				{
					unordered_set<uint64_t> n_ports = ports_left;
					n_ports.erase(port);
					pair<uint64_t, uint64_t> length = find_longest(next_port_id, curr_length + 1, curr_strength + last_port_id + next_port_id, n_ports);

					max_strength = max(max_strength, length);
				}
			}

			return max_strength;
		};

		auto res = find_longest(0, 0, 0, ports);
		part2 = res.second;

		return { part1, part2 };
	}
};
