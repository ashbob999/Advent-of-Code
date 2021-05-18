#include "../aocHelper.h"

enum class section_type : int
{
	value = 0,
	op = 1,
	section = 2
};

struct equation_section
{
	union
	{
		long long value;
		char op;
		deque<shared_ptr<equation_section>> eq_list;
	};
	section_type t;
	equation_section(long long val) : t(section_type::value), value(val) {}
	equation_section(char o) : t(section_type::op), op(o) {}
	equation_section(deque<shared_ptr<equation_section>>& eq) : t(section_type::section), eq_list(eq) {}
	equation_section() : t(section_type::section), eq_list() {}

	~equation_section()
	{}
};

class Day18 : public BaseDay
{
public:
	Day18() : BaseDay("18") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		using eq_ptr = shared_ptr<equation_section>;

		function<long long(deque<eq_ptr>&)> solve_part1;
		solve_part1 = [&solve_part1](deque<eq_ptr>& eq_og)
		{
			deque<eq_ptr> eq(eq_og);

			for (int i = 0; i < eq.size(); i++)
			{
				if (eq[i]->t == section_type::section)
				{
					eq[i] = make_shared<equation_section>(solve_part1(eq[i]->eq_list));
				}
			}

			while (eq.size() > 1)
			{
				if (eq[1]->op == '+') // do addition
				{
					long long val = eq[0]->value + eq[2]->value;
					eq.erase(eq.begin(), eq.begin() + 3);
					eq.push_front(make_shared<equation_section>(val));
				}
				else if (eq[1]->op == '*') // do multiplication
				{
					long long val = eq[0]->value * eq[2]->value;
					eq.erase(eq.begin(), eq.begin() + 3);
					eq.push_front(make_shared<equation_section>(val));
				}
			}

			return eq[0]->value;
		};

		function<long long(deque<eq_ptr>&)> solve_part2;
		solve_part2 = [&solve_part2](deque<eq_ptr>& eq_og)
		{
			deque<eq_ptr> eq(eq_og);

			for (int i = 0; i < eq.size(); i++)
			{
				if (eq[i]->t == section_type::section)
				{
					eq[i] = make_shared<equation_section>(solve_part2(eq[i]->eq_list));
				}
			}

			while (eq.size() > 1) // do addition
			{
				auto f = find_if(eq.begin(), eq.end(), [](const eq_ptr& e)
				{
					return e->op == '+' && e->t == section_type::op;
				});

				if (f != eq.end())
				{
					long long value = (*(f - 1))->value + (*(f + 1))->value;
					auto it = eq.erase(f - 1, f + 2);
					eq.insert(it, make_shared<equation_section>(value));
				}
				else
				{
					break;
				}
			}

			while (eq.size() > 1) // do multiplication
			{
				long long val = eq[0]->value * eq[2]->value;
				eq.erase(eq.begin(), eq.begin() + 3);
				eq.push_front(make_shared<equation_section>(val));
			}

			return eq[0]->value;
		};
		int i = 0;
		// parse input
		while (*input != '\0')
		{
			i++;
			// parse equation
			deque<eq_ptr> eq;
			int current_depth = 0;

			while (*input != '\n')
			{
				if (*input >= '0' && *input <= '9') // number
				{
					if (current_depth == 0)
					{
						eq.push_back(make_shared<equation_section>(numericParse<long long>(input)));
					}
					else if (current_depth == 1)
					{
						eq.back()->eq_list.push_back(make_shared<equation_section>(numericParse<long long>(input)));
					}
					else if (current_depth == 2)
					{
						eq.back()->eq_list.back()->eq_list.push_back(make_shared<equation_section>(numericParse<long long>(input)));
					}
					input--;
				}
				else if (*input == '+' || *input == '*') // operator
				{
					if (current_depth == 0)
					{
						eq.push_back(make_shared<equation_section>(*input));
					}
					else if (current_depth == 1)
					{
						eq.back()->eq_list.push_back(make_shared<equation_section>(*input));
					}
					else if (current_depth == 2)
					{
						eq.back()->eq_list.back()->eq_list.push_back(make_shared<equation_section>(*input));
					}
				}
				else if (*input == '(') // open bracket
				{
					if (current_depth == 0)
					{
						eq.push_back(make_shared<equation_section>());
					}
					else if (current_depth == 1)
					{
						eq.back()->eq_list.push_back(make_shared<equation_section>());
					}
					current_depth++;
				}
				else if (*input == ')') // close bracket
				{
					current_depth--;
				}
				input++;
			}

			long long value1 = solve_part1(eq);
			part1 += value1;

			long long value2 = solve_part2(eq);
			part2 += value2;

			input++;
		}

		return { part1, part2 };
	}
};
