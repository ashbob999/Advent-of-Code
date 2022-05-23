#include "../aocHelper.h"
#include "md5_simd/md5-simd.h"

constexpr char char_map[10] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };

class Day05 : public BaseDay
{
public:
	Day05() : BaseDay("05") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		auto digit_count = [](int number)
		{
			if (number < 10) return 1;
			if (number < 100) return 2;
			if (number < 1000) return 3;
			if (number < 10000) return 4;
			if (number < 100000) return 5;
			if (number < 1000000) return 6;
			if (number < 10000000) return 7;
			if (number < 100000000) return 8;
			if (number < 1000000000) return 9;
			return 10;
		};

		// parse input
		char buffer[100]{ '\0' };

		int id_length = 0;
		while (*input != '\n')
		{
			buffer[id_length] = *input;
			input++;
			id_length++;
		}

		// setup md5
		uint64_t lengths[8];

		char* buffers[8];
		buffers[0] = new char[128];
		buffers[1] = new char[128];
		buffers[2] = new char[128];
		buffers[3] = new char[128];
		buffers[4] = new char[128];
		buffers[5] = new char[128];
		buffers[6] = new char[128];
		buffers[7] = new char[128];

		md5_simd::MD5_SIMD md5;

		auto check_hash = [&](int number)->pair<int, pair<char, char>>
		{
			// fill buffers
			for (int i = 0; i < 8; i++)
			{
				int num = number + i;
				int digits = digit_count(num);

				lengths[i] = id_length + digits; // set the buffer string length

				buffers[i][id_length + digits] = '\0'; // set char after init string to 0
				memcpy(buffers[i], buffer, id_length); // copy init string

				// convert the number to a string, and add it to the buffer
				int index = id_length + digits - 1;
				while (num > 0)
				{
					buffers[i][index] = char_map[num % 10];
					num /= 10;
					index--;
				}
			}

			md5.calculate<8, false>(buffers, lengths); // calculate the hashes

			for (int buffer_index = 0; buffer_index < 8; buffer_index++)
			{
				if (md5.check_zeroes<5>(buffer_index)) // check the hashes for leading zeroes
				{
					char output[32];
					md5.hexdigest(output, buffer_index);
					return pair<int, pair<char, char>>{ number + buffer_index, { output[5], output[6] } };
				}
			}

			return pair<int, pair<char, char>>{ -1, { '\0', '\0' } };
		};

		// part 1
		int found = 0;
		int number = 0;
		char p1_out[8]{ '\0' };

		while (found < 8)
		{
			pair<int, pair<char, char>> res = check_hash(number);

			if (res.first >= 0)
			{
				p1_out[found] = res.second.first;
				found++;
				number = res.first + 1;
			}
			else
			{
				number += 8;
			}
		}

		memcpy(this->stringResult.first, p1_out, 8);

		// part 2
		found = 0;
		number = 0;
		char p2_out[8]{ '\0' };

		while (found < 8)
		{
			pair<int, pair<char, char>> res = check_hash(number);

			if (res.first >= 0)
			{
				if (res.second.first >= '0' && res.second.first <= '7')
				{
					int idx = res.second.first - '0';
					if (p2_out[idx] == '\0')
					{
						p2_out[idx] = res.second.second;
						found++;
					}
				}
				number = res.first + 1;
			}
			else
			{
				number += 8;
			}
		}

		memcpy(this->stringResult.second, p2_out, 8);

		delete[] buffers[0];
		delete[] buffers[1];
		delete[] buffers[2];
		delete[] buffers[3];
		delete[] buffers[4];
		delete[] buffers[5];
		delete[] buffers[6];
		delete[] buffers[7];

		return { part1, part2 };
	}
};
