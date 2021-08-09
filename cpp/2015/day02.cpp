#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

		auto surface_area = [](int l, int w, int h)
		{
			return 2 * ((l * w) + (w * h) + (h * l));
		};

		auto slack_area = [](int l, int w, int h)
		{
			return min(l, min(w, h));
		};

		auto ribbon_length = [](int l, int w, int h)
		{
			return 2 * min(l + w, min(w + h, l + h));
		};
		
		auto bow_length = [](int l, int w, int h)
		{
			return l * w * h;
		};

		while (*input != '\0')
		{
			int length = numericParse<int>(input);
			input += 2; // skip: x
			int width = numericParse<int>(input);
			input += 2; // skip: x
			int height = numericParse<int>(input);

			// part 1
			part1 += surface_area(length, width, height);
			part1 += slack_area(length, width, height);

			// part 2
			part2 += ribbon_length(length, width, height);
			part2 += bow_length(length, width, height);

			input += 2; //skip: \n
		}

		return { part1, part2 };
	}
};
