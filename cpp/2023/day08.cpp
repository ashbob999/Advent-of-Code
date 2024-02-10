#include "../aocHelper.h"

#include <algorithm>
#include <numeric>

class Day08 : public BaseDay
{
public:
	Day08() : BaseDay("08") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		int i = 0;
		while (*input != '\n')
		{
			i++;
			input++;
		}

		std::string_view directions{this->input_data.get(), input};

		input += 2; // skip '\n\n'

		constexpr int Dim1 = 32;
		constexpr int Dim2 = 26;
		constexpr int Dim3 = 26;
		std::array<std::pair<uint32_t, uint32_t>, Dim1 * Dim2 * Dim3> nodes{};

		const auto get_index = [](uint8_t i, uint8_t j, uint8_t k) -> uint32_t
		{ return i * Dim1 * Dim2 + j * Dim1 + k; };

		const auto readIndex = [&get_index](char*& data) -> uint32_t
		{
			uint8_t i = *(data + 0) - 'A';
			uint8_t j = *(data + 1) - 'A';
			uint8_t k = *(data + 2) - 'A';
			data += 3;

			return get_index(i, j, k);
		};

		std::vector<uint32_t> p2_startNodes{};

		while (*input != '\0')
		{
			uint32_t node = readIndex(input);
			input += 4; // skip ' = ('

			uint32_t left = readIndex(input);
			input += 2; // skip ', '

			uint32_t right = readIndex(input);
			input++; // skip ')'

			input++; // skip '\n'

			nodes[node] = {left, right};

			if (node % Dim1 == 0)
			{
				p2_startNodes.push_back(node);
			}
		}

		constexpr uint32_t StartNode = 0;
		constexpr uint32_t EndNode = get_index(25, 25, 25);

		// part 1
		uint32_t currNode = StartNode;
		int p1_index = 0;
		while (currNode != EndNode)
		{
			if (directions[p1_index] == 'L')
			{
				currNode = nodes[currNode].first;
			}
			else
			{
				currNode = nodes[currNode].second;
			}

			p1_index++;
			if (p1_index >= directions.size())
			{
				p1_index = 0;
			}
			part1++;
		}

		// part 2

		// find cycles between **A nodes and **Z nodes
		// the puzzle is nice, so we can assume any cycle length and start offset are the same
		std::vector<long long> cycleLengths{};
		cycleLengths.reserve(p2_startNodes.size());

		for (auto& startNode : p2_startNodes)
		{
			uint32_t currNode = startNode;
			int index = 0;
			int steps = 0;

			while (currNode % Dim1 != 25)
			{
				if (directions[index] == 'L')
				{
					currNode = nodes[currNode].first;
				}
				else
				{
					currNode = nodes[currNode].second;
				}

				index++;
				if (index >= directions.size())
				{
					index = 0;
				}
				steps++;
			}

			cycleLengths.push_back(steps);
		}

		part2 = std::accumulate(
			cycleLengths.begin() + 1,
			cycleLengths.end(),
			cycleLengths.front(),
			[](const auto& curr, const auto& v) { return std::lcm(curr, v); });

		return {part1, part2};
	}
};
