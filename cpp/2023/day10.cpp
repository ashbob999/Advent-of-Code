#include "../aocHelper.h"

#include <cassert>

class Day10 : public BaseDay
{
public:
	Day10() : BaseDay("10") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::string_view> grid{};

		const char* lineStart = input;

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				grid.push_back({lineStart, input});
				input++;
				lineStart = input;
			}
			else
			{
				input++;
			}
		}

		const int height = grid.size();
		const int width = grid[0].size();

		const auto find_start = [&grid, &width, &height]() -> uint16_t
		{
			for (int y = 0; y < height; y++)
			{
				for (int x = 0; x < width; x++)
				{
					if (grid[y][x] == 'S')
					{
						return x << 8 | y;
					}
				}
			}
			return 0;
		};

		const uint16_t start = find_start();

		const auto get_delta = [](char c) -> std::pair<std::pair<int, int>, std::pair<int, int>>
		{
			switch (c)
			{
				case '|':
				{
					return {{0, -1}, {0, 1}};
				}
				case '-':
				{
					return {{-1, 0}, {1, 0}};
				}
				case 'L':
				{
					return {{0, -1}, {1, 0}};
				}
				case 'J':
				{
					return {{0, -1}, {-1, 0}};
				}
				case '7':
				{
					return {{-1, 0}, {0, 1}};
				}
				case 'F':
				{
					return {{1, 0}, {0, 1}};
				}
				default:
				{
					return {};
				}
			}
		};

		const auto next_pos = [&grid, &get_delta](uint16_t curr, uint16_t prev) -> uint16_t
		{
			int cx = curr >> 8;
			int cy = curr & 0xFF;

			int px = prev >> 8;
			int py = prev & 0xFF;

			int dx = px - cx;
			int dy = py - cy;

			char curr_pos = grid[cy][cx];

			std::pair<int, int> current_delta{dx, dy};

			auto deltas = get_delta(curr_pos);

			std::pair<int, int> other_delta = (deltas.first == current_delta) ? deltas.second : deltas.first;

			int nx = cx + other_delta.first;
			int ny = cy + other_delta.second;
			return nx << 8 | ny;
		};

		const auto apply_adj = [](uint16_t pos, const std::pair<int, int>& adj) -> uint16_t
		{
			int x = (pos >> 8) + adj.first;
			int y = (pos & 0xFF) + adj.second;
			if (x < 0 || y < 0)
			{
				assert(false && __FUNCTION__ ": result is negative");
			}
			return x << 8 | y;
		};

		// part 1

		std::vector<uint16_t> loop{};

		loop.push_back(start);

		{
			uint16_t pos = start;

			int cx = pos >> 8;
			int cy = pos & 0xFF;

			char up = grid[cy - 1][cx];
			char down = grid[cy + 1][cx];
			char left = grid[cy][cx - 1];
			char right = grid[cy][cx + 1];

			if (up == '|' || up == '7' || up == 'F')
			{
				cy--;
			}
			else if (down == '|' || down == 'L' || down == 'J')
			{
				cy++;
			}
			else if (left == '-' || left == 'L' || left == 'F')
			{
				cx--;
			}
			else if (right == '-' || right == 'J' || right == '7')
			{
				cx++;
			}
			else
			{
				assert(false && "No start");
			}

			pos = cx << 8 | cy;

			loop.push_back(pos);

			while (pos != start)
			{
				pos = next_pos(loop[loop.size() - 1], loop[loop.size() - 2]);
				loop.push_back(pos);
			}

			assert(loop.size() % 2 == 1 && "Loop size should be even");
			part1 = loop.size() / 2;
		}

		// part 2

		std::unordered_set<uint16_t> loop_set{loop.begin(), loop.end()};

		const auto bfs = [&grid, &width, &height, &loop_set](uint16_t start) -> std::unordered_set<uint16_t>
		{
			std::deque<uint16_t> to_check{};
			to_check.push_back(start);
			std::unordered_set<uint16_t> seen{};
			seen.insert(start);

			while (!to_check.empty())
			{
				uint16_t curr = to_check.front();
				to_check.pop_front();

				static constexpr std::array<std::pair<int, int>, 4> adj_values{{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}};

				int cx = curr >> 8;
				int cy = curr & 0xFF;

				for (auto adj : adj_values)
				{
					int nx = cx + adj.first;
					int ny = cy + adj.second;
					if (nx >= 0 && nx < width && ny >= 0 && ny < height)
					{
						uint16_t next_pos = nx << 8 | ny;
						if (!loop_set.contains(next_pos))
						{
							if (!seen.contains(next_pos))
							{
								seen.insert(next_pos);
								to_check.push_back(next_pos);
							}
						}
					}
				}
			}

			return seen;
		};

		const auto is_point_in_path = [](uint16_t pos, const std::vector<uint16_t>& poly) -> bool
		{
			// https://en.m.wikipedia.org/wiki/Even%E2%80%93odd_rule
			int size = poly.size();
			int j = size - 1;
			bool c = false;

			int x = pos >> 8;
			int y = pos & 0xFF;

			for (int i = 0; i < size; i++)
			{
				int ix = poly[i] >> 8;
				int iy = poly[i] & 0xFF;
				int jx = poly[j] >> 8;
				int jy = poly[j] & 0xFF;

				if (x == ix && y == iy)
				{
					// point is in corner
					return true;
				}

				if ((iy > y) != (jy > y))
				{
					int slope = (x - ix) * (jy - iy) - (jx - ix) * (y - iy);

					if (slope == 0)
					{
						// point is on boundary
						return true;
					}
					if ((slope < 0) != (jy < iy))
					{
						c = !c;
					}
				}

				j = i;
			}

			return c;
		};

		const auto check_group =
			[&width, &height, &is_point_in_path, &loop](const std::unordered_set<uint16_t>& group) -> bool
		{
			// check touching edges

			for (auto& pos : group)
			{
				int x = pos >> 8;
				int y = pos & 0xFF;
				if (x == 0 || x == width - 1)
				{
					return false;
				}
				if (y == 0 || y == height - 1)
				{
					return false;
				}
			}

			// group is now surrounded by loop

			uint16_t test_pos = *group.begin();

			return is_point_in_path(test_pos, loop);
		};

		{
			std::unordered_set<uint16_t> seen{};

			for (int y = 0; y < height; y++)
			{
				for (int x = 0; x < width; x++)
				{
					uint16_t pos = x << 8 | y;
					if (!seen.contains(pos) && !loop_set.contains(pos))
					{
						auto group = bfs(pos);
						seen.insert(group.begin(), group.end());

						if (check_group(group))
						{
							part2 += group.size();
						}
					}
				}
			}
		}

		return {part1, part2};
	}
};
