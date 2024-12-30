#include "../aocHelper.h"

class Day05 : public BaseDay
{
public:
	Day05() : BaseDay("05") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::pair<uint8_t, uint8_t>> rules{};
		std::vector<std::vector<uint8_t>> orders{};

		// parse input
		while (*input != '\n')
		{
			uint8_t r1 = numericParse<uint8_t>(input);
			input++; // skip '|'
			uint8_t r2 = numericParse<uint8_t>(input);

			rules.emplace_back(r1, r2);

			input++; // skip '\n'
		}

		input++; // skip '\n'

		while (*input != '\0')
		{
			std::vector<uint8_t> order{};
			order.reserve(30);

			order.push_back(numericParse<uint8_t>(input));

			while (*input != '\n' && *input != '\0')
			{
				input++; // skip ','
				order.push_back(numericParse<uint8_t>(input));
			}

			orders.push_back(std::move(order));

			input++; // skip '\n'
		}

		const auto checkOrder = [&rules](const std::vector<uint8_t>& order) -> bool
		{
			for (size_t i = 0; i < order.size(); i++)
			{
				uint8_t value = order[i];

				for (auto& rule : rules)
				{
					if (rule.second == value)
					{
						auto it = std::find(order.begin(), order.end(), rule.first);
						if (it != order.end())
						{
							if (std::distance(order.begin(), it) >= i)
							{
								return false;
							}
						}
					}
				}
			}

			return true;
		};

		// parse 1
		for (auto& order : orders)
		{
			if (checkOrder(order))
			{
				part1 += order[order.size() / 2];
			}
		}

		// part 2
		const auto fixOrder = [&rules, &checkOrder](const std::vector<uint8_t>& order) -> std::vector<uint8_t>
		{
			std::vector<uint8_t> newOrder{};
			newOrder.reserve(order.size());

			std::vector<int8_t> scratch{};
			scratch.reserve(order.size());

			for (auto& v : order)
			{
				scratch.clear();
				for (auto& rule : rules)
				{
					if (std::find(order.begin(), order.end(), rule.first) != order.end() &&
						std::find(order.begin(), order.end(), rule.second) != order.end())
					{
						if (rule.second == v)
						{
							auto it = std::find(newOrder.begin(), newOrder.end(), rule.first);
							if (it != newOrder.end())
							{
								scratch.push_back(std::distance(newOrder.begin(), it));
							}
						}
					}
				}

				int8_t index = scratch.empty() ? -1 : *std::max_element(scratch.begin(), scratch.end());
				index++;
				newOrder.insert(newOrder.begin() + index, v);
			}

			return newOrder;
		};

		for (auto& order : orders)
		{
			if (!checkOrder(order))
			{
				auto newOrder = fixOrder(order);
				part2 += newOrder[newOrder.size() / 2];
			}
		}

		return {part1, part2};
	}
};
