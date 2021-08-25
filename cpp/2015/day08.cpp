#include "../aocHelper.h"

class Day08 : public BaseDay
{
public:
	Day08() : BaseDay("08") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

		struct count
		{
			int code;
			int char_;
		};

		count p1_count = { 0,0 }, p2_count = { 0,0 };

		int lines = 0;

		// parse input
		while (*input != '\0')
		{
			char* line_start = input;

			int line_length = 0;
			while (*input != '\n')
			{
				line_length++;
				input++;
			}

			// part 1
			p1_count.code += line_length;

			int i = 0;
			while (i < line_length)
			{
				if (*(line_start + i) == '\\')
				{
					if (*(line_start + i + 1) == '\\' || *(line_start + i + 1) == '"')
					{
						p1_count.char_++;
						i++;
					}
					else if (*(line_start + i + 1) == 'x')
					{
						p1_count.char_++;
						i += 3;
					}
					else
					{
						p1_count.char_++;
					}
				}
				else
				{
					p1_count.char_++;
				}
				i++;
			}

			// part 2
			p2_count.code += line_length;

			for (int index = 0; index < line_length; index++)
			{
				if (*(line_start + index) == '"' || *(line_start + index) == '\\')
				{
					p2_count.char_++;
				}
				p2_count.char_++;
			}

			lines++;
			input++; // skip \n
		}

		// part 1
		p1_count.char_ -= 2 * lines;
		part1 = p1_count.code - p1_count.char_;

		// part 2
		p2_count.char_ += 2 * lines;
		part2 = p2_count.char_ - p2_count.code;

		return { part1, part2 };
	}
};
