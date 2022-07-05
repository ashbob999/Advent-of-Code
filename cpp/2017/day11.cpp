#include "../aocHelper.h"

class Day11 : public BaseDay
{
public:
	Day11() : BaseDay("11") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		enum class dir
		{
			n,
			nw,
			ne,
			s,
			sw,
			se,
		};

		vector<dir> moves;

		// parse input
		while (*input != '\n')
		{
			if (*input == 'n')
			{
				input++; // skip 'n'

				if (*input == 'w')
				{
					input++; // skip 'w'
					moves.push_back(dir::nw);
				}
				else if (*input == 'e')
				{
					input++; // skip 'e'
					moves.push_back(dir::ne);
				}
				else
				{
					moves.push_back(dir::n);
				}
			}
			else if (*input == 's')
			{
				input++; // skip 's'

				if (*input == 'w')
				{
					input++; // skip 'w'
					moves.push_back(dir::sw);
				}
				else if (*input == 'e')
				{
					input++; // skip 'e'
					moves.push_back(dir::se);
				}
				else
				{
					moves.push_back(dir::s);
				}
			}

			if (*input == ',')
			{
				input++; // skip ','
			}
		}

		auto move = [](vector<dir>& moves)
		{
			pair<int, int> pos{ 0, 0 };
			int dist = 0;
			int max_dist = dist;

			for (auto& d : moves)
			{
				switch (d)
				{
					case dir::n:
					{
						pos.second -= 2;
						break;
					}
					case dir::nw:
					{
						pos.first--;
						pos.second--;
						break;
					}
					case dir::ne:
					{
						pos.first++;
						pos.second--;
						break;
					}
					case dir::s:
					{
						pos.second += 2;
						break;
					}
					case dir::sw:
					{
						pos.first--;
						pos.second++;
						break;
					}
					case dir::se:
					{
						pos.first++;
						pos.second++;
						break;
					}
				}

				dist = abs(pos.first) + abs(pos.second);

				if (dist > max_dist)
				{
					max_dist = dist;
				}
			}

			return pair<int, int>{ dist / 2, max_dist / 2 };
		};

		pair<int, int> res = move(moves);

		// part 1
		part1 = res.first;

		// part 2
		part2 = res.second;

		return { part1, part2 };
	}
};
