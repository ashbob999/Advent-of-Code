#include "../aocHelper.h"

class Day12 : public BaseDay
{
public:
	Day12() : BaseDay("12") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<pair<char, int>> data;

		while (*input != '\0')
		{
			char c = *input;
			int n = numericParse<int>(input);

			data.emplace_back(c, n);

			input++;
		}

		// part 1

		int x = 0, y = 0;

		int dir = 90;

		for (auto& v : data)
		{
			switch (v.first)
			{
				case 'L':
				{
					dir -= v.second;
					dir = ((dir % 360) + 360) % 360;
					break;
				}
				case 'R':
				{
					dir += v.second;
					dir = ((dir % 360) + 360) % 360;
					break;
				}
				case 'N':
				{
					y += v.second;
					break;
				}
				case 'E':
				{
					x += v.second;
					break;
				}
				case 'S':
				{
					y -= v.second;
					break;
				}
				case 'W':
				{
					x -= v.second;
					break;
				}
				case 'F':
				{
					switch (dir)
					{
						case 0:
						{
							y += v.second;
							break;
						}
						case 90:
						{
							x += v.second;
							break;
						}
						case 180:
						{
							y -= v.second;
							break;
						}
						case 270:
						{
							x -= v.second;
							break;
						}
					}
					break;
				}

			}

			//cout << x << " " << y << endl;
		}

		part1 = abs(x) + abs(y);

		// part 2

		x = 0, y = 0;
		int wayX = 10, wayY = -1;

		dir = 0;

		for (auto& v : data)
		{
			switch (v.first)
			{
				case 'L':
				{
					int tmpX = wayX, tmpY = wayY;

					switch (4 - (v.second / 90))
					{
						case 1:
						{
							tmpX = -wayY;
							tmpY = wayX;
							break;
						}
						case 2:
						{
							tmpX = -wayX;
							tmpY = -wayY;
							break;
						}
						case 3:
						{
							tmpX = wayY;
							tmpY = -wayX;
							break;
						}
					}

					wayX = tmpX;
					wayY = tmpY;

					break;
				}
				case 'R':
				{
					int tmpX = wayX, tmpY = wayY;

					switch (v.second / 90)
					{
						case 1:
						{
							tmpX = -wayY;
							tmpY = wayX;
							break;
						}
						case 2:
						{
							tmpX = -wayX;
							tmpY = -wayY;
							break;
						}
						case 3:
						{
							tmpX = wayY;
							tmpY = -wayX;
							break;
						}
					}

					wayX = tmpX;
					wayY = tmpY;

					break;
				}
				case 'N':
				{
					wayY -= v.second;
					break;
				}
				case 'E':
				{
					wayX += v.second;
					break;
				}
				case 'S':
				{
					wayY += v.second;
					break;
				}
				case 'W':
				{
					wayX -= v.second;
					break;
				}
				case 'F':
				{
					x += wayX * v.second;
					y += wayY * v.second;
					break;
				}
			}
		}

		part2 = abs(x) + abs(y);

		return { part1, part2 };
	}
};
