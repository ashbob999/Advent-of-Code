#include "../aocHelper.h"

#include "md5_simd/md5-simd.h"

class Day14 : public BaseDay
{
public:
	Day14() : BaseDay("14") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr char char_map[10] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };

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

		char* md5_buffers[8];
		md5_buffers[0] = new char[32];
		md5_buffers[1] = new char[32];
		md5_buffers[2] = new char[32];
		md5_buffers[3] = new char[32];
		md5_buffers[4] = new char[32];
		md5_buffers[5] = new char[32];
		md5_buffers[6] = new char[32];
		md5_buffers[7] = new char[32];

		md5_simd::MD5_SIMD md5;

		auto get_hash = [&](unordered_map<int, string>& mem, unordered_set<int>& base_nums, int number, int times)
		{
			array<string, 8> hashes;
			if (base_nums.contains(number))
			{
				for (int i = 0; i < 8; i++)
				{
					hashes[i] = mem[number + i];
				}
			}
			else
			{
				// do it once
				for (int i = 0; i < 8; i++)
				{
					int num = number + i;
					int digits = digit_count(num);

					lengths[i] = id_length + digits; // set the buffer string length

					buffers[i][id_length + digits] = '\0'; // set char after init string to 0
					memcpy(buffers[i], buffer, id_length); // copy init string

					// convert the number to a string, and add it to the buffer
					int index = id_length + digits - 1;
					if (num == 0)
					{
						buffers[i][index] = '0';
					}
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
					md5.hexdigest(md5_buffers[buffer_index], buffer_index);
				}

				// do it the rest amount of times
				for (int t = 0; t < times - 1; t++)
				{
					// fill buffers
					for (int i = 0; i < 8; i++)
					{
						memcpy(buffers[i], md5_buffers[i], 32);
						lengths[i] = 32;
					}

					md5.calculate<8, false>(buffers, lengths); // calculate the hashes

					for (int buffer_index = 0; buffer_index < 8; buffer_index++)
					{
						md5.hexdigest(md5_buffers[buffer_index], buffer_index);
					}
				}

				// store the final hashes
				for (int buffer_index = 0; buffer_index < 8; buffer_index++)
				{
					hashes[buffer_index] = string{ md5_buffers[buffer_index], md5_buffers[buffer_index] + 32 };
					mem[number + buffer_index] = hashes[buffer_index];
				}
				base_nums.insert(number);
			}

			return hashes;
		};

		auto check_n = [&](string& s, int n) -> pair<bool, char>
		{
			for (int i = 0; i < s.length() - n + 1; i++)
			{
				char c = s[i];
				if (all_of(&s[i + 1], &s[i + n], [&](char c_) { return c_ == c; }))
				{
					return { true, c };
				}
			}
			return { false, '\0' };
		};

		auto check_match = [&](string& s, int n, char c)
		{
			for (int i = 0; i < s.length() - n + 1; i++)
			{
				if (all_of(&s[i], &s[i + n], [&](char c_) { return c_ == c; }))
				{
					return true;
				}
			}
			return false;
		};

		auto is_key = [&](int number, unordered_map<int, string>& mem, unordered_set<int>& base_nums, int times) -> pair<bool, int>
		{
			array<string, 8> hashes = get_hash(mem, base_nums, number, times);

			for (int i = 0; i < 8; i++)
			{
				string& s = hashes[i];

				auto res = check_n(s, 3);
				if (res.first)
				{
					// check next 1000 hashes
					// do whole 8 sets of hashes
					for (int j = 0; j < 1000 / 8; j++)
					{
						array<string, 8> hs = get_hash(mem, base_nums, number + i + j * 8 + 1, times);
						for (int k = 0; k < 8; k++)
						{
							auto c = check_match(hs[k], 5, res.second);
							if (c)
							{
								return { true, number + i };
							}
						}
					}
				}
			}

			return { false, 0 };
		};

		// part 1

		unordered_map<int, string> mem_hash1;
		unordered_set<int> base_numbers1;

		int i = 0;
		int key_count = 0;

		while (true)
		{
			auto res = is_key(i, mem_hash1, base_numbers1, 1);
			if (res.first)
			{
				key_count++;
				i = res.second;

				if (key_count == 64)
				{
					break;
				}

				i++;
			}
			else
			{
				i += 8;
			}
		}

		part1 = i;

		// part 2
		unordered_map<int, string> mem_hash2;
		unordered_set<int> base_numbers2;

		i = 0;
		key_count = 0;

		while (true)
		{
			auto res = is_key(i, mem_hash2, base_numbers2, 1 + 2016);
			if (res.first)
			{
				key_count++;
				i = res.second;

				if (key_count == 64)
				{
					break;
				}

				i++;
			}
			else
			{
				i += 8;
			}
		}

		part2 = i;

		delete[] buffers[0];
		delete[] buffers[1];
		delete[] buffers[2];
		delete[] buffers[3];
		delete[] buffers[4];
		delete[] buffers[5];
		delete[] buffers[6];
		delete[] buffers[7];

		delete[] md5_buffers[0];
		delete[] md5_buffers[1];
		delete[] md5_buffers[2];
		delete[] md5_buffers[3];
		delete[] md5_buffers[4];
		delete[] md5_buffers[5];
		delete[] md5_buffers[6];
		delete[] md5_buffers[7];

		return { part1, part2 };
	}
};
