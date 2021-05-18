#include "../aocHelper.h"

struct field
{
	int low1;
	int high1;
	int low2;
	int high2;
	field() : low1(), high1(), low2(), high2() {}
	field(int l1, int h1, int l2, int h2) : low1(l1), high1(h1), low2(l2), high2(h2) {}
};

class Day16 : public BaseDay
{
public:
	Day16() : BaseDay("16") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<char*> field_starts;
		vector<field> fields;

		int* my_ticket;
		list<int*> tickets;

		// parse input

		// parse fields
		while (*input != '\n')
		{
			field_starts.push_back(input);

			// skip text
			while (*input != ':')
			{
				input++;
			}
			input += 2;

			field f;

			// get first range
			f.low1 = numericParse<int>(input);
			input++; // skip -
			f.high1 = numericParse<int>(input);
			input += 4; // skip or

			//get second range
			f.low2 = numericParse<int>(input);
			input++; // skip -
			f.high2 = numericParse<int>(input);

			fields.push_back(f);

			input++; // skip newline
		}

		// parse our ticket
		input++; // skip newline
		input += 12; // skip your ticket:
		my_ticket = new int[fields.size()];

		for (int i = 0; i < fields.size(); i++)
		{
			my_ticket[i] = numericParse<int>(input);
			input++; // skip ,
		}

		input++; // skip newline

		// parse other tickets
		input += 16; // skip nearby tickets:

		while (*input != '\0')
		{
			int* ticket = new int[fields.size()];

			for (int i = 0; i < fields.size(); i++)
			{
				ticket[i] = numericParse<int>(input);
				input++; // skip ,
			}

			tickets.push_back(ticket);
		}

		// part 1

		// create intervals
		pair<int, int>* intervals = new pair<int, int>[fields.size() * 2];

		for (int i = 0; i < fields.size(); i++)
		{
			intervals[i * 2] = { fields[i].low1, fields[i].high1 };
			intervals[(i * 2) + 1] = { fields[i].low2, fields[i].high2 };
		}

		// merge intervals
		sort(intervals, intervals + fields.size() * 2);

		int index = 0;
		for (int i = 1; i < fields.size() * 2; i++)
		{
			if (intervals[index].second >= intervals[i].first)
			{
				intervals[index].second = max(intervals[index].second, intervals[i].second);
				intervals[index].first = min(intervals[index].first, intervals[i].first);
			}
			else
			{
				index++;
				intervals[index] = intervals[i];
			}
		}

		// check invalid tickets
		for (auto it = tickets.begin(); it != tickets.end();)
		{
			bool invalid = false;
			// check invalid fields for each interval
			for (int int_index = 0; int_index <= index; int_index++)
			{
				for (int field_index = 0; field_index < fields.size(); field_index++)
				{
					if ((*it)[field_index] < intervals[int_index].first || (*it)[field_index] > intervals[int_index].second)
					{
						invalid = true;
						part1 += (*it)[field_index];
					}
				}
			}

			if (invalid) // remove invalid tickets
			{
				delete[] * it;
				it = tickets.erase(it);
			}
			else
			{
				++it;
			}
		}

		// part 2

		// create ranges for each ticket field
		unordered_set<int>* field_ranges = new unordered_set<int>[fields.size()];

		for (auto& ticket : tickets)
		{
			for (int field_index = 0; field_index < fields.size(); field_index++)
			{
				field_ranges[field_index].insert(ticket[field_index]);
			}
		}

		// create poss array
		unordered_set<int>* poss_values = new unordered_set<int>[fields.size()];

		for (int field_index = 0; field_index < fields.size(); field_index++)
		{
			for (int fi = 0; fi < fields.size(); fi++)
			{
				auto& f = fields[fi];

				bool in_range = true;

				for (auto& ticket : tickets)
				{
					int val = ticket[field_index];
					if ((f.low1 > val || f.high1 < val) && (f.low2 > val || f.high2 < val))
					{
						in_range = false;
						break;
					}
				}

				if (in_range)
				{
					poss_values[field_index].insert(fi);
				}
			}
		}

		// find final fields positions
		int* final_fields = new int[fields.size()];
		int placed = 0;

		while (placed < fields.size())
		{
			//cout << placed << endl;
			for (int field_index = 0; field_index < fields.size(); field_index++)
			{
				//cout << poss_values[field_index].size() << endl;
				if (poss_values[field_index].size() == 1)
				{
					placed++;
					int val = *poss_values[field_index].begin();
					final_fields[field_index] = val;

					for (int i = 0; i < fields.size(); i++)
					{
						poss_values[i].erase(val);
					}
				}
			}
		}

		// get destination values
		part2 = 1;

		for (int field_index = 0; field_index < fields.size(); field_index++)
		{
			if (strncmp(field_starts[final_fields[field_index]], "departure", 9) == 0)
			{
				part2 *= my_ticket[field_index];
			}
		}

		// free memory
		delete[] my_ticket;
		delete[] intervals;
		delete[] field_ranges;
		delete[] final_fields;
		delete[] poss_values;

		for (auto& ticket : tickets)
		{
			delete[] ticket;
		}

		return { part1, part2 };
	}
};
