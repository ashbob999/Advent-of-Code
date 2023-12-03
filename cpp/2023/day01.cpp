#include "../aocHelper.h"

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::string> lines;

		std::string str;
		str.reserve(64);

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				lines.push_back(str);
				str.clear();
			}
			else
			{
				str += *input;
			}

			input++;
		}

		// part 1
		for (auto&& line : lines)
		{
			int v1 = 0;
			for (auto&& c : line)
			{
				if (c >= '0' && c <= '9')
				{
					v1 = c - '0';
					break;
				}
			}

			int v2 = 0;
			for (int i = line.size() - 1; i >= 0; i--)
			{
				char c = line[i];
				if (c >= '0' && c <= '9')
				{
					v2 = c - '0';
					break;
				}
			}

			part1 += v1 * 10 + v2;
		}

		// part 2
		constexpr std::array<std::pair<const char*, int>, 20> numbers = {
			{{"0", 0},	  {"1", 1},	   {"2", 2},   {"3", 3},	 {"4", 4},	   {"5", 5},   {"6", 6},
			 {"7", 7},	  {"8", 8},	   {"9", 9},   {"zero", 0},	 {"one", 1},   {"two", 2}, {"three", 3},
			 {"four", 4}, {"five", 5}, {"six", 6}, {"seven", 7}, {"eight", 8}, {"nine", 9}}};

		for (auto&& line : lines)
		{
			int v1_index = 1000;
			int v1 = 0;
			for (auto&& [number, value] : numbers)
			{
				int pos = line.find(number);
				if (pos != std::string::npos && pos < v1_index)
				{
					v1_index = pos;
					v1 = value;
				}
			}

			int v2_index = -1;
			int v2 = 0;
			for (auto&& [number, value] : numbers)
			{
				int pos = line.rfind(number);
				if (pos != std::string::npos && pos > v2_index)
				{
					v2_index = pos;
					v2 = value;
				}
			}

			part2 += v1 * 10 + v2;
		}

		return {part1, part2};
	}
};
