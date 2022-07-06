#include "../aocHelper.h"

class Day25 : public BaseDay
{
public:
	Day25() : BaseDay("25") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct data
		{
			int value;
			int dir;
			int next;
		};

		using state = array<data, 2>;

		//unordered_map<char, state> states;
		array<state, 6> states;

		input += 15; // skip "Begin in state "
		int start_state = *input - 'A';
		input++;
		input += 2; // skip ".\n"
		input += 36; // skip "Perform a diagnostic checksum after "
		int steps = numericParse<int>(input);
		input += 8; // skip " steps.\n"

		// parse input
		while (*input != '\0')
		{
			state st;

			input++; // skip '\n'
			input += 9; // skip "In state "
			char c = *input;
			input++;
			input += 2; // skip ":\n"
			input += 29; // skip "  If the current value is 0:\n"
			input += 22; // skip "    - Write the value "
			st[0].value = numericParse<int>(input);
			input += 2; // skip ".\n"
			input += 27; // skip "    - Move one slot to the "
			if (*input == 'r')
			{
				st[0].dir = 1;
				input += 5; // skip "right"
			}
			else
			{
				st[0].dir = -1;
				input += 4; // skip "left"
			}
			input += 2; // skip ".\n"
			input += 26; // skip "    - Continue with state "
			st[0].next = *input - 'A';
			input++;
			input += 2; // skip ".\n"

			input += 29; // skip "  If the current value is 1:\n"
			input += 22; // skip "    - Write the value "
			st[1].value = numericParse<int>(input);
			input += 2; // skip ".\n"
			input += 27; // skip "    - Move one slot to the "
			if (*input == 'r')
			{
				st[1].dir = 1;
				input += 5; // skip "right"
			}
			else
			{
				st[1].dir = -1;
				input += 4; // skip "left"
			}
			input += 2; // skip ".\n"
			input += 26; // skip "    - Continue with state "
			st[1].next = *input - 'A';
			input++;
			input += 2; // skip ".\n"

			//states.insert({ c, st });
			states[c - 'A'] = st;
		}

		// part 1
		unordered_map<int, int> tape;
		int pos = 0;
		int curr_state = start_state;

		for (int i = 0; i < steps; i++)
		{
			int value = 0;
			if (tape.contains(pos))
			{
				value = tape[pos];
			}

			state& st = states[curr_state];

			// write value
			tape[pos] = st[value].value;

			// move the pos
			pos += st[value].dir;

			// change the state
			curr_state = st[value].next;
		}

		for (auto& p : tape)
		{
			if (p.second == 1)
			{
				part1++;
			}
		}

		return { part1, part2 };
	}
};
