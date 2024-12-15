#include "../aocHelper.h"

class Day05 : public BaseDay
{
public:
	Day05() : BaseDay("05") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<uint64_t> seeds;

		// parse input

		input += 6; // skip 'seeds:'

		while (*input != '\n')
		{
			input++; // skip ' '
			uint64_t seed = numericParse<uint64_t>(input);
			seeds.push_back(seed);
		}

		input += 2; // skip '\n\n'

		std::vector<std::vector<std::array<uint64_t, 3>>> maps;

		while (*input != '\0')
		{
			// skip the name
			while (*input != '\n')
			{
				input++;
			}
			input++; // skip '\n'

			std::vector<std::array<uint64_t, 3>> map;

			while (*input != '\n' && *input != '\0')
			{
				// dst src len
				uint64_t v0 = numericParse<uint64_t>(input);
				input++; // skip ' '
				uint64_t v1 = numericParse<uint64_t>(input);
				input++; // skip ' '
				uint64_t v2 = numericParse<uint64_t>(input);
				input++; // skip '\n'

				map.push_back({v0, v1, v2});
			}

			maps.push_back(std::move(map));

			if (*input == '\n')
			{
				input += 1; // skip '\n'
			}
		}

		// part 1
		std::vector<uint64_t> current_numbers = seeds;
		for (auto&& map : maps)
		{
			for (int i = 0; i < current_numbers.size(); i++)
			{
				auto&& number = current_numbers[i];

				for (auto&& range : map)
				{
					if (number >= range[1] && number < range[1] + range[2])
					{
						uint64_t dest = range[0] + (number - range[1]);
						current_numbers[i] = dest;
						break;
					}
				}
			}
		}

		part1 = *std::min_element(current_numbers.begin(), current_numbers.end());

		// part 2

		using Range = std::array<uint64_t, 2>;
		const auto check_range =
			[](const Range& r1,
			   Range r2) -> std::pair<std::optional<Range>, std::pair<std::optional<Range>, std::optional<Range>>>
		{
			std::pair<std::optional<Range>, std::pair<std::optional<Range>, std::optional<Range>>> result{};

			// check no overlap
			if (r2[1] <= r1[0] || r2[0] >= r1[1])
			{
				return result;
			}

			// check left
			if (r2[0] < r1[0])
			{
				Range overlap{r2[0], r1[0]};
				result.second.first = std::move(overlap);
				r2[0] = r1[0];
			}

			// check right
			if (r2[1] > r1[1])
			{
				Range overlap{r1[1], r2[1]};
				result.second.second = std::move(overlap);
				r2[1] = r1[1];
			}

			// check centre
			if (r2[0] >= r1[0] && r2[1] <= r1[1])
			{
				result.first = r2;
			}

			return result;
		};

		// Range(left=inclusive, right=exclusive)
		std::vector<Range> number_ranges;
		for (int i = 0; i < seeds.size(); i += 2)
		{
			number_ranges.push_back({seeds[i], seeds[i] + seeds[i + 1]});
		}

		for (auto&& map : maps)
		{
			std::vector<Range> new_number_ranges;
			new_number_ranges.reserve(number_ranges.size());

			for (int i = 0; i < number_ranges.size(); i++)
			{
				auto&& number_range = number_ranges[i];

				bool match = false;

				for (auto&& range : map)
				{
					Range proper_range{range[1], range[1] + range[2]};
					auto res = check_range(proper_range, number_range);

					if (res.first.has_value())
					{
						match = true;

						if (res.second.first.has_value())
						{
							number_ranges.push_back(*res.second.first);
						}
						if (res.second.second.has_value())
						{
							number_ranges.push_back(*res.second.second);
						}

						auto&& overlap = *res.first;

						uint64_t left = range[0] + overlap[0] - range[1];
						uint64_t len = overlap[1] - overlap[0];
						new_number_ranges.push_back({left, left + len});

						break;
					}
				}

				if (!match)
				{
					new_number_ranges.push_back(number_range);
				}
			}

			number_ranges = new_number_ranges;
		}

		part2 = std::min_element(
					number_ranges.begin(),
					number_ranges.end(),
					[](const auto& a, const auto& b) { return a[0] < b[0]; })
					->at(0);

		return {part1, part2};
	}
};
