#include "../aocHelper.h"

namespace
{
	struct GridSquare
	{
		char square{0};
		bool empty{false};
	};
}

class Day11 : public BaseDay
{
public:
	Day11() : BaseDay("11") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::vector<GridSquare>> grid{};
		grid.push_back({});

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				grid.push_back({});
			}
			else
			{
				grid.back().push_back({*input, false});
			}

			input++;
		}

		grid.pop_back();

		const int height = grid.size();
		const int width = grid[0].size();

		// process empty rows/columns
		for (uint8_t y = 0; y < height; y++)
		{
			bool empty = true;
			for (uint8_t x = 0; x < width; x++)
			{
				if (grid[y][x].square == '#')
				{
					empty = false;
					break;
				}
			}

			if (empty)
			{
				for (uint8_t x = 0; x < width; x++)
				{
					grid[y][x].empty = true;
				}
			}
		}

		for (uint8_t x = 0; x < width; x++)
		{
			bool empty = true;
			for (uint8_t y = 0; y < height; y++)
			{
				if (grid[y][x].square == '#')
				{
					empty = false;
					break;
				}
			}

			if (empty)
			{
				for (uint8_t y = 0; y < height; y++)
				{
					grid[y][x].empty = true;
				}
			}
		}

		std::vector<std::pair<uint8_t, uint8_t>> galaxies{};
		std::vector<bool> columns_with_galaxies{};
		columns_with_galaxies.resize(width, false);
		for (uint8_t y = 0; y < height; y++)
		{
			for (uint8_t x = 0; x < width; x++)
			{
				if (grid[y][x].square == '#')
				{
					galaxies.push_back({x, y});
					columns_with_galaxies[x] = true;
				}
			}
		}

		std::array<std::pair<uint8_t, uint8_t>, 256 * 256> distances{};
		distances[0] = {0, 0};

		for (uint8_t x = 1; x < width; x++)
		{
			auto&& prev = distances[(x - 1) << 8ul];
			std::pair<uint8_t, uint8_t> res = prev;
			if (grid[0][x - 1].empty)
			{
				res.second++;
			}
			else
			{
				res.first++;
			}

			distances[x << 8ul] = res;
		}

		for (int y = 1; y < height; y++)
		{
			for (int x = 0; x < width; x++)
			{
				if (columns_with_galaxies[x] == false)
				{
					continue;
				}
				auto&& prev = distances[x << 8 | (y - 1)];
				std::pair<uint8_t, uint8_t> res = prev;
				if (grid[y - 1][x].empty)
				{
					res.second++;
				}
				else
				{
					res.first++;
				}

				distances[x << 8 | y] = res;
			}
		}

		const auto count = [&distances](
							   const std::pair<uint8_t, uint8_t>& g1,
							   const std::pair<uint8_t, uint8_t>& g2) -> std::pair<uint8_t, uint8_t>
		{
			uint8_t x1 = g1.first;
			uint8_t y1 = g1.second;
			uint8_t x2 = g2.first;
			uint8_t y2 = g2.second;

			if (x2 < x1)
			{
				std::swap(x1, x2);
			}

			if (y2 < y1)
			{
				std::swap(y1, y2);
			}

			auto&& tl = distances[x1 << 8 | y1];
			auto&& br = distances[x2 << 8 | y2];

			return {br.first - tl.first, br.second - tl.second};
		};

		for (int i = 0; i < galaxies.size(); i++)
		{
			for (int j = i + 1; j < galaxies.size(); j++)
			{
				auto&& g1 = galaxies[i];
				auto&& g2 = galaxies[j];

				auto res = count(g1, g2);

				part1 += res.first + res.second * 2;
				part2 += res.first + res.second * 1'000'000;
			}
		}

		return {part1, part2};
	}
};
