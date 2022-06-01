#include "../aocHelper.h"

class Day22 : public BaseDay
{
public:
	Day22() : BaseDay("22") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct node
		{
			uint64_t x = 0;
			uint64_t y = 0;
			int size = 0;
			int used = 0;
			int avail = 0;
			int percent = 0;
		};

		unordered_map<uint64_t, node> nodes;

		uint64_t max_x = 0;
		uint64_t max_y = 0;

		// parse input

		// skip first line
		while (*input != '\n')
		{
			input++;
		}
		input++;

		// skip second line
		while (*input != '\n')
		{
			input++;
		}
		input++;

		while (*input != '\0')
		{
			input += 16;// skip "/dev/grid/node-x"
			uint64_t x = numericParse<uint64_t>(input);
			input += 2; // skip "-y"
			uint64_t y = numericParse<uint64_t>(input);

			max_x = max(max_x, x);
			max_y = max(max_y, y);

			uint64_t pos = (x << 32) | (y & 0xffffffff);

			// skip all spaces
			while (*input == ' ')
			{
				input++;
			}

			int size = numericParse<int>(input);
			input += 1; // skip 'T'

			// skip all spaces
			while (*input == ' ')
			{
				input++;
			}

			int used = numericParse<int>(input);
			input += 1; // skip 'T'

			// skip all spaces
			while (*input == ' ')
			{
				input++;
			}

			int avail = numericParse<int>(input);
			input += 1; // skip 'T'

			// skip all spaces
			while (*input == ' ')
			{
				input++;
			}

			int percent = numericParse<int>(input);
			input += 1; // skip '%'


			nodes[pos] = { x, y, size, used, avail, percent };

			input++; // skip '\n'
		}

		// part 1
		for (auto& node1 : nodes)
		{
			for (auto& node2 : nodes)
			{
				if (node1.first != node2.first)
				{
					if (node1.second.used > 0 && node1.second.used <= node2.second.avail)
					{
						part1++;
					}
				}
			}
		}

		// part 2

		int width = max_x + 1;
		int height = max_y + 1;

		uint64_t start_pos = 0;
		node& start_node = nodes[start_pos];

		uint64_t target_pos = (max_x << 32) | (0 & 0xffffffff);

		// find zero location
		uint64_t zero_location = 0;
		for (auto& node : nodes)
		{
			if (node.second.used == 0)
			{
				zero_location = node.first;
				break;
			}
		}

		// make the grid
		char** grid = new char* [height];

		for (uint64_t y = 0; y < height; y++)
		{
			grid[y] = new char[width];
			for (uint64_t x = 0; x < width; x++)
			{
				uint64_t pos = (x << 32) | (y & 0xffffffff);
				if (pos == start_pos)
				{
					grid[y][x] = 'S';
				}
				else if (pos == target_pos)
				{
					grid[y][x] = 'T';
				}
				else if (pos == zero_location)
				{
					grid[y][x] = 'E';
				}
				else if (nodes[pos].used > start_node.size)
				{
					grid[y][x] = '#';
				}
				else
				{
					grid[y][x] = '.';
				}
			}
		}

		auto bfs = [&width, &height](uint64_t start, uint64_t end, char** grid, char wall, uint64_t ignore_pos)
		{
			deque<uint64_t> to_check;
			to_check.push_back(start);

			unordered_map<uint64_t, int> dists;
			dists[start] = 0;

			while (to_check.size() > 0)
			{
				uint64_t curr_pos = to_check.front();
				to_check.pop_front();
				int curr_dist = dists[curr_pos];

				vector<uint64_t> adj;

				uint64_t x_pos = curr_pos >> 32;
				uint64_t y_pos = curr_pos & 0xffffffff;

				for (int y = -1; y <= 1; y += 2)
				{
					if (y_pos + y >= 0 && y_pos + y < height)
					{
						uint64_t new_pos = ((uint64_t) x_pos << 32) | ((uint64_t) (y_pos + y) & 0xffffffff);
						if (grid[y_pos + y][x_pos] != wall && new_pos != ignore_pos)
						{
							adj.push_back(new_pos);
						}
					}
				}

				for (int x = -1; x <= 1; x += 2)
				{
					if (x_pos + x >= 0 && x_pos + x < width)
					{
						uint64_t new_pos = ((uint64_t) (x_pos + x) << 32) | ((uint64_t) y_pos & 0xffffffff);
						if (grid[y_pos][x_pos + x] != wall && new_pos != ignore_pos)
						{
							adj.push_back(new_pos);
						}
					}
				}

				for (auto& ad : adj)
				{
					if (ad == end)
					{
						return curr_dist + 1;
					}
					else
					{
						if (!dists.contains(ad) || curr_dist + 1 < dists[ad])
						{
							to_check.push_back(ad);
							dists[ad] = curr_dist + 1;
						}
					}
				}
			}

			return 0;
		};

		uint64_t curr_target_pos = target_pos;
		uint64_t curr_empty_pos = zero_location;

		while (curr_target_pos != start_pos)
		{
			uint64_t in_front = (((curr_target_pos >> 32) - 1) << 32) | (curr_target_pos & 0xffffffff);

			int curr_steps = bfs(curr_empty_pos, in_front, grid, '#', curr_target_pos);
			curr_steps++;
			part2 += curr_steps;

			curr_empty_pos = curr_target_pos;
			curr_target_pos = in_front;
		}

		// delete grid
		for (int y = 0; y < height; y++)
		{
			delete[] grid[y];
		}

		delete[] grid;

		return { part1, part2 };
	}
};
