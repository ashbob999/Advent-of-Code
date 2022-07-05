#include "../aocHelper.h"


class Day07 : public BaseDay
{
public:
	Day07() : BaseDay("07") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct Node
		{
			string name;
			int weight;
			vector<Node*> child_nodes;
			Node* parent_node = nullptr;

			Node(string& name, int weight) : name(name), weight(weight)
			{}

			int calc_weight()
			{
				int s = this->weight;
				for (auto& c : this->child_nodes)
				{
					s += c->calc_weight();
				}
				return s;
			}

			pair<bool, int> is_balanced()
			{
				if (this->child_nodes.size() == 0)
				{
					return { true, 0 };
				}

				unordered_map<int, int> counts;
				for (auto& c : this->child_nodes)
				{
					auto res = c->is_balanced();
					if (!res.first)
					{
						return res;
					}

					int cw = c->calc_weight();
					if (counts.contains(cw))
					{
						counts[cw]++;
					}
					else
					{
						counts[cw] = 1;
					}
				}

				if (counts.size() == 1)
				{
					return { true, 0 };
				}

				if (counts.size() > 2)
				{
					return { false, -1 };
				}

				vector<int> keys;
				for (auto& p : counts)
				{
					keys.push_back(p.first);
				}

				sort(keys.begin(), keys.end(), [&](const int& a, const int& b)
				{
					return counts[a] < counts[b];
				});

				int diff = keys[1] - keys[0];

				Node* tmp = nullptr;

				for (auto& c : this->child_nodes)
				{
					if (c->calc_weight() == keys[0])
					{
						tmp = c;
						break;
					}
				}

				return { false, tmp->weight + diff };
			}
		};

		struct raw_node
		{
			string name;
			int weight;
			vector<string> child_nodes;
		};

		vector<raw_node> raw_nodes;
		unordered_map<string, Node*> node_dict;

		// parse input

		string str;

		while (*input != '\0')
		{
			raw_node curr_node;

			while (*input >= 'a' && *input <= 'z')
			{
				curr_node.name += *input;
				input++;
			}

			input += 2; // slip " ("

			curr_node.weight = numericParse<int>(input);

			input++; // skip ')'

			if (*input != '\n')
			{
				input += 4; // skip " -> "

				string str;

				while (*input != '\n')
				{
					str += *input;
					input++;

					if (*input == ',')
					{
						input += 2; // skip ", "
						curr_node.child_nodes.push_back(str);
						str = "";
					}
				}

				curr_node.child_nodes.push_back(str);
			}

			raw_nodes.push_back(curr_node);
			node_dict[curr_node.name] = new Node(curr_node.name, curr_node.weight);

			input++; // skip '\n'
		}

		// build tree
		for (auto& rn : raw_nodes)
		{
			Node* node = node_dict[rn.name];

			for (auto& c : rn.child_nodes)
			{
				Node* child_node = node_dict[c];
				node->child_nodes.push_back(child_node);
				child_node->parent_node = node;
			}
		}

		Node* tree_node = nullptr;

		// part 1
		for (auto& p : node_dict)
		{
			if (p.second->parent_node == nullptr)
			{
				tree_node = p.second;
				memcpy(stringResult.first, p.first.c_str(), p.first.length());
				break;
			}
		}

		// part 2
		auto res = tree_node->is_balanced();
		part2 = res.second;

		for (auto& p : node_dict)
		{
			delete p.second;
		}

		return { part1, part2 };
	}
};
