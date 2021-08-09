#include "../aocHelper.h"
#include "md5_simd/md5-simd.h"

#include <immintrin.h>

constexpr char char_map[10] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };

class Day04 : public BaseDay
{
public:
	Day04() : BaseDay("04") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

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




		//string key;
		char buffer[100];
		fill(buffer, buffer + 100, '\0');

		int key_length = 0;

		// get input
		while (*input != '\n')
		{
			//key += *input;
			buffer[key_length] = *input;
			key_length++;
			input++;
		}

		int number = 1;

		char* buffers[8];
		buffers[0] = new char[128];
		buffers[1] = new char[128];
		buffers[2] = new char[128];
		buffers[3] = new char[128];
		buffers[4] = new char[128];
		buffers[5] = new char[128];
		buffers[6] = new char[128];
		buffers[7] = new char[128];

		uint64_t lengths[8];

		md5_simd::MD5_SIMD md5;

		while (true)
		{
			// fill buffers
			for (int i = 0; i < 8; i++)
			{
				int num = number + i;
				int digits = digit_count(num);

				lengths[i] = key_length + digits; // set the buffer string length

				buffers[i][key_length + digits] = '\0'; // set char after init string to 0
				memcpy(buffers[i], buffer, key_length); // copy init string

				// convert the number to a string, and add it to the buffer
				int index = key_length + digits - 1;
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
					part1 = number + buffer_index;
					goto solve_part2;
				}
			}

			number += 8;
		}

	solve_part2:

		number = part1 + 1;

		while (true)
		{
			// fill buffers
			for (int i = 0; i < 8; i++)
			{
				int num = number + i;
				int digits = digit_count(num);

				lengths[i] = key_length + digits; // set the buffer string length

				buffers[i][key_length + digits] = '\0'; // set char after init string to 0
				memcpy(buffers[i], buffer, key_length); // copy init string

				// convert the number to a string, and add it to the buffer
				int index = key_length + digits - 1;
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
				if (md5.check_zeroes<6>(buffer_index)) // check the hashes for leading zeroes
				{
					part2 = number + buffer_index;
					goto end;
				}
			}

			number += 8;
		}

	end:

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
