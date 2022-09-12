#include "../aocHelper.h"

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int bit_count = 12;

		vector<uint16_t> values;

		while (*input != '\0')
		{
			uint16_t n = 0;

			for (int i = 0; i < bit_count; i++)
			{
				n <<= 1;
				if (*input == '1')
				{
					n |= 1;
				}
				input++;
			}

			values.push_back(n);

			input++; // skip '\n'
		}

		// part 1
		uint16_t gamma = 0;
		uint16_t epsilon = 0;

		for (uint16_t i = 0, mask = 1; i < bit_count; i++, mask <<= 1)
		{
			int c = 0;
			for (auto& v : values)
			{
				if ((v & mask) > 0)
				{
					c++;
				}
			}

			if (c >= (values.size() / 2 + (values.size() % 2)))
			{
				gamma |= mask;
			}
			else
			{
				epsilon |= mask;
			}
		}

		part1 = gamma * epsilon;

		// part 2
		auto get_oxygen_rating = [&bit_count](vector<uint16_t>& values)
		{
			vector<uint16_t> left = values;

			uint16_t mask = 1 << (bit_count - 1);

			while (left.size() > 1)
			{
				int c = 0;

				for (auto& v : left)
				{
					if ((v & mask) > 0)
					{
						c++;
					}
				}

				if (c >= (left.size() / 2 + (left.size() % 2)))
				{
					vector<uint16_t> new_left;
					for (auto& v : left)
					{
						if ((v & mask) > 0)
						{
							new_left.push_back(v);
						}
					}
					left = new_left;
				}
				else
				{
					vector<uint16_t> new_left;
					for (auto& v : left)
					{
						if ((v & mask) == 0)
						{
							new_left.push_back(v);
						}
					}
					left = new_left;
				}

				mask >>= 1;
			}

			return left[0];
		};

		auto get_co2_rating = [&bit_count](vector<uint16_t>& values)
		{
			vector<uint16_t> left = values;

			uint16_t mask = 1 << (bit_count - 1);

			while (left.size() > 1)
			{
				int c = 0;

				for (auto& v : left)
				{
					if ((v & mask) > 0)
					{
						c++;
					}
				}

				if (c >= (left.size() / 2 + (left.size() % 2)))
				{
					vector<uint16_t> new_left;
					for (auto& v : left)
					{
						if ((v & mask) == 0)
						{
							new_left.push_back(v);
						}
					}
					left = new_left;
				}
				else
				{
					vector<uint16_t> new_left;
					for (auto& v : left)
					{
						if ((v & mask) > 0)
						{
							new_left.push_back(v);
						}
					}
					left = new_left;
				}

				mask >>= 1;
			}

			return left[0];
		};

		part2 = get_oxygen_rating(values) * get_co2_rating(values);

		return { part1, part2 };
	}
};
