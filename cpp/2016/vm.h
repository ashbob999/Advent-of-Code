#pragma once

#include <vector>
#include <utility>
#include <unordered_map>

#include "../aocHelper.h"

using namespace std;

class VM
{
public:
	enum class Opcode
	{
		NUL,
		INC,
		DEC,
		CPY,
		JNZ,
		TGL,
		MUL,
		OUT,
	};

	enum class Operand
	{
		Register,
		Number,
	};

	struct Instruction
	{
		Opcode opcode = Opcode::NUL;
		vector<pair<Operand, int>> values;
	};

public:
	unordered_map<char, long long> registers = {
		{ 'a', 0 },
		{ 'b', 0 },
		{ 'c', 0 },
		{ 'd', 0 },
	};

	vector<Instruction> instructions;
	vector<long long> out_values;

private:
	long long pc = 0;

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
				instr.values.emplace_back(Operand::Register, (int) *input);
				input++;
			}
			else if (*input == 'd') // dec
			{
				input += 4; // skip "dec "
				instr.opcode = Opcode::DEC;
				instr.values.emplace_back(Operand::Register, (int) *input);
				input++;
			}
			else if (*input == 'c') // cpy
			{
				input += 4; // skip "cpy "
				instr.opcode = Opcode::CPY;

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int) *input);
					input++; // skip char
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int>(input));
				}

				input++; // skip ' '

				instr.values.emplace_back(Operand::Register, (int) *input);
				input++; // skip char
			}
			else if (*input == 'j') // jnz
			{
				input += 4; // skip "jnz "
				instr.opcode = Opcode::JNZ;

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int) *input);
					input++;
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int>(input));
				}

				input++; // skip ' '

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int) *input);
					input++;
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int>(input));
				}
			}
			else if (*input == 't') // tgl
			{
				input += 4; // skip "tgl "
				instr.opcode = Opcode::TGL;

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int) *input);
					input++;
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int>(input));
				}
			}
			else if (*input == 'o') // out
			{
				input += 4; // skip "out "
				instr.opcode = Opcode::OUT;

				if (*input >= 'a' && *input <= 'z') // is reg
				{
					instr.values.emplace_back(Operand::Register, (int) *input);
					input++;
				}
				else // is number
				{
					instr.values.emplace_back(Operand::Number, numericParse<int>(input));
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
		vector<Instruction> copied_instructions{ this->instructions };

		while (pc < copied_instructions.size())
		{
			Instruction& instr = copied_instructions[pc];

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
							registers[(char) instr.values[1].second] = (long long) instr.values[0].second;
						}
					}
					pc++;
					break;
				}
				case Opcode::JNZ:
				{
					long long value = 0;
					if (instr.values[0].first == Operand::Register)
					{
						value = registers[(char) instr.values[0].second];
					}
					else
					{
						value = (long long) instr.values[0].second;
					}

					if (value != 0)
					{
						long long index = 0;
						if (instr.values[1].first == Operand::Register)
						{
							index = registers[(char) instr.values[1].second];
						}
						else
						{
							index = (long long) instr.values[1].second;
						}
						pc += index;
					}
					else
					{
						pc++;
					}
					break;
				}
				case Opcode::TGL:
				{
					long long index = 0;

					if (instr.values[0].first == Operand::Register)
					{
						index = registers[(char) instr.values[0].second];
					}
					else
					{
						index = (long long) instr.values[0].second;
					}

					if (pc + index >= 0 && pc + index < copied_instructions.size())
					{
						Instruction& target = copied_instructions[pc + index];

						if (target.values.size() == 1)
						{
							if (target.opcode == Opcode::INC)
							{
								target.opcode = Opcode::DEC;
							}
							else
							{
								target.opcode = Opcode::INC;
							}
						}
						else if (target.values.size() == 2)
						{
							if (target.opcode == Opcode::JNZ)
							{
								target.opcode = Opcode::CPY;
							}
							else
							{
								target.opcode = Opcode::JNZ;
							}
						}
					}

					pc++;
					break;
				}
				case Opcode::MUL:
				{
					long long b = 0;
					if (instr.values[1].first == Operand::Register)
					{
						b = registers[(char) instr.values[1].second];
					}
					else
					{
						b = (long long) instr.values[1].second;
					}

					long long c = 0;
					if (instr.values[2].first == Operand::Register)
					{
						c = registers[(char) instr.values[2].second];
					}
					else
					{
						c = (long long) instr.values[2].second;
					}

					long long res = b * c;

					registers[(char) instr.values[0].second] = res;

					pc++;
					break;
				}
				case Opcode::OUT:
				{
					if (instr.values[0].first == Operand::Register)
					{
						out_values.push_back(registers[(char) instr.values[2].second]);
					}
					else
					{
						out_values.push_back((long long) instr.values[2].second);
					}

					pc++;
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
