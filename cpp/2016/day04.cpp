#include "../aocHelper.h"

template<int N = 0>
int mem_to_int_length(const char* buf, int len) // spaces, sign, digits
{
	int n = 0, sign = 1;

	while (len && isspace(*buf))
		--len, ++buf;

	if (len) switch (*buf)
	{
		case '-':       sign = -1;        \
		case '+':       --len, ++buf;
	}

	while (len-- && isdigit(*buf))
		n = n * 10 + *buf++ - '0';

	return n * sign;
}

class Day04 : public BaseDay
{
public:
	Day04() : BaseDay("04") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct room
		{
			vector<pair<char*, int>> names;
			int id = 0;
			pair<char*, int> checksum;
		};

		auto check = [](room& r)
		{
			unordered_map<char, int> counts;

			for (auto& name : r.names)
			{
				for (int i = 0; i < name.second; i++)
				{
					char c = name.first[i];
					if (counts.contains(c))
					{
						counts[c]++;
					}
					else
					{
						counts[c] = 1;
					}
				}
			}

			vector<pair<int, int>> chars;
			for (auto& p : counts)
			{
				chars.emplace_back(p.second, 'a' - p.first);
			}

			sort(chars.begin(), chars.end(), std::greater<pair<int, int>>());

			char check_sum[5]{ '\0' };
			for (int i = 0; i < 5; i++)
			{
				check_sum[i] = (char) ('a' - chars[i].second);
			}

			if (r.checksum.second == 5 && strncmp(r.checksum.first, check_sum, 5) == 0)
			{
				return true;
			}
			return false;
		};

		auto decrypt = [](room& r)
		{
			unordered_set<string> decrypted;

			for (auto& n : r.names)
			{
				string s;

				for (int i = 0; i < n.second; i++)
				{
					char c = n.first[i];
					int index = c - 'a';
					index += r.id;
					index %= 26;
					index += (index < 0) ? 26 : 0;
					s += 'a' + index;
				}

				decrypted.insert(s);
			}

			return decrypted;
		};

		string target = "northpole";

		char* text_start = input;
		room curr_room;
		int text_length = 0;

		// parse input
		while (*input != '\0')
		{
			if (*input == '-')
			{
				curr_room.names.emplace_back(text_start, text_length);
				text_length = 0;
				text_start = input + 1;
			}
			else if (*input == '[')
			{
				curr_room.id = mem_to_int_length(text_start, text_length);
				text_length = 0;
				text_start = input + 1;
			}
			else if (*input == ']')
			{
				curr_room.checksum = { text_start, text_length };
				text_length = 0;
				text_start = input + 2;

				// part 2
				if (check(curr_room))
				{
					part1 += curr_room.id;

					// part 2
					auto decrypted = decrypt(curr_room);

					if (part2 == 0 && decrypted.contains(target))
					{
						part2 = curr_room.id;
					}
				}

				curr_room = room();
				input++;
			}
			else
			{
				text_length++;
			}
			input++;
		}

		return { part1, part2 };
	}
};
