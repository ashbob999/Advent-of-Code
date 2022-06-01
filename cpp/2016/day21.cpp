#include "../aocHelper.h"

class Day21 : public BaseDay
{
public:
	Day21() : BaseDay("21") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		string password = "abcdefgh";
		string scrambled_password = "fbgdceah";

		enum class instruction_type
		{
			none,
			swap_position,
			swap_letter,
			rotate_steps,
			rotate_letter,
			reverse_positions,
			move_positions,
		};

		struct Instruction
		{
			instruction_type type = instruction_type::none;
			vector<uint8_t> values;
		};

		vector<Instruction> instructions;

		// parse input
		while (*input != '\0')
		{
			if (*input == 's') // swap
			{
				input += 5; // skip "swap "
				if (*input == 'p') // swap position
				{
					input += 9; // skip "position "
					uint8_t pos_1 = numericParse<uint8_t>(input);
					input += 15; // skip " with position "
					uint8_t pos_2 = numericParse<uint8_t>(input);
					Instruction i;
					i.type = instruction_type::swap_position;
					i.values.push_back(pos_1);
					i.values.push_back(pos_2);
					instructions.push_back(i);
				}
				else // swap letter
				{
					input += 7; // skip "letter "
					uint8_t char_1 = *input;
					input++;
					input += 13; // skip " with letter "
					uint8_t char_2 = *input;
					input++;
					Instruction i;
					i.type = instruction_type::swap_letter;
					i.values.push_back(char_1);
					i.values.push_back(char_2);
					instructions.push_back(i);
				}
			}
			else if (*input == 'r')
			{
				input++; // skip 'r'
				if (*input == 'o') // rotate
				{
					input += 6; // skip "otate "
					if (*input == 'l') // rotate left steps
					{
						input += 5; // skip "left "
						uint8_t steps = (uint8_t) numericParse<int8_t>(input);
						input += 5; // skip " step"
						if (*input == 's')
						{
							input++; // skip 's'
						}
						Instruction i;
						i.type = instruction_type::rotate_steps;
						i.values.push_back(steps);
						i.values.push_back(0);
						instructions.push_back(i);
					}
					else if (*input == 'r') // rotate right steps
					{
						input += 6; // skip "right "
						uint8_t steps = (uint8_t) numericParse<int8_t>(input);
						input += 5; // skip " step"
						if (*input == 's')
						{
							input++; // skip 's'
						}
						Instruction i;
						i.type = instruction_type::rotate_steps;
						i.values.push_back(steps);
						i.values.push_back(1);
						instructions.push_back(i);
					}
					else // rotate letter
					{
						input += 28; // skip "based on position of letter "
						uint8_t char_1 = *input;
						input++;
						Instruction i;
						i.type = instruction_type::rotate_letter;
						i.values.push_back(char_1);
						instructions.push_back(i);
					}
				}
				else // reverse positions
				{
					input += 17; // skip "everse positions "
					uint8_t pos_1 = numericParse<uint8_t>(input);
					input += 9; // skip " through "
					uint8_t pos_2 = numericParse<uint8_t>(input);
					Instruction i;
					i.type = instruction_type::reverse_positions;
					i.values.push_back(pos_1);
					i.values.push_back(pos_2);
					instructions.push_back(i);
				}
			}
			else if (*input == 'm') // move positions
			{
				input += 14; // skip "move position "
				uint8_t pos_1 = numericParse<uint8_t>(input);
				input += 13; // skip " to position "
				uint8_t pos_2 = numericParse<uint8_t>(input);
				Instruction i;
				i.type = instruction_type::move_positions;
				i.values.push_back(pos_1);
				i.values.push_back(pos_2);
				instructions.push_back(i);
			}
			input++; // skip '\n'
		}

		auto swap_position = [](string& str, vector<uint8_t>& values)
		{
			char tmp = str[values[1]];
			str[values[1]] = str[values[0]];
			str[values[0]] = tmp;
		};

		auto swap_letter = [](string& str, vector<uint8_t>& values)
		{
			int index_1 = str.find(values[0]);
			int index_2 = str.find(values[1]);

			char tmp = str[index_2];
			str[index_2] = str[index_1];
			str[index_1] = tmp;
		};

		auto rotate_steps = [](string& str, vector<uint8_t>& values)
		{
			string s_tmp{ str };
			int diff = values[0] * (values[1] == 0 ? -1 : 1);

			for (int i = 0; i < str.length(); i++)
			{
				int new_index = (i + diff) % str.length();
				new_index += new_index < 0 ? str.length() : 0;
				s_tmp[new_index] = str[i];
			}

			str.swap(s_tmp);
		};

