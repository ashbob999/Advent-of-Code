#include "../aocHelper.h"

// custon bitset for up to 128 bits
struct custom_bitset
{
	static const unsigned bits_per_value = 64;
	static const unsigned value_count = 2;
	static const uint64_t max = 0xffffffffffffffff;

	uint64_t data[value_count] = { 0, 0 };

	custom_bitset()
	{
		//data[0] = 0;
		//data[1] = 0;
	};

	custom_bitset(const custom_bitset& cb)
	{
		data[0] = cb.data[0];
		data[1] = cb.data[1];
	}

	inline void set(unsigned index)
	{
		unsigned data_index = index / bits_per_value;
		unsigned bit_index = index % bits_per_value;

		if (data_index <= value_count)
		{
			uint64_t val = (uint64_t) 1 << bit_index;

			data[data_index] |= val;
		}
	}

	inline void unset(unsigned index)
	{
		unsigned data_index = index / bits_per_value;
		unsigned bit_index = index % bits_per_value;

		if (data_index <= value_count)
		{
			uint64_t val = (uint64_t) 1 << bit_index;

			data[data_index] &= (max ^ val);
		}
	}

	inline bool get(unsigned index)
	{
		if (index < value_count * bits_per_value)
		{
			unsigned data_index = index / bits_per_value;
			unsigned bit_index = index % bits_per_value;

			uint64_t val = (uint64_t) 1 << bit_index;

			return data[data_index] & val;
		}
		return 0;
	}

	inline unsigned count()
	{
		unsigned cnt = 0;
		for (int i = 0; i < value_count; i++)
		{
			uint64_t t = data[i];
			while (t)
			{
				if (t & 1)
				{
					cnt++;
				}
				t >>= 1;
			}
		}

		return cnt;
	}
};