#include "../aocHelper.h"

class Day16 : public BaseDay
{
public:
	Day16() : BaseDay("16") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		enum class move_type
		{
			spin,
			exchange,
			partner,
		};

		struct move
		{
			move_type type;
			int a;
			int b;
		};

		vector<move> moves;

		// parse input
		while (*input != '\n')
		{
			if (*input == 's') // spin
			{
				input++; // skip 's'

				int a = numericParse<int>(input);

				moves.push_back({ move_type::spin, a, 0 });
			}
			else if (*input == 'x') // exchange
			{
				input++; // skip 'x'

				int a = numericParse<int>(input);
				input++;
				int b = numericParse<int>(input);

				moves.push_back({ move_type::exchange, a, b });
			}
			else if (*input == 'p') // partner
			{
				input++; // skip 'p'

				int a = *input - 'a';
				input += 2;
				int b = *input - 'a';
				input++;

				moves.push_back({ move_type::partner, a, b });
			}

			if (*input == ',')
			{
				input++; // skip ','
			}
		}

		auto dance = [](array<int, 16>& programs, vector<move>& moves)
		{
			for (auto& m : moves)
			{
				switch (m.type)
				{
					case move_type::spin:
					{
						array<int, 16> tmp_programs;
						for (int i = 0; i < 16; i++)
						{
							tmp_programs[(i + m.a) % 16] = programs[i];
						}

						copy(tmp_programs.begin(), tmp_programs.end(), programs.begin());

						break;
					}
					case move_type::exchange:
					{
						int temp = programs[m.a];
						programs[m.a] = programs[m.b];
						programs[m.b] = temp;

						break;
					}
					case move_type::partner:
					{
						int i1 = 0;
						for (int i = 0; i < 16; i++)
						{
							if (programs[i] == m.a)
							{
								i1 = i;
								break;
							}
						}

						int i2 = 0;
						for (int i = 0; i < 16; i++)
						{
							if (programs[i] == m.b)
							{
								i2 = i;
								break;
							}
						}

						int temp = programs[i1];
						programs[i1] = programs[i2];
						programs[i2] = temp;

						break;
					}
				}
			}
		};

		array<int, 16> programs;
		for (int i = 0; i < 16; i++)
		{
			programs[i] = i;
		}

		// part 1
		array<int, 16> p1_programs;
		copy(programs.begin(), programs.end(), p1_programs.begin());

		dance(p1_programs, moves);

		for (int i = 0; i < 16; i++)
		{
			stringResult.first[i] = (char) (p1_programs[i] + 'a');
		}

		// part 2
		array<int, 16> p2_programs;
		copy(programs.begin(), programs.end(), p2_programs.begin());

		int reset_i = 1;

		for (int i = 0; i < 1'000'000'000; i++)
		{
			dance(p2_programs, moves);

			if (p2_programs == programs)
			{
				reset_i = i + 1;
				break;
			}
		}

		int steps_after_start = 1'000'000'000 % reset_i;

		for (int i = 0; i < steps_after_start; i++)
		{
			dance(p2_programs, moves);
		}

		for (int i = 0; i < 16; i++)
		{
			stringResult.second[i] = (char) (p2_programs[i] + 'a');
		}

		return { part1, part2 };
	}
};
