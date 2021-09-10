#include "../aocHelper.h"

#include <variant>

class Day12 : public BaseDay
{
public:
	Day12() : BaseDay("12") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// this solution is effectively a JSON parse, but I didn't want to use external libs
		// also this should never be used on real JSON

		enum class value_type : int
		{
			STRING,
			NUMBER,
			ARRAY,
			OBJECT
		};

		struct value
		{
			value_type type;
			variant<string, int, vector<value*>, unordered_map<char, value*>> data;

			value(value_type t_) : type(t_)
			{
				switch (t_)
				{
					case value_type::STRING:
						data.emplace<string>();
						break;
					case value_type::NUMBER:
						data.emplace<int>();
						break;
					case value_type::ARRAY:
						data.emplace<vector<value*>>();
						break;
					case value_type::OBJECT:
						data.emplace<unordered_map<char, value*>>();
						break;
				}
			}
		};

		vector<value*> pointers;

		function<int(value*, bool)> calc_sum;
		calc_sum = [&calc_sum](value* root, bool ignore_red)
		{
			int sum = 0;

			switch (root->type)
			{
				case value_type::STRING:
				{
					break;
				}
				case value_type::NUMBER:
				{
					sum += get<int>(root->data);
					break;
				}
				case value_type::ARRAY:
				{
					for (auto& v : get<vector<value*>>(root->data))
					{
						sum += calc_sum(v, ignore_red);
					}
					break;
				}
				case value_type::OBJECT:
				{
					int tmp_sum = 0;

					for (auto& p : get<unordered_map<char, value*>>(root->data))
					{
						if (ignore_red && p.second->type == value_type::STRING)
						{
							string& s = get<string>(p.second->data);

							if (s.length() >= 3 && s[0] == 'r' && s[1] == 'e' && s[2] == 'd')
							{
								// ignore values and children
								tmp_sum = 0;
								break;
							}
						}

						tmp_sum += calc_sum(p.second, ignore_red);
					}

					sum += tmp_sum;

					break;
				}
			}
			return sum;
		};

		function<value* (char*&)> parse_section;

		auto handle_type = [&parse_section, &pointers](char*& input)
		{
			value* item;

			if (*input == '{') // object
			{
				item = parse_section(input);
			}
			else if (*input == '[') // array
			{
				item = parse_section(input);
			}
			else if (*input == '"') // string
			{
				input++; // skip opening "

				item = new value(value_type::STRING);

				while (*input != '"')
				{
					get<string>(item->data) += *input;
					input++;
				}

				input++; // skip closing "
			}
			else if ((*input >= '0' && *input <= '9') || *input == '-') // number positive/negative
			{
				bool is_negative = false;

				if (*input == '-')
				{
					is_negative = true;
					input++; // skip -
				}

				int i = numericParse<int>(input);

				if (is_negative)
				{
					i *= -1;
				}

				item = new value(value_type::NUMBER);
				item->data.emplace<int>(i);
			}
			else
			{
			}

			// add item to pointers
			pointers.push_back(item);

			return item;
		};

		parse_section = [&pointers, &parse_section, &handle_type](char*& input)
		{
			value* root;

			if (*input == '{') // object
			{
				root = new value(value_type::OBJECT);
			}
			else // array
			{
				root = new value(value_type::ARRAY);
			}

			input++; // skip opening {/[

			if (root->type == value_type::OBJECT) // loop through object key/value pairs
			{
				while (*input != '}')
				{
					input++; // skip opening "

					char key = *input; // get key
					input++; // skip key

					input++; // skip closing "

					// skip :
					input++;

					value* item = handle_type(input);

					if (*input == ',') // skip ,
					{
						input++;
					}

					// add item to object
					get<unordered_map<char, value*>>(root->data).insert({ key, item });
				}
			}
			else // loop through array items
			{
				while (*input != ']')
				{
					value* item = handle_type(input);

					if (*input == ',') // skip ,
					{
						input++;
					}

					// add item to array
					get<vector<value*>>(root->data).push_back(item);
				}
			}

			input++; // skip closing } or }

			return root;
		};

		// parse input

		//value* root = parse_section(input);
		value* root = handle_type(input);

		// part 1
		part1 = calc_sum(root, false);

		// part 2
		part2 = calc_sum(root, true);

		// delete all pointers
		for (auto& p : pointers)
		{
			delete p;
		}

		return { part1, part2 };
	}
};
