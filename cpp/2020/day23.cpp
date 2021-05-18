#include "../aocHelper.h"

struct Node
{
	Node* next = nullptr;
	int value;
	bool first = false;

	Node(int value) : value(value) {}
};

class Day23 : public BaseDay
{
public:
	Day23() : BaseDay("23") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		auto solve = [](vector<int>& values, int size, int moves, bool part1)
		{
			int max_value = *max_element(values.begin(), values.end());

			unordered_map<int, Node*> val_node;

			Node* start_node = new Node(values[0]);
			val_node[values[0]] = start_node;
			Node* curr_node = start_node;

			//cout << "creating base nodes" << endl;

			// create nodes for given values
			for (auto it = next(values.begin()); it != values.end(); it++)
			{
				Node* next = new Node(*it);
				curr_node->next = next;
				val_node[*it] = next;
				curr_node = next;
			}

			//cout << "creating extra nodes" << endl;

			// create nodes for not given values
			int max_i = max_value + 1 + size - values.size();
			for (int i = max_value + 1; i < max_i; i++)
			{
				Node* next = new Node(i);
				curr_node->next = next;
				val_node[i] = next;
				curr_node = next;
			}

			// makes nodes circular
			curr_node->next = start_node;

			int curr_i = 0;
			int curr_val = values[0];
			curr_node = start_node;

			// make moves
			for (int i = 0; i < moves; i++)
			{
				array<Node*, 3> picked_up;
				array<int, 3> vals;

				for (int j = 0; j < 3; j++)
				{
					Node* cn = curr_node->next;
					picked_up[j] = cn;
					vals[j] = cn->value;
					curr_node->next = curr_node->next->next;
				}

				//cout << "picked up: " << vals[0] << " " << vals[1] << " " << vals[2] << endl;

				int dest_val = curr_node->value - 1;
				if (dest_val <= 0)
				{
					dest_val = size;
				}

				while (dest_val == vals[0] || dest_val == vals[1] || dest_val == vals[2])
				{
					dest_val--;
					if (dest_val <= 0)
					{
						dest_val = size;
					}
				}

				//cout << "dest: " << dest_val << " curr_val: " << curr_node->value << endl;

				Node* dest = val_node[dest_val];

				Node* after = dest->next;
				for (int j = 0; j < 3; j++)
				{
					dest->next = picked_up[2 - j];
					dest->next->next = after;
					after = dest->next;
				}

				curr_node = curr_node->next;
			}

			//cout << "moves stopped" << endl;

			long long answer = 0;

			if (part1)
			{
				Node* curr = val_node[1]->next;
				for (int i = 0, p = 1; i < size - 1; i++, p *= 10)
				{
					answer *= 10;
					answer += curr->value;
					curr = curr->next;
				}
			}
			else
			{
				Node* cup1 = val_node[1];

				answer = (long long) cup1->next->value * cup1->next->next->value;
			}

			// free memory
			Node* temp = start_node;
			for (int i = 0; i < size - 1; i++)
			{
				Node* next = temp->next;
				delete temp;
				temp = next;
			}

			delete temp;

			return answer;
		};

		vector<int> nums;

		// parse

		while (*input != '\n')
		{
			nums.push_back(*input - '0');
			input++;
		}

		// part 1
		//part1 = solve_part1(nums, 100);
		part1 = solve(nums, nums.size(), 100, true);

		// part 2
		part2 = solve(nums, 1'000'000, 10'000'000, false);

		return { part1, part2 };
	}
};
