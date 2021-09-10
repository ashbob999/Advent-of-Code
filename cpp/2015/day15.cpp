#include "../aocHelper.h"

class Day15 : public BaseDay
{
public:
	Day15() : BaseDay("15") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		/*struct info
		{
			int capacity;
			int durability;
			int flavour;
			int texture;
			int calories;
		};*/

		using info = array<int, 5>;

		vector<info> ingredients;

		// parse input
		while (*input != '\0')
		{
			// skip name
			while (*input != ' ')
			{
				input++;
			}

			info i;

			input += 10; //skip ' capacity '

			bool neg_cap = false;

			if (*input == '-')
			{
				neg_cap = true;
				input++;
			}
			i[0] = numericParse<int>(input);

			if (neg_cap)
			{
				i[0] *= -1;
			}

			input += 13; // skip ', durability '

			bool neg_dur = false;

			if (*input == '-')
			{
				neg_dur = true;
				input++;
			}
			i[1] = numericParse<int>(input);

			if (neg_dur)
			{
				i[1] *= -1;
			}

			input += 9; // skip ', flavor '

			bool neg_fla = false;

			if (*input == '-')
			{
				neg_fla = true;
				input++;
			}
			i[2] = numericParse<int>(input);

			if (neg_fla)
			{
				i[2] *= -1;
			}

			input += 10; // skip ', texture '

			bool neg_tex = false;

			if (*input == '-')
			{
				neg_tex = true;
				input++;
			}
			i[3] = numericParse<int>(input);

			if (neg_tex)
			{
				i[3] *= -1;
			}

			input += 11; // skip ', calories '

			bool neg_cal = false;

			if (*input == '-')
			{
				neg_cal = true;
				input++;
			}
			i[4] = numericParse<int>(input);

			if (neg_cal)
			{
				i[4] *= -1;
			}

			ingredients.push_back(i);

			input++; // skip \n
		}

		auto calc_value = [&ingredients](array<int, 4> amounts, int index)
		{
			int value = 0;
			for (int i = 0; i < 4; i++)
			{
				value += ingredients[i][index] * amounts[i];
			}

			return max(value, 0);
		};

		constexpr int limit = 100;

		// part 1
		int max_score = 0;

		array<int, 4> amounts = { 0, 0, 0, 0 };

		for (amounts[0] = 0; amounts[0] <= limit; amounts[0]++)
		{
			for (amounts[1] = 0; amounts[1] <= limit - amounts[0]; amounts[1]++)
			{
				for (amounts[2] = 0; amounts[2] <= limit - amounts[0] - amounts[1]; amounts[2]++)
				{
					amounts[3] = limit - amounts[0] - amounts[1] - amounts[2];

					int cap = calc_value(amounts, 0);
					int dur = calc_value(amounts, 1);
					int fla = calc_value(amounts, 2);
					int tex = calc_value(amounts, 3);

					int score = cap * dur * fla * tex;
					max_score = max(max_score, score);
				}
			}
		}

		part1 = max_score;

		// part 2
		max_score = 0;

		for (amounts[0] = 0; amounts[0] <= limit; amounts[0]++)
		{
			for (amounts[1] = 0; amounts[1] <= limit - amounts[0]; amounts[1]++)
			{
				for (amounts[2] = 0; amounts[2] <= limit - amounts[0] - amounts[1]; amounts[2]++)
				{
					amounts[3] = limit - amounts[0] - amounts[1] - amounts[2];

					int cal = calc_value(amounts, 4);

					if (cal == 500)
					{
						int cap = calc_value(amounts, 0);
						int dur = calc_value(amounts, 1);
						int fla = calc_value(amounts, 2);
						int tex = calc_value(amounts, 3);

						int score = cap * dur * fla * tex;
						max_score = max(max_score, score);
					}
				}
			}
		}

		part2 = max_score;

		return { part1, part2 };
	}
};
