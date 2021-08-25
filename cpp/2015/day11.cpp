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

			}
			else // increment last char
			{
				text[length - 1]++;
			}
		};

		auto get_next_password = [&get_next_string](char* text, int length)
		{

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

		return { part1, part2 };
	}
};
