#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<pair<char*, int>> buttons;

		char* start = input;
		int length = 0;

		// parse input
		while (*input != '\0')
		{
			if (*input == '\n')
			{
				buttons.emplace_back(start, length);
				input++;
				start = input;
				length = 0;
			}
			else
			{
				length++;
				input++;
			}
		}

		// cheaty hack again
		union location
		{
			int32_t pos[2] = { 0, 0 };
			uint64_t mixed;
		};

		auto solve = [&](unordered_map<uint64_t, char> button_locations)
		{
			location pos{ 0, 0 };
			string code;

			for (auto& button : buttons)
			{
				for (int i = 0; i < button.second; i++)
				{
					switch (*(button.first + i))
					{
						case 'U':
						{
							if (button_locations.contains(location{ pos.pos[0], pos.pos[1] - 1 }.mixed))
							{
								pos.pos[1]--;
							}
							break;
						}
						case 'D':
						{
							if (button_locations.contains(location{ pos.pos[0], pos.pos[1] + 1 }.mixed))
							{
								pos.pos[1]++;
							}
							break;
						}
						case 'L':
						{
							if (button_locations.contains(location{ pos.pos[0] - 1, pos.pos[1] }.mixed))
							{
								pos.pos[0]--;
							}
							break;
						}
						case 'R':
						{
							if (button_locations.contains(location{ pos.pos[0] + 1, pos.pos[1] }.mixed))
							{
								pos.pos[0]++;
							}
							break;
						}
					}
				}

				code += button_locations[pos.mixed];
			}

			return code;
		};

		// part 1
		unordered_map<uint64_t, char> button_locations_p1 = {
			{ location{ -1, -1 }.mixed, '1' },
			{ location{  0, -1 }.mixed, '2' },
			{ location{  1, -1 }.mixed, '3' },
			{ location{ -1,  0 }.mixed, '4' },
			{ location{  0,  0 }.mixed, '5' },
			{ location{  1,  0 }.mixed, '6' },
			{ location{ -1,  1 }.mixed, '7' },
			{ location{  0,  1 }.mixed, '8' },
			{ location{  1,  1 }.mixed, '9' },
		};

		string p1_res = solve(button_locations_p1);

		for (int i = 0; i < p1_res.length(); i++)
		{
			this->stringResult.first[i] = p1_res[i];
		}

		// part 2
		unordered_map<uint64_t, char> button_locations_p2 = {
			{ location{  0, -2 }.mixed, '1' },
			{ location{ -1, -1 }.mixed, '2' },
			{ location{  0, -1 }.mixed, '3' },
			{ location{  1, -1 }.mixed, '4' },
			{ location{ -2,  0 }.mixed, '5' },
			{ location{ -1,  0 }.mixed, '6' },
			{ location{  0,  0 }.mixed, '7' },
			{ location{  1,  0 }.mixed, '8' },
			{ location{  2,  0 }.mixed, '9' },
			{ location{ -1,  1 }.mixed, 'A' },
			{ location{  0,  1 }.mixed, 'B' },
			{ location{  1,  1 }.mixed, 'C' },
			{ location{  0,  1 }.mixed, 'D' },
		};

		string p2_res = solve(button_locations_p2);

		for (int i = 0; i < p2_res.length(); i++)
		{
			this->stringResult.second[i] = p2_res[i];
		}

		return { part1, part2 };
	}
};
