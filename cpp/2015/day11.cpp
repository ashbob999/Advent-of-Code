#include "../aocHelper.h"

class Day11 : public BaseDay
{
public:
	Day11() : BaseDay("11")
	{}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		auto get_next_string = [](char* text, int length)
		{
			if (text[length - 1] == 'z') // overflow
			{
				int i = length - 1;
				bool overflow = true;

				while (overflow && i >= 0)
				{
					text[i] = 'a';
					i--;
					overflow = (text[i] == 'z');

					if (!overflow)
					{
						text[i]++;
					}
				}
			}
			else // increment last char
			{
				text[length - 1]++;
			}
		};

		auto get_next_password = [&get_next_string](char* text, int length)
		{
			while (true)
			{
				get_next_string(text, length);

				// not contain i, o, l
				for (int i = 0; i < length; i++)
				{
					if (text[i] == 'i' || text[i] == 'l' || text[i] == 'l')
					{
						continue;
					}
				}

				// increasing straight of 3 letters
				bool has_straight = false;
				for (int i = 0; i < length - 2; i++)
				{
					char c1 = text[i];
					char c2 = text[i] + 1;
					char c3 = text[i] + 2;

					if (text[i + 1] == c2 && text[i + 2] == c3)
					{
						has_straight = true;
						break;
					}
				}

				if (!has_straight)
				{
					continue;
				}

				// 2 different pairs
				auto check_pairs = [&text, &length]()
				{
					for (int i = 0; i < length - 2; i++)
					{
						if (text[i] == text[i + 1])
						{
							for (int j = i + 2; j < length - 1; j++)
							{
								if (text[j] == text[j + 1] && text[i] != text[j])
								{
									return true;
								}
							}
						}
					}
					return false;
				};

				if (!check_pairs())
				{
					continue;
				}

				break;
			}
		};

		int length = 0;

		// parse input
		while (*input != '\n')
		{
			length++;
			input++;
		}

		input -= length;

		// copy input
		char* text = new char[length + 1];
		memcpy(text, input, length);
		text[length] = '\0';

		// part 1
		get_next_password(text, length);

		// copy answer to stringResult
		for (int i = 0; i < length; i++)
		{
			stringResult.first[i] = text[i];
		}

		// part 2
		get_next_password(text, length);

		// copy answer to stringResult
		for (int i = 0; i < length; i++)
		{
			stringResult.second[i] = text[i];
		}

		delete[] text;

		return { part1, part2 };
	}
};
