#include "../aocHelper.h"

class Day08 : public BaseDay
{
public:
	Day08() : BaseDay("08") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int signal_count = 10;
		constexpr int output_count = 4;

		struct data
		{
			array<unordered_set<int>, signal_count> signals;
			array<unordered_set<int>, output_count> output_value;
		};

		const unordered_map<int, const unordered_set<int>> seg_counts = {
			{ 2, { 1 } },
			{ 3, { 7 } },
			{ 4, { 4 } },
			{ 5, { 2, 3, 5 } },
			{ 6, { 0, 6, 9 } },
			{ 7, { 7 } },
		};

		const map<const set<int>, int> seg_pos = {
			{ { 0, 1, 2, 4, 5, 6 }, 0 },
			{ { 2, 5 }, 1 },
			{ { 0, 2, 3, 4, 6 }, 2 },
			{ { 0, 2, 3, 5, 6 }, 3 },
			{ { 1, 2, 3, 5 }, 4 },
			{ { 0, 1, 3, 5, 6 }, 5 },
			{ { 0, 1, 3, 4, 5, 6 }, 6 },
			{ { 0, 2, 5 }, 7 },
			{ { 0, 1, 2, 3, 4, 5, 6 }, 8 },
			{ { 0, 1, 2, 3, 5, 6 }, 9 },
		};

		constexpr array<int, 7> all_values{ 0, 1, 2, 3, 4, 5, 6 };

		vector<data> inputs;

		while (*input != '\0')
		{
			data d;

			for (int i = 0; i < signal_count; i++)
			{
				unordered_set<int> segments;
				while (*input != ' ')
				{
					segments.insert(*input - 'a');
					input++;
				}
				d.signals[i] = segments;
				input++; // skip ' '
			}

			input += 2; // skip '| '

			for (int i = 0; i < output_count; i++)
			{
				unordered_set<int> segments;
				while (*input != ' ' && *input != '\n')
				{
					segments.insert(*input - 'a');
					input++;
				}
				d.output_value[i] = segments;
				input++; // skip ' '
			}

			inputs.push_back(d);
		}

		// part 1
		for (auto& d : inputs)
		{
			for (auto& seg : d.output_value)
			{
				for (auto& p : seg_counts)
				{
					if (p.second.size() == 1)
					{
						if (seg.size() == p.first)
						{
							part1++;
						}
					}
				}
			}
		}

		// part 2

		// checks if a segemnt is valid
		auto check_segments = [&](data& d, unordered_map<int, int>& mapping)
		{
			for (auto& seg : d.signals)
			{
				set<int> seg_set;
				for_each(seg.begin(), seg.end(), [&](int v)
				{
					seg_set.insert(mapping[v]);
				});

				if (!seg_pos.contains(seg_set))
				{
					return false;
				}
			}

			return true;
		};

		// gets the 4 digit number using the given mapping
		auto calc_number = [&](data& d, unordered_map<int, int>& mapping)
		{
			int num = 0;

			for (auto& seg : d.output_value)
			{
				set<int> seg_set;
				for_each(seg.begin(), seg.end(), [&](int v)
				{
					seg_set.insert(mapping[v]);
				});

				int n = seg_pos.at(seg_set);
				num *= 10;
				num += n;
			}

			return num;
		};

		// inserts elements into a new vector, using the specified indices
		auto interleave = [](vector<int>& original, vector<int>& new_values, vector<int>& indices)
		{
			vector<int> result = original;

			for (int i = 0; i < indices.size(); i++)
			{
				result.insert(result.begin() + indices[i], new_values[i]);
			}

			return result;
		};

		auto get_number = [&](data& d, vector<int>& left_values, vector<int>& poss_values, vector<int> indices)
		{
			do
			{
				do
				{
					vector<int> p = interleave(left_values, poss_values, indices);

					unordered_map<int, int> mapping;
					for (int i = 0; i < p.size(); i++)
					{
						mapping[p[i]] = i;
					}

					bool success = check_segments(d, mapping);
					if (success)
					{
						return calc_number(d, mapping);
					}

				} while (next_permutation(left_values.begin(), left_values.end()));
			} while (next_permutation(poss_values.begin(), poss_values.end()));

			return 0;
		};

		for (auto& d : inputs)
		{
			// get the 5 segments that are unique to 1/4/7
			unordered_set<int> poss_segs;

			for (auto& seg : d.signals)
			{
				if (seg.size() <= 4)
				{
					poss_segs.insert(seg.begin(), seg.end()); // set union
				}
			}

			vector<int> left_values;
			for (auto& v : all_values) // set difference
			{
				if (!poss_segs.contains(v))
				{
					left_values.push_back(v);
				}
			}

			sort(left_values.begin(), left_values.end());

			vector<int> poss_values;
			poss_values.insert(poss_values.end(), poss_segs.begin(), poss_segs.end());
			sort(poss_values.begin(), poss_values.end());

			const vector<int> indices = { 0, 1, 2, 3, 5 };

			int num = get_number(d, left_values, poss_values, indices);

			part2 += num;
		}


		return { part1, part2 };
	}
};
