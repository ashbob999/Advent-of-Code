#include "../aocHelper.h"

template<int Base = 10>
constexpr long long charp_to_int(const char* str, int size)
{
	long long value = 0;
	if constexpr (Base == 10)
	{
		for (int i = 0; i < size; i++)
		{
			value *= 10;
			value += str[i] - '0';
		}
	}
	else if constexpr (Base == 2)
	{
		for (int i = 0; i < size; i++)
		{
			value <<= 1;
			value |= str[i] - '0';
		}
	}
	else
	{
		static_assert(false, "Base not implemented");
	}

	return value;
}

class Day16 : public BaseDay
{
public:
	Day16() : BaseDay("16") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		string binary;

		while (*input != '\n')
		{
			char c = *input;

			int value = 0;

			if (c >= '0' && c <= '9')
			{
				value = c - '0';
			}
			else
			{
				value = (c - 'A') + 10;
			}

			for (int i = 3; i >= 0; i--)
			{
				if (((value >> i) & 1) == 1)
				{
					binary += '1';
				}
				else
				{
					binary += '0';
				}

			}

			input++;
		}

		binary += '\0';

		static_assert(charp_to_int<10>("123", 3) == 123);
		static_assert(charp_to_int<2>("101", 3) == 5);

		struct Data
		{
			int version = 0;
			int type = 0;
			long long sub_count = 0;
			vector<Data> subs;
			int chars_read = 0;
		};

		function<Data(const char*)> decode;
		decode = [&decode](const char* binary) -> Data
		{
			int version = charp_to_int<2>(binary + 0, 3);
			int type = charp_to_int<2>(binary + 3, 3);
			int chars_read = 3 + 3;

			if (type == 4) // literal
			{
				const char* value_str = binary + 6;
				long long value = 0;

				int i = 0;
				while (true)
				{
					for (int j = 1; j < 5; j++)
					{
						value <<= 1;
						value |= *(value_str + i + j) - '0';
					}

					chars_read += 5;

					if (value_str[i] == '0')
					{
						break;
					}

					i += 5;
				}

				return Data{ version, type, value, {}, chars_read };
			}
			else
			{
				int length_id = charp_to_int<2>(binary + 6, 1);
				chars_read++;

				if (length_id == 0)
				{
					int sub_length = charp_to_int<2>(binary + 7, 15);
					chars_read += 15;

					const char* sub_str = binary + 7 + 15;

					vector<Data> subs;

					int i = 0;
					while (i < sub_length)
					{
						Data sub = decode(sub_str + i);
						subs.push_back(sub);
						i += sub.chars_read;
						chars_read += sub.chars_read;
					}

					return Data{ version, type, sub_length, subs, chars_read };
				}
				else
				{
					int sub_count = charp_to_int<2>(binary + 7, 11);
					chars_read += 11;

					const char* sub_str = binary + 7 + 11;

					vector<Data> subs;

					int i = 0;
					for (int c = 0; c < sub_count; c++)
					{
						Data sub = decode(sub_str + i);
						subs.push_back(sub);
						i += sub.chars_read;
						chars_read += sub.chars_read;
					}

					return Data{ version, type, sub_count, subs, chars_read };
				}
			}
		};

		Data decoded = decode(binary.c_str());

		// part 1
		function<long long(Data&)> sum_versions;
		sum_versions = [&sum_versions](Data& data) -> long long
		{
			if (data.type == 4)
			{
				return data.version;
			}
			else
			{
				long long sum = data.version;
				for (auto& sub : data.subs)
				{
					sum += sum_versions(sub);
				}
				return sum;
			}
		};

		part1 = sum_versions(decoded);

		// part 2

		function<long long(Data&)> calculate;
		calculate = [&calculate](Data& data) -> long long
		{
			switch (data.type)
			{
				case 0: // sum
				{
					return std::accumulate(data.subs.begin(), data.subs.end(), 0LL, [&](const long long& value, Data& b)
					{
						return value + calculate(b);
					});
				}
				case 1: // product
				{
					return std::accumulate(data.subs.begin(), data.subs.end(), 1LL, [&](const long long& value, Data& b)
					{
						return value * calculate(b);
					});
				}
				case 2: // min
				{
					long long min_value = LLONG_MAX;
					for (auto& sub : data.subs)
					{
						min_value = min(min_value, calculate(sub));
					}
					return min_value;
				}
				case 3: // max
				{
					long long max_value = 0;
					for (auto& sub : data.subs)
					{
						max_value = max(max_value, calculate(sub));
					}
					return max_value;
				}
				case 4: // literal
				{
					return data.sub_count;
				}
				case 5: // greater than
				{
					long long v0 = calculate(data.subs[0]);
					long long v1 = calculate(data.subs[1]);
					if (v0 > v1)
					{
						return 1;
					}
					else
					{
						return 0;
					}
				}
				case 6: // less than
				{
					long long v0 = calculate(data.subs[0]);
					long long v1 = calculate(data.subs[1]);
					if (v0 < v1)
					{
						return 1;
					}
					else
					{
						return 0;
					}
				}
				case 7: // equal to
				{
					long long v0 = calculate(data.subs[0]);
					long long v1 = calculate(data.subs[1]);
					if (v0 == v1)
					{
						return 1;
					}
					else
					{
						return 0;
					}
				}
			}
		};

		part2 = calculate(decoded);

		return { part1, part2 };
	}
};
