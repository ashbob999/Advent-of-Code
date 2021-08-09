#include "../aocHelper.h"

class Day05 : public BaseDay
{
public:
	Day05() : BaseDay("05") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

		auto test_part1 = [](string& s)
		{
			static constexpr bool vowel_index[26] = { true,  false, false, false, // a, b, c, d
													  true,  false, false, false, // e, f, g, h
													  true,  false, false, false, // i, j, k, l
													  false, false, true,  false, // m, n, o, p
													  false, false, false, false, // q, r, s, t
													  true,  false, false, false, // u, v, w, x
													  false, false };             // y, z

			static constexpr char invalid_chars[8] = { 'a', 'b', 'c', 'd', 'p', 'q', 'x', 'y' }; // ab, cd, pq, xy

			bool matches[3] = { false, false, true };

			// contains 3 vowels
			int vowel_count = 0;
			for (auto& c : s)
			{
				if (vowel_index[c - 'a'])
				{
					vowel_count++;
					if (vowel_count >= 3)
					{
						matches[0] = true;
						break;
					}
				}
			}

			if (!matches[0])
			{
				return false;
			}

			for (int i = 0; i < s.size() - 1; i++)
			{
				// letter twice in row
				if (s[i] == s[i + 1])
				{
					matches[1] = true;
				}

				// doesn't contain invalid strings
				for (int index = 0; index < 4; index++)
				{
					if (s[i] == invalid_chars[index * 2] && s[i + 1] == invalid_chars[index * 2 + 1])
					{
						//matches[2] = false;
						return false;
					}
				}
			}

			return matches[1];
		};

		auto test_part2 = [](string& s)
		{
			bool matches[2] = { false, false };

			// letter twice with gap
			for (int i = 0; i < s.size() - 2; i++)
			{
				if (s[i] == s[i + 2])
				{
					matches[0] = true;
					break;
				}
			}

			if (!matches[0])
			{
				return false;
			}

			// check pair appears twice
			for (int i = 0; i < s.size() - 3; i++)
			{
				for (int j = i + 2; j < s.size() - 1; j++)
				{
					if (s[i] == s[j] && s[i + 1] == s[j + 1])
					{
						//matches[1] = true;
						return true;
					}
				}
			}

			return false;
		};

		// parse input
		while (*input != '\0')
		{
			string s;

			while (*input != '\n')
			{
				s += *input;
				input++;
			}

			part1 += test_part1(s);
			part2 += test_part2(s);

			input++; // skip \n
		}

		return { part1, part2 };
	}
};
