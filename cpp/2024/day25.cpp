#include "../aocHelper.h"

class Day25 : public BaseDay
{
public:
	Day25() : BaseDay("25") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr size_t Width = 5;
		constexpr size_t Height = 7;

		std::vector<std::array<int, Width>> locks{};
		std::vector<std::array<int, Width>> keys{};

		// parse input
		while (*input != '\0')
		{
			bool isKey = false;
			std::array<int, Width> heights{};
			bool first = true;

			while (*input != '\n' && *input != '\0')
			{
				for (size_t i = 0; i < Width; i++)
				{
					if (*(input + i) == '#')
					{
						heights[i]++;
					}
				}

				if (first)
				{
					if (std::memchr(input, '.', Width) == nullptr)
					{
						isKey = true;
					}
					first = false;
				}

				input += Width;
				input++; // skip '\n'
			}

			if (isKey)
			{
				keys.push_back(heights);
			}
			else
			{
				locks.push_back(heights);
			}

			input++; // skip '\n'
		}

		// part 1

		for (auto& lock : locks)
		{
			for (auto& key : keys)
			{
				bool fits = true;

				for (size_t i = 0; i < Width; i++)
				{
					if (lock[i] + key[i] > Height)
					{
						fits = false;
						break;
					}
				}

				if (fits)
				{
					part1++;
				}
			}
		}

		return {part1, part2};
	}
};
