#include "../aocHelper.h"

class Day10 : public BaseDay
{
public:
	Day10() : BaseDay("10")
	{}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct node
		{
			int value;
			node* next;

			node(int v, node* n) : value(v), next(n)
			{}

			node(int v) : value(v), next(nullptr)
			{}

			node() : value(0), next(nullptr)
			{}
		};

		auto do_exchange = [](node* start)
		{
			int value = start->value;

			node* tmp = start;


			// get length of the same value nodes
			int length = 0;

			while (tmp != nullptr && tmp->value == value)
			{
				length++;
				tmp = tmp->next;
			}

			node* after = tmp;

			if (length > 1)
			{
				if (length > 2)
				{
					// delete middle nodes
					tmp = start->next->next;
					for (int i = 0; i < length - 2; i++)
					{
						node* next = tmp->next;
						delete tmp;
						tmp = next;
					}
				}

				// insert value into second node
				start->next->value = value;
				start->next->next = after;

				// update first node
				start->value = length;
				// start->next = value_node;
			}
			else
			{
				node* value_node = new node(value, after);

				start->value = length;
				start->next = value_node;
			}

			return after;
		};

		auto step_process = [&do_exchange](node* start)
		{
			node* next = start;

			while (next != nullptr)
			{
				next = do_exchange(next);
			}
		};

		auto calc_length = [](node* start)
		{
			int length = 0;
			while (start != nullptr)
			{
				length++;
				start = start->next;
			}

			return length;
		};

		int value = (*input) - '0';

		node* start = new node(value);
		node* curr = start;

		input++;

		// parse input
		while (*input != '\n')
		{
			value = (*input) - '0';
			
			node* next = new node(value);

			curr->next = next;

			curr = next;

			input++;
		}

		// part 1
		int i = 0;
		for (; i < 40; i++)
		{
			step_process(start);
		}

		part1 = calc_length(start);

		// part 2
		for (; i < 50; i++)
		{
			step_process(start);
		}

		part2 = calc_length(start);

		// clean up
		node* tmp = start;

		while (tmp != nullptr)
		{
			node* next = tmp->next;

			delete tmp;

			tmp = next;
		}

		return { part1, part2 };
	}
};
