#pragma once

#include <vector>
#include <utility>
#include <unordered_map>
#include <cstdint>

#include "../aocHelper.h"

using namespace std;

class VM
{
	enum class Opcode
	{
		NUL,
		INC,
		DEC,
		CPY,
		JNZ,
	};

	enum class Operand
	{
		Register,
		Number,
	};

	struct Instruction
	{
		Opcode opcode = Opcode::NUL;
		vector<pair<Operand, int8_t>> values;
	};

public:
	unordered_map<char, int> registers = {
		{ 'a', 0 },
		{ 'b', 0 },
		{ 'c', 0 },
		{ 'd', 0 },
	};

	vector<Instruction> instructions;

private:
	int pc = 0;

public:
	VM(char* input)
	{
		// parse instructions

		Instruction instr;

		while (*input != '\0')
		{
			if (*input == 'i') // inc
			{
				input += 4; // skip "inc "
				instr.opcode = Opcode::INC;
				instr.values.emplace_back(Operand::Register, (int8_t) *input);
				input++;
			}
			else if (*input == 'd') // dec
			{
				input += 4; // skip "dec "
				instr.opcode = Opcode::DEC;
				instr.values.emplace_back(Operand::Register, (int8_t) *input);
				input++;
			}
			else if (*input == 'c') // cpy
			{
				input += 4; // skip "cpy "
				instr.opcode = Opcode::CPY;

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int8_t) *input);
					input++; // skip char
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int8_t>(input));
				}

				input++; // skip ' '

				instr.values.emplace_back(Operand::Register, (int8_t) *input);
				input++; // skip char
			}
			else if (*input == 'j') // jnz
			{
				input += 4; // skip "jnz "
				instr.opcode = Opcode::JNZ;

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int8_t) *input);
					input++;
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int8_t>(input));
				}

				input++; // skip ' '

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int8_t) *input);
					input++;
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int8_t>(input));
				}
			}

			if (*input == '\n')
			{
				instructions.push_back(instr);
				instr = Instruction{};
				input++;
			}
		}
	}

	void run()
	{
		while (pc < instructions.size())
		{
			Instruction& instr = instructions[pc];

			switch (instr.opcode)
			{
				case Opcode::INC:
				{
					if (instr.values[0].first == Operand::Register)
					{
						registers[(char) instr.values[0].second]++;
					}
					pc++;
					break;
				}
				case Opcode::DEC:
				{
					if (instr.values[0].first == Operand::Register)
					{
						registers[(char) instr.values[0].second]--;
					}
					pc++;
					break;
				}
				case Opcode::CPY:
				{
					if (instr.values[1].first == Operand::Register)
					{
						if (instr.values[0].first == Operand::Register)
						{
							registers[(char) instr.values[1].second] = registers[(char) instr.values[0].second];
						}
						else
						{
							registers[(char) instr.values[1].second] = (int) instr.values[0].second;
						}
					}
					pc++;
					break;
				}
				case Opcode::JNZ:
				{
					int value = 0;
					if (instr.values[0].first == Operand::Register)
					{
						value = registers[(char) instr.values[0].second];
					}
					else
					{
						value = (int) instr.values[0].second;
					}

					if (value != 0)
					{
						int index = 0;
						if (instr.values[1].first == Operand::Register)
						{
							index = registers[(char) instr.values[1].second];
						}
						else
						{
							index = (int) instr.values[1].second;
						}
						pc += index;
					}
					else
					{
						pc++;
					}
					break;
				}
				default:
				{
					pc++;
					break;
				}
			}
		}
	}

	void reset()
	{
		for (auto& p : registers)
		{
			registers[p.first] = 0;
		}
		pc = 0;
	}
};
