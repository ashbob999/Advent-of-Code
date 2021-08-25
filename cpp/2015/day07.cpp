#include "../aocHelper.h"

class Day07 : public BaseDay
{
public:
	Day07() : BaseDay("07") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

		enum class op_type : int
		{
			NOT = 0,
			AND = 1,
			OR = 2,
			LSHIFT = 3,
			RSHIFT = 4,
			NUMBER = 5,
			SET = 6,
			NONE = 7
		};

		struct value
		{
			op_type type = op_type::NONE;
			string s1;
			string s2;
			uint16_t n;
		};

		unordered_map<string, value> circuit;

		// parse input
		while (*input != '\0')
		{
			vector<string> in_signal_parts;
			string out_signal;

			in_signal_parts.push_back("");

			while (*(input + 1) != '-')
			{
				if (*input == ' ')
				{
					in_signal_parts.push_back("");
				}
				else
				{
					in_signal_parts.back() += *input;
				}

				input++;
			}

			input += 4;

			while (*input != '\n')
			{
				out_signal += *input;
				input++;
			}

			value v;

			if (in_signal_parts.size() == 1 && in_signal_parts[0][0] >= '0' && in_signal_parts[0][0] <= '9') // number
			{
				v.type = op_type::NUMBER;

				char* cp = const_cast<char*>(in_signal_parts[0].c_str());

				v.n = numericParse<uint16_t>(cp);
			}
			else if (in_signal_parts.size() == 1) // set
			{
				v.type = op_type::SET;
				v.s1 = in_signal_parts[0];
			}
			else if (in_signal_parts[0][0] == 'N') // not
			{
				v.type = op_type::NOT;
				v.s1 = in_signal_parts[1];
			}
			else if (in_signal_parts[1][0] == 'A') // and
			{
				v.type = op_type::AND;
				v.s1 = in_signal_parts[0];
				v.s2 = in_signal_parts[2];
			}
			else if (in_signal_parts[1][0] == 'O') // or
			{
				v.type = op_type::OR;
				v.s1 = in_signal_parts[0];
				v.s2 = in_signal_parts[2];
			}
			else if (in_signal_parts[1][0] == 'L') // lshift
			{
				v.type = op_type::LSHIFT;
				v.s1 = in_signal_parts[0];

				char* cp = const_cast<char*>(in_signal_parts[2].c_str());

				v.n = numericParse<uint16_t>(cp);
			}
			else if (in_signal_parts[1][0] == 'R') // rshift
			{
				v.type = op_type::RSHIFT;
				v.s1 = in_signal_parts[0];

				char* cp = const_cast<char*>(in_signal_parts[2].c_str());

				v.n = numericParse<uint16_t>(cp);
			}

			circuit[out_signal] = v;

			input++; // skip \n
		}

		unordered_map<string, uint16_t> done_signals;

		for (auto it = circuit.cbegin(); it != circuit.cend();)
		{
			if (it->second.type == op_type::NUMBER)
			{
				done_signals[it->first] = it->second.n;
				it = circuit.erase(it);
			}
			else
			{
				it++;
			}
		}

		auto solve_circuit = [](unordered_map<string, value> circuit, unordered_map<string, uint16_t> done_signals)
		{
			while (circuit.size() > 0)
			{
				for (auto it = circuit.cbegin(); it != circuit.cend();)
				{
					auto& k = it->first;
					auto& v = it->second;
					bool increment = true;

					if (v.type == op_type::SET)
					{
						auto f = done_signals.find(v.s1);
						if (f != done_signals.end())
						{
							done_signals[k] = f->second;
							increment = false;
						}
					}
					else if (v.type == op_type::NOT || v.type == op_type::LSHIFT || v.type == op_type::RSHIFT)
					{
						auto f = done_signals.find(v.s1);
						if (f != done_signals.end())
						{
							uint16_t val;
							if (v.s1[0] >= '0' && v.s1[0] <= '9')
							{
								char* cp = const_cast<char*>(v.s1.c_str());

								val = numericParse<uint16_t>(cp);
							}
							else
							{
								val = f->second;
							}

							uint16_t signal;

							if (v.type == op_type::NOT)
							{
								signal = ~val;
							}
							else if (v.type == op_type::LSHIFT)
							{
								signal = val << v.n;
							}
							else if (v.type == op_type::RSHIFT)
							{
								signal = val >> v.n;
							}

							done_signals[k] = signal;
							increment = false;
						}
					}
					else if (v.type == op_type::AND || v.type == op_type::OR)
					{
						bool v1_numeric = v.s1[0] >= '0' && v.s1[0] <= '9';
						auto f1 = done_signals.find(v.s1);

						bool v2_numeric = v.s2[0] >= '0' && v.s2[0] <= '9';
						auto f2 = done_signals.find(v.s2);

						if ((v1_numeric || f1 != done_signals.end()) && (v2_numeric || f2 != done_signals.end()))
						{
							uint16_t val1, val2;

							if (f1 != done_signals.end())
							{
								val1 = f1->second;
							}
							else
							{
								char* cp = const_cast<char*>(v.s1.c_str());

								val1 = numericParse<uint16_t>(cp);
							}

							if (f2 != done_signals.end())
							{
								val2 = f2->second;
							}
							else
							{
								char* cp = const_cast<char*>(v.s2.c_str());

								val2 = numericParse<uint16_t>(cp);
							}

							uint16_t signal;

							if (v.type == op_type::AND)
							{
								signal = val1 & val2;
							}
							else if (v.type == op_type::OR)
							{
								signal = val1 | val2;
							}

							done_signals[k] = signal;
							increment = false;
						}
					}

					if (increment)
					{
						it++;
					}
					else
					{
						it = circuit.erase(it);
					}
				}
			}

			return done_signals["a"];
		};

		// part 1
		part1 = solve_circuit(circuit, done_signals);

		// part 2
		done_signals["b"] = part1;

		part2 = solve_circuit(circuit, done_signals);

		return { part1, part2 };
	}
};
