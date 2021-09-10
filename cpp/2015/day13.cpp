#include "../aocHelper.h"

class Day13 : public BaseDay
{
public:
	Day13() : BaseDay("13") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_map<int, string> index_to_person; // index -> person
		unordered_map<string, int> person_to_index; // person -> index
		unordered_set<string> people_set;

		// {person_index: {person_index: happiness_diff}}
		unordered_map<int, unordered_map<int, int>> people;

		auto calc_happiness = [&people]()
		{
			int happiness = 0;

			vector<int> perm(people.size());

			for (int i = 0; i < people.size(); i++)
			{
				perm[i] = i;
			}

			// loop through each permutation
			do
			{
				int tmp_happ = 0;

				for (int i = 0; i < people.size() - 1; i++)
				{
					tmp_happ += people[perm[i]][perm[i + 1]];
					tmp_happ += people[perm[i + 1]][perm[i]];
				}

				tmp_happ += people[perm.front()][perm.back()];
				tmp_happ += people[perm.back()][perm.front()];

				happiness = max(happiness, tmp_happ);

			} while (next_permutation(perm.begin(), perm.end()));

			return happiness;
		};

		// parse input
		while (*input != '\0')
		{
			string person1{ "" };

			while (*input != ' ')
			{
				person1 += *input;
				input++;
			}

			input += 7; // skip ' would '

			bool negative = (*input == 'l');

			input += 5; // skip 'gain ' or 'lose '

			int diff = numericParse<int>(input);
			if (negative)
			{
				diff *= -1;
			}

			input += 36; // skip ' happiness units by sitting next to '

			string person2{ "" };

			while (*input != '.')
			{
				person2 += *input;
				input++;
			}

			int p1_index = -1;
			int p2_index = -1;

			auto f = people_set.find(person1);
			if (f != people_set.end()) // person has been given an index
			{
				p1_index = person_to_index[person1];
			}
			else // person has not been given an index
			{
				people_set.insert(person1);
				p1_index = person_to_index.size();
				person_to_index.insert({ person1, p1_index });
				index_to_person.insert({ p1_index,person1 });
			}

			f = people_set.find(person2);
			if (f != people_set.end()) // person has been given an index
			{
				p2_index = person_to_index[person2];
			}
			else // person has not been given an index
			{
				people_set.insert(person2);
				p2_index = person_to_index.size();
				person_to_index.insert({ person2, p2_index });
				index_to_person.insert({ p2_index,person2 });
			}

			people[p1_index][p2_index] = diff;

			input += 2; // skip '.\n'
		}

		// part 1
		part1 = calc_happiness();

		// part 2

		int my_id = people_set.size();

		for (auto p : people)
		{
			p.second[my_id] = 0;
		}

		for (int i = 0; i < people_set.size(); i++)
		{
			people[my_id][i] = 0;
		}

		part2 = calc_happiness();

		return { part1, part2 };
	}
};
