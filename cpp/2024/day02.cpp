#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::vector<uint8_t>> levels{};

		// parse input
		while (*input != '\0')
		{
			std::vector<uint8_t> level{};
			level.reserve(10);

			level.push_back(numericParse<uint8_t>(input));

			while (*input != '\n' && *input != '\0')
			{
				input++; // skip ' '
				level.push_back(numericParse<uint8_t>(input));
			}

			levels.push_back(std::move(level));

			input++; // skip '\n'
		}

		const auto isSafe = [](const std::vector<uint8_t>& level) -> bool
		{
			bool increasing = true;

			for (size_t i = 0; i < level.size() - 1; i++)
			{
				auto& v1 = level[i];
				auto& v2 = level[i + 1];

				int8_t diff = static_cast<int8_t>(v2) - static_cast<int8_t>(v1);

				if (diff == 0 || std::abs(diff) > 3)
				{
					return false;
				}

				if (i == 0)
				{
					increasing = (diff > 0);
				}
				else
				{
					if (increasing && diff < 0)
					{
						return false;
					}
					else if (!increasing && diff > 0)
					{
						return false;
					}
				}
			}

			return true;
		};

		// part 1
		for (auto& level : levels)
		{
			if (isSafe(level))
			{
				part1++;
			}
		}

		// part 2
		for (auto& level : levels)
		{
			if (isSafe(level))
			{
				part2++;
			}
			else
			{
				for (size_t i = 0; i < level.size(); i++)
				{
					std::vector<uint8_t> newLevel = level;
					newLevel.erase(newLevel.begin() + i);
					if (isSafe(newLevel))
					{
						part2++;
						break;
					}
				}
			}
		}

		return {part1, part2};
	}
};