		auto rotate_letter = [](string& str, vector<uint8_t>& values)
		{
			int index = str.find(values[0]);

			string s_tmp{ str };
			int diff = index + 1 + (index >= 4 ? 1 : 0);

			for (int i = 0; i < str.length(); i++)
			{
				int new_index = (i + diff) % str.length();
				new_index += new_index < 0 ? str.length() : 0;
				s_tmp[new_index] = str[i];
			}

			str.swap(s_tmp);
		};

		auto reverse_positions = [](string& str, vector<uint8_t>& values)
		{
			int diff = (values[1] - values[0] + 1) / 2;

			for (int i = 0; i < diff; i++)
			{
				int index_1 = values[0] + i;
				int index_2 = values[1] - i;

				char tmp = str[index_2];
				str[index_2] = str[index_1];
				str[index_1] = tmp;
			}
		};

		auto move_positions = [](string& str, vector<uint8_t>& values)
		{
			char c = str[values[0]];
			str.erase(values[0], 1);
			str.insert(values[1], 1, c);
		};

		unordered_map<instruction_type, function<void(string&, vector<uint8_t>&)>> funcs = {
			{instruction_type::swap_position, swap_position},
			{instruction_type::swap_letter, swap_letter},
			{instruction_type::rotate_steps, rotate_steps},
			{instruction_type::rotate_letter, rotate_letter},
			{instruction_type::reverse_positions, reverse_positions},
			{instruction_type::move_positions, move_positions},
		};

		auto scramble = [&](string str, vector<Instruction>& instrs)
		{
			for (auto& instr : instrs)
			{
				funcs[instr.type](str, instr.values);
			}

			return str;
		};

		auto reverse_rotate_steps = [](string& str, vector<uint8_t>& values)
		{
			string s_tmp{ str };
			int diff = values[0] * -1 * (values[1] == 0 ? -1 : 1);

			for (int i = 0; i < str.length(); i++)
			{
				int new_index = (i + diff) % str.length();
				new_index += new_index < 0 ? str.length() : 0;
				s_tmp[new_index] = str[i];
			}

			str.swap(s_tmp);
		};

		auto reverse_rotate_letter = [](string& str, vector<uint8_t>& values)
		{
			int index = str.find(values[0]);

			/*	reverse rotate letter only works for length==8
				start index -> right shifts -> end index
				0 -> 1 -> 1
				1 -> 2 -> 3
				2 -> 3 -> 5
				3 -> 4 -> 7
				4 -> 6 -> 2
				5 -> 7 -> 4
				6 -> 8 -> 6
				7 -> 9 -> 0
				mapping[i] = shifts left
				mapping = {1: 1, 3: 2, 5: 3, 7: 4, 2: 6, 4: 7, 6: 8, 0: 9}
			*/

			unordered_map<int, int> mapping = {
				{1, 1},
				{3, 2},
				{5, 3},
				{7, 4},
				{2, 6},
				{4, 7},
				{6, 8},
				{0, 9},
			};

			string s_tmp{ str };
			int diff = -1 * mapping[index];

			for (int i = 0; i < str.length(); i++)
			{
				int new_index = (i + diff) % str.length();
				new_index += new_index < 0 ? str.length() : 0;
				s_tmp[new_index] = str[i];
			}

			str.swap(s_tmp);
		};

		auto reverse_move_positions = [](string& str, vector<uint8_t>& values)
		{
			char c = str[values[1]];
			str.erase(values[1], 1);
			str.insert(values[0], 1, c);
		};

		unordered_map<instruction_type, function<void(string&, vector<uint8_t>&)>> reverse_funcs = {
			{instruction_type::swap_position, swap_position},
			{instruction_type::swap_letter, swap_letter},
			{instruction_type::rotate_steps, reverse_rotate_steps},
			{instruction_type::rotate_letter, reverse_rotate_letter},
			{instruction_type::reverse_positions, reverse_positions},
			{instruction_type::move_positions, reverse_move_positions},
		};

		auto reverse_scramble = [&](string str, vector<Instruction>& instrs)
		{
			for (int i = instrs.size() - 1; i >= 0; i--)
			{
				auto& instr = instrs[i];
				reverse_funcs[instr.type](str, instr.values);
			}

			return str;
		};

		// part 1
		string p1_str = scramble(password, instructions);
		memcpy(this->stringResult.first, p1_str.c_str(), p1_str.length());

		// part 2
		string p2_str = reverse_scramble(scrambled_password, instructions);
		memcpy(this->stringResult.second, p2_str.c_str(), p2_str.length());

		return { part1, part2 };
	}
};
