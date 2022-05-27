#include "../aocHelper.h"

class Day16 : public BaseDay
{
public:
	Day16() : BaseDay("16") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		string input_string;

		while (*input != '\n')
		{
			input_string += *input;
			input++;
		}

		auto step = [](string& state)
		{
			state += '0';

			// swap zeros and ones, but in reverse
			for (int i = state.length() - 2; i >= 0; i--)
			{
				if (state[i] == '0')
				{
					state += '1';
				}
				else
				{
					state += '0';
				}
			}
		};

		function<string(string::iterator, string::iterator, long long)> checksum;
		checksum = [&checksum](string::iterator start, string::iterator end, long long size) -> string
		{
			string cs;

			for (int i = 0; i < size; i += 2)
			{
				if (*(start + i) == *(start + i + 1))
				{
					cs += '1';
				}
				else
				{
					cs += '0';
				}
			}

			if (cs.length() % 2 == 0)
			{
				return checksum(cs.begin(), cs.end(), cs.length());
			}

			return cs;
		};

		auto randomise = [&step, &checksum](string& init_state, long long size) -> string
		{
			string state{ init_state };
			while (state.length() < size)
			{
				step(state);
			}

			string check = checksum(state.begin(), state.begin() + size, size);

			return check;
		};

		// part 1
		string p1 = randomise(input_string, 272);
		memcpy(this->stringResult.first, p1.c_str(), p1.length());

		// part 2
		string p2 = randomise(input_string, 35651584);
		memcpy(this->stringResult.second, p2.c_str(), p2.length());

		return { part1, part2 };
	}
};
