#include "../aocHelper.h"

class Day03 : public BaseDay
{
public:
	Day03() : BaseDay("03") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::string_view inputStr(input, this->input_length);

		auto isMul = [](std::string_view str, size_t index) -> std::tuple<bool, size_t, uint16_t, uint16_t>
		{
			size_t startIndex = index;

			if (index + 8 > str.size())
			{
				return {false, 0, 0, 0};
			}

			// not matching 'mul('
			if (str[index] != 'm' || str[index + 1] != 'u' || str[index + 2] != 'l' || str[index + 3] != '(')
			{
				return {false, 0, 0, 0};
			}

			// not digit
			if (str[index + 4] < '0' || str[index + 4] > '9')
			{
				return {false, 0, 0, 0};
			}

			const char* ptr = str.data() + index + 4;
			uint16_t num1 = numericParse<uint16_t>(ptr);

			if (ptr >= str.data() + str.size())
			{
				return {false, 0, 0, 0};
			}

			if (*ptr != ',')
			{
				return {false, 0, 0, 0};
			}

			ptr++; // skip ','
			uint16_t num2 = numericParse<uint16_t>(ptr);

			if (ptr >= str.data() + str.size())
			{
				return {false, 0, 0, 0};
			}

			if (*ptr != ')')
			{
				return {false, 0, 0, 0};
			}

			return {true, std::distance(str.data(), ptr) - index + 1, num1, num2};
		};

		// part 1

		for (size_t i = 0; i < inputStr.size(); i++)
		{
			auto res = isMul(inputStr, i);
			if (std::get<0>(res))
			{
				part1 += std::get<2>(res) * std::get<3>(res);
				i += std::get<1>(res) - 1;
			}
		}

		// part 2
		for (size_t i = 0; i < inputStr.size(); i++)
		{
			auto res = isMul(inputStr, i);
			if (std::get<0>(res))
			{
				part1 += std::get<2>(res) * std::get<3>(res);
				i += std::get<1>(res) - 1;
			}
		}

		for (size_t i = 0; i < inputStr.size(); i++)
		{
			auto res = isMul(inputStr, i);
			if (std::get<0>(res))
			{
				part2 += std::get<2>(res) * std::get<3>(res);
				i += std::get<1>(res) - 1;
			}
			else
			{
				if (inputStr.substr(i).starts_with("don't()"))
				{
					i += 7 - 1;

					size_t nextDoIndex = inputStr.find("do()", i + 1);
					if (nextDoIndex == std::string_view::npos)
					{
						break;
					}
					else
					{
						i = nextDoIndex + 4 - 1;
					}
				}
			}
		}

		return {part1, part2};
	}
};
