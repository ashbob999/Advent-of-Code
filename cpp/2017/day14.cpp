#include "../aocHelper.h"

#include <immintrin.h>

class Day14 : public BaseDay
{
public:
	Day14() : BaseDay("14") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		string key;

		while (*input != '\n')
		{
			key += *input;
			input++;
		}

		auto calc_round = [](array<uint8_t, 256> numbers, vector<uint8_t>& lengths, int index = 0, int skip_size = 0)
		{
			array<uint8_t, 256> nums;
			copy(numbers.begin(), numbers.end(), nums.begin());

			for (auto& length : lengths)
			{
				for (int ni = 0; ni < length / 2; ni++)
				{
					int i1 = (index + ni) % nums.size();
					int i2 = (index + length - 1 - ni) % nums.size();

					uint8_t tmp = nums[i1];
					nums[i1] = nums[i2];
					nums[i2] = tmp;
				}

				index += skip_size + length;
				skip_size++;
			}

			return pair<array<uint8_t, 256>, pair<int, int>>{ nums, { index, skip_size } };
		};

		auto int_to_hex = [](uint8_t v)
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

		auto hex_to_int = [](char c)
		{
			if (c >= '0' && c <= '9')
			{
				return (uint8_t) (c - '0');
			}
			else
			{
				return (uint8_t) (c - 'a' + 10);
			}
		};

		auto calc_hash = [&calc_round, &int_to_hex](string key)
		{
			vector<uint8_t> p2_lengths;
			for (auto& c : key)
			{
				p2_lengths.push_back(c);
			}
			p2_lengths.push_back(17);
			p2_lengths.push_back(31);
			p2_lengths.push_back(73);
			p2_lengths.push_back(47);
			p2_lengths.push_back(23);

			array<uint8_t, 256> numbers;
			for (int i = 0; i < 256; i++)
			{
				numbers[i] = i;
			}

			int index = 0;
			int skip_size = 0;

			array<uint8_t, 256> p2_nums;
			copy(numbers.begin(), numbers.end(), p2_nums.begin());

			for (int i = 0; i < 64; i++)
			{
				auto res = calc_round(p2_nums, p2_lengths, index, skip_size);

				copy(res.first.begin(), res.first.end(), p2_nums.begin());
				index = res.second.first;
				skip_size = res.second.second;
			}

			array<uint8_t, 16> dense{};

			for (int i = 0; i < 256; i++)
			{
				dense[i / 16] ^= p2_nums[i];
			}

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

			return hash_str;
		};

		// part 1
		array<array<uint32_t, 4>, 128> grid{};

		for (int y = 0; y < 128; y++)
		{
			array<char, 32> row_hash = calc_hash(key + "-" + to_string(y));

			for (int x = 0; x < 4; x++)
			{
				for (int i = 0; i < 8; i++)
				{
					grid[y][x] |= (uint64_t) hex_to_int(row_hash[x * 8 + i]) << ((7 - i) * 4);
				}
			}
		}

		for (int y = 0; y < 128; y++)
		{
			for (int x = 0; x < 4; x++)
			{
				part1 += _mm_popcnt_u32(grid[y][x]);
			}
		}

		// part 2
		auto find_region = [&grid](uint64_t start)
		{
			unordered_set<uint64_t> points;
			points.insert(start);

			deque<uint64_t> to_check;
			to_check.push_back(start);

			while (to_check.size() > 0)
			{
				uint64_t curr_pos = to_check.front();
				to_check.pop_front();

				points.insert(curr_pos);


				int x_pos = curr_pos >> 32;
				int y_pos = curr_pos & 0xffffffff;

				for (int y = -1; y < 2; y++)
				{
					int new_y = y_pos + y;
					if (y != 0 && new_y >= 0 && new_y < 128)
					{
						uint64_t p = (uint64_t) x_pos << 32 | (uint64_t) new_y;
						if (!points.contains(p) && ((grid[new_y][x_pos / 32] >> (31 - x_pos % 32)) & 1) == 1)
						{
							to_check.push_back(p);
						}
					}
				}

				for (int x = -1; x < 2; x++)
				{
					int new_x = x_pos + x;
					if (x != 0 && new_x >= 0 && new_x < 128)
					{
						uint64_t p = (uint64_t) new_x << 32 | (uint64_t) y_pos;
						if (!points.contains(p) && ((grid[y_pos][new_x / 32] >> (31 - new_x % 32)) & 1) == 1)
						{
							to_check.push_back(p);
						}
					}
				}
			}

			return points;
		};

		unordered_set<uint64_t> positions;
		for (uint64_t y = 0; y < 128; y++)
		{
			for (uint64_t x = 0; x < 4; x++)
			{
				for (uint64_t i = 0; i < 32; i++)
				{
					if (((grid[y][x] >> (31 - i)) & 1) == 1)
					{
						positions.insert((x * 32 + i) << 32 | y);
					}
				}
			}
		}

		while (positions.size() > 0)
		{
			uint64_t curr_pos = *positions.begin();

			unordered_set<uint64_t> region = find_region(curr_pos);

			part2++;

			for (auto& v : region)
			{
				positions.erase(v);
			}
		}

		return { part1, part2 };
	}
};
