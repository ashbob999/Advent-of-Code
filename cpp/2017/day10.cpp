#include "../aocHelper.h"

class Day10 : public BaseDay
{
public:
	Day10() : BaseDay("10") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<uint8_t> lengths;
		string input_str;

		// parse input
		while (*input != '\n')
		{
			uint8_t n = numericParse<uint8_t>(input);
			lengths.push_back(n);

			if (*input == ',')
			{
				input++; // skip ','
			}
		}

		input = this->input_start;

		while (*input != '\n')
		{
			input_str += *input;
			input++;
		}

		auto calc_hash = [](array<uint8_t, 256> numbers, vector<uint8_t>& lengths, int index = 0, int skip_size = 0)
		{
			array<uint8_t, 256> nums;
			copy(numbers.begin(), numbers.end(), nums.begin());

			for (auto& length : lengths)
			{
				for (int ni = 0; ni < length / 2; ni++)
				{
					int i1 = (index + ni) % nums.size();
					int i2 = (index + length - 1 - ni) % nums.size();

					//cout << i1 << " " << i2 << endl;

					uint8_t tmp = nums[i1];
					nums[i1] = nums[i2];
					nums[i2] = tmp;
				}

				index += skip_size + length;
				skip_size++;
			}

			return pair<array<uint8_t, 256>, pair<int, int>>{ nums, { index, skip_size } };
		};

		array<uint8_t, 256> numbers;
		for (int i = 0; i < 256; i++)
		{
			numbers[i] = i;
		}

		// part 1
		auto res = calc_hash(numbers, lengths);
		part1 = res.first[0] * res.first[1];

		// part 2

		vector<uint8_t> p2_lengths;
		for (auto& c : input_str)
		{
			p2_lengths.push_back(c);
		}
		p2_lengths.push_back(17);
		p2_lengths.push_back(31);
		p2_lengths.push_back(73);
		p2_lengths.push_back(47);
		p2_lengths.push_back(23);

		int index = 0;
		int skip_size = 0;

		array<uint8_t, 256> p2_nums;
		copy(numbers.begin(), numbers.end(), p2_nums.begin());

		for (int i = 0; i < 64; i++)
		{
			auto res = calc_hash(p2_nums, p2_lengths, index, skip_size);

			copy(res.first.begin(), res.first.end(), p2_nums.begin());
			index = res.second.first;
			skip_size = res.second.second;
		}

		array<uint8_t, 16> dense{};

		for (int i = 0; i < 256; i++)
		{
			dense[i / 16] ^= p2_nums[i];
		}

		auto int_to_hex = [](int v)
		{
			if (v < 10)
			{
				return (char) ('0' + v);
			}
			else
			{
				return (char) ('a' + (v - 10));
			}
		};

		array<char, 32> hash_str;

		for (int i = 0; i < 16; i++)
		{
			uint8_t d = dense[i];

			if ((d & 0xf0) != 0)
			{
				hash_str[i * 2] = int_to_hex(d >> 4);
			}
			else
			{
				hash_str[i * 2] = '0';
			}

			hash_str[i * 2 + 1] = int_to_hex(d & 0xf);
		}

		memcpy(stringResult.second, hash_str.data(), hash_str.size());

		return { part1, part2 };
	}
};
