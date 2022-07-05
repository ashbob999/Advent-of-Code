#include "../aocHelper.h"

class Day08 : public BaseDay
{
public:
	Day08() : BaseDay("08") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		enum class value_type
		{
			reg,
			number,
		};

		enum class op_type
		{
			lt,
			gt,
			lte,
			gte,
			eq,
			ne,
		};

		struct instr
		{
			string reg;
			int diff = 0;
			value_type lhs_type;
			string lhs_s;
			int lhs_v;
			op_type op = op_type::eq;
			int rhs_v;
		};

		vector<instr> instructions;

		// parse input
		while (*input != '\0')
		{
			instr inst;

			while (*input != ' ')
			{
				inst.reg += *input;
				input++;
			}

			input++; // skip ' '

			if (*input == 'd')
			{
				inst.diff = -1;
				input += 3; // skip "dec"
			}
			else
			{
				inst.diff = 1;
				input += 3; // skip "inc"
			}

			input++; // skip ' '

			int value = numericParse<int>(input);
			inst.diff *= value;

			input += 4; // skip ' if '

			if (*input >= 'a' && *input <= 'z')
			{
				inst.lhs_type = value_type::reg;
				while (*input >= 'a' && *input <= 'z')
				{
					inst.lhs_s += *input;
					input++;
				}
			}
			else
			{
				inst.lhs_type = value_type::number;
				int value = numericParse<int>(input);
				inst.lhs_v = value;
			}

			input++; // skip ' '

			if (*input == '<')
			{
				input++; // skip '<'
				if (*input == '=')
				{
					inst.op = op_type::lte;
					input++; // skip '='
				}
				else
				{
					inst.op = op_type::lt;
				}
			}
			else if (*input == '>')
			{
				input++; // skip '>'
				if (*input == '=')
				{
					inst.op = op_type::gte;
					input++; // skip '='
				}
				else
				{
					inst.op = op_type::gt;
				}
			}
			else if (*input == '=')
			{
				inst.op = op_type::eq;
				input += 2; // skip "=="
			}
			else if (*input == '!')
			{
				inst.op = op_type::ne;
				input += 2; // skip "!="
			}

			input++; // skip ' '

			value = numericParse<int>(input);
			inst.rhs_v = value;

			instructions.push_back(inst);

			input++; // skip '\n'

			//cout << endl;
		}

		// part 1
		unordered_map<string, int> p1_regs;

		for (auto& inst : instructions)
		{
			if (!p1_regs.contains(inst.reg))
			{
				p1_regs[inst.reg] = 0;
			}

			int v1;

			if (inst.lhs_type == value_type::number)
			{
				v1 = inst.lhs_v;
			}
			else
			{
				if (p1_regs.contains(inst.lhs_s))
				{
					v1 = p1_regs[inst.lhs_s];
				}
				else
				{
					v1 = 0;
				}
			}

			int v2 = inst.rhs_v;

			bool cv;

			switch (inst.op)
			{
				case op_type::eq:
				{
					cv = v1 == v2;
					break;
				}
				case op_type::ne:
				{
					cv = v1 != v2;
					break;
				}
				case op_type::lt:
				{
					cv = v1 < v2;
					break;
				}
				case op_type::lte:
				{
					cv = v1 <= v2;
					break;
				}
				case op_type::gt:
				{
					cv = v1 > v2;
					break;
				}
				case op_type::gte:
				{
					cv = v1 >= v2;
					break;
				}
			}

			if (cv)
			{
				p1_regs[inst.reg] += inst.diff;
			}
		}

		part1 = max_element(p1_regs.begin(), p1_regs.end(), [](const pair<string, int>& a, const pair<string, int>& b)
		{
			return a.second < b.second;
		})->second;

		// part 2
		unordered_map<string, int> p2_regs;

		for (auto& inst : instructions)
		{
			if (!p2_regs.contains(inst.reg))
			{
				p2_regs[inst.reg] = 0;
			}

			int v1;

			if (inst.lhs_type == value_type::number)
			{
				v1 = inst.lhs_v;
			}
			else
			{
				if (p2_regs.contains(inst.lhs_s))
				{
					v1 = p2_regs[inst.lhs_s];
				}
				else
				{
					v1 = 0;
				}
			}

			int v2 = inst.rhs_v;

			bool cv;

			switch (inst.op)
			{
				case op_type::eq:
				{
					cv = v1 == v2;
					break;
				}
				case op_type::ne:
				{
					cv = v1 != v2;
					break;
				}
				case op_type::lt:
				{
					cv = v1 < v2;
					break;
				}
				case op_type::lte:
				{
					cv = v1 <= v2;
					break;
				}
				case op_type::gt:
				{
					cv = v1 > v2;
					break;
				}
				case op_type::gte:
				{
					cv = v1 >= v2;
					break;
				}
			}

			if (cv)
			{
				p2_regs[inst.reg] += inst.diff;

				if (p2_regs[inst.reg] > part2)
				{
					part2 = p2_regs[inst.reg];
				}
			}
		}

		return { part1, part2 };
	}
};
