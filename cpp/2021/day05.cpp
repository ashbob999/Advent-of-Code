#include "../aocHelper.h"

class Day05 : public BaseDay
{
public:
	Day05() : BaseDay("05") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct line
		{
			uint32_t x1;
			uint32_t x2;
			uint32_t y1;
			uint32_t y2;
		};

		vector<line> lines;

		while (*input != '\0')
		{
			line li;

			uint32_t x1 = numericParse<uint32_t>(input);
			input++; // skip ','
			uint32_t y1 = numericParse<uint32_t>(input);
			input += 4; // skip ' -> '
			uint32_t x2 = numericParse<uint32_t>(input);
			input++; // skip ','
			uint32_t y2 = numericParse<uint32_t>(input);

			lines.push_back({ x1, x2, y1, y2 });

			input++; // skip '\n'
		}

		// part 1
		unordered_map<uint64_t, int> p1_points;

		for (auto& li : lines)
		{
			uint32_t x1 = min(li.x1, li.x2);
			uint32_t x2 = max(li.x1, li.x2);
			uint32_t y1 = min(li.y1, li.y2);
			uint32_t y2 = max(li.y1, li.y2);

			if (x1 == x2)
			{
				for (uint32_t y = y1; y <= y2; y++)
				{
					uint64_t point = ((uint64_t) x1 << 32) | y;
					if (p1_points.contains(point))
					{
						p1_points[point]++;
					}
					else
					{
						p1_points[point] = 1;
					}
				}
			}
			else if (y1 == y2)
			{
				for (uint32_t x = x1; x <= x2; x++)
				{
					uint64_t point = ((uint64_t) x << 32) | y1;
					if (p1_points.contains(point))
					{
						p1_points[point]++;
					}
					else
					{
						p1_points[point] = 1;
					}
				}
			}
			else
			{
				continue;
			}
		}

		for (auto& p : p1_points)
		{
			if (p.second >= 2)
			{
				part1++;
			}
		}

		// part 2
		unordered_map<uint64_t, int> p2_points;

		for (auto& li : lines)
		{
			uint32_t x1 = min(li.x1, li.x2);
			uint32_t x2 = max(li.x1, li.x2);
			uint32_t y1 = min(li.y1, li.y2);
			uint32_t y2 = max(li.y1, li.y2);

			if (x1 == x2)
			{
				for (uint32_t y = y1; y <= y2; y++)
				{
					uint64_t point = ((uint64_t) x1 << 32) | y;
					if (p2_points.contains(point))
					{
						p2_points[point]++;
					}
					else
					{
						p2_points[point] = 1;
					}
				}
			}
			else if (y1 == y2)
			{
				for (uint32_t x = x1; x <= x2; x++)
				{
					uint64_t point = ((uint64_t) x << 32) | y1;
					if (p2_points.contains(point))
					{
						p2_points[point]++;
					}
					else
					{
						p2_points[point] = 1;
					}
				}
			}
			else
			{
				int dx = (li.x2 > li.x1) ? 1 : -1;
				int dy = (li.y2 > li.y1) ? 1 : -1;

				for (int step = 0; step <= abs((int) li.x2 - (int) li.x1); step++)
				{
					uint32_t x = li.x1 + dx * step;
					uint32_t y = li.y1 + dy * step;
					uint64_t point = ((uint64_t) x << 32) | y;

					if (p2_points.contains(point))
					{
						p2_points[point]++;
					}
					else
					{
						p2_points[point] = 1;
					}
				}
			}
		}

		for (auto& p : p2_points)
		{
			if (p.second >= 2)
			{
				part2++;
			}
		}

		return { part1, part2 };
	}
};
