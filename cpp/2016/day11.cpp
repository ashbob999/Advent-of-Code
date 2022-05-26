#include "../aocHelper.h"

class State
{
public:
	// 64 bits to hold each floor
	// 4 bits per item: 3-bits = id, 1-bit = gen/chip flag (chip=1, gen=0)
	// maximum of 16 items per floor, id range from 0b000 (0) to 0b111 (7) so 8 ids but 0 is ignored
	static constexpr uint64_t bits_per_item = 4;
	static constexpr uint64_t floor_count = 4;
	static constexpr uint64_t max_item_count = 64 / bits_per_item;
	static constexpr uint64_t item_mask = (1 << bits_per_item) - 1;
	static constexpr uint64_t item_id_mask = item_mask ^ 1;
	uint64_t floors[floor_count]{ 0 };
	uint64_t lift_position = 0;

	State() = default;

	State(uint64_t floors[floor_count], uint8_t lift_posistion)
	{
		for (int i = 0; i < floor_count; i++)
		{
			this->floors[i] = floors[i];
		}
		this->lift_position = lift_posistion;
	}

	State(const State&) = default;

public:
	void remove_from_floor(uint64_t item, uint64_t floor_index)
	{
		uint64_t new_floor = 0;
		bool removed = false;

		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if (v == item)
			{
				// skip
				removed = true;
			}
			else
			{
				new_floor <<= bits_per_item;
				new_floor |= v;
			}
		}

		uint64_t tmp_floor = new_floor;
		new_floor = 0;

		// reverse the item order
		for (uint64_t cf = tmp_floor, v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			new_floor <<= bits_per_item;
			new_floor |= v;
		}

		floors[floor_index] = new_floor;
	}

	void add_to_floor(uint64_t item, uint64_t floor_index)
	{
		uint64_t new_floor = 0;

		bool added = false;

		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if (item < v && !added) // add item
			{
				new_floor <<= bits_per_item;
				new_floor |= item;
				added = true;
			}

			new_floor <<= bits_per_item;
			new_floor |= v;
		}

		if (!added)
		{
			new_floor <<= bits_per_item;
			new_floor |= item;
			added = true;
		}

		uint64_t tmp_floor = new_floor;
		new_floor = 0;

		// reverse the item order
		for (uint64_t cf = tmp_floor, v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			new_floor <<= bits_per_item;
			new_floor |= v;
		}

		floors[floor_index] = new_floor;
	}

	bool in_floor(uint64_t floor_index, uint64_t item)
	{
		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if (v == item)
			{
				return true;
			}
		}
		return false;
	}

	bool in_floor(uint64_t floor_index, uint64_t item1, uint64_t item2)
	{
		bool item1_in_floor = false;
		bool item2_in_floor = false;

		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if (v == item1)
			{
				item1_in_floor = true;
			}
			else if (v == item2)
			{
				item2_in_floor = true;
			}
		}

		return item1_in_floor && item2_in_floor;
	}

	bool either_in_floor(uint64_t floor_index, uint64_t item1, uint64_t item2)
	{
		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if (v == item1 || v == item2)
			{
				return true;
			}
		}
		return false;
	}

	bool all_match(uint64_t floor_index, uint64_t type)
	{
		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if ((v & 1) != type)
			{
				return false;
			}
		}

		return true;
	}

	bool all_match(uint64_t floor_index, uint64_t type, uint64_t item_to_exclude)
	{
		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if (v == item_to_exclude)
			{
				// skip
			}
			else
			{
				if ((v & 1) != type)
				{
					return false;
				}
			}
		}

		return true;
	}

	bool all_match(uint64_t floor_index, uint64_t type, uint64_t item_to_exclude1, uint64_t item_to_exclude2)
	{
		for (uint64_t cf = floors[floor_index], v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if (v == item_to_exclude1 || v == item_to_exclude2)
			{
				// skip
			}
			else
			{
				if ((v & 1) != type)
				{
					return false;
				}
			}
		}

		return true;
	}

	bool all_chips_paired(uint64_t floor_index)
	{
		for (uint64_t cf1 = floors[floor_index], v1 = cf1 & item_mask; cf1 > 0; cf1 >>= bits_per_item, v1 = cf1 & item_mask)
		{
			if ((v1 & 1) == 1) // is chip
			{
				bool found = false;
				for (uint64_t cf2 = floors[floor_index], v2 = cf2 & item_mask; cf2 > 0; cf2 >>= bits_per_item, v2 = cf2 & item_mask)
				{
					if ((v2 & 1) == 0) // is generator
					{
						if ((v1 & item_id_mask) == (v2 & item_id_mask)) // is match
						{
							found = true;
							break;
						}
					}
				}

				if (!found)
				{
					return false;
				}
			}
		}

		return true;
	}

	bool all_chips_paired(uint64_t floor_index, uint64_t chip_to_exclude1, uint64_t chip_to_exclude2)
	{
		for (uint64_t cf1 = floors[floor_index], v1 = cf1 & item_mask; cf1 > 0; cf1 >>= bits_per_item, v1 = cf1 & item_mask)
		{
			if ((v1 & 1) == 1) // is chip
			{
				if (v1 == chip_to_exclude1 || v1 == chip_to_exclude2)
				{
					continue;
				}
				bool found = false;
				for (uint64_t cf2 = floors[floor_index], v2 = cf2 & item_mask; cf2 > 0; cf2 >>= bits_per_item, v2 = cf2 & item_mask)
				{
					if ((v2 & 1) == 0) // is generator
					{
						if ((v1 & item_id_mask) == (v2 & item_id_mask)) // is match
						{
							found = true;
							break;
						}
					}
				}

				if (!found)
				{
					return false;
				}
			}
		}

		return true;
	}

public:
	void sort_floors()
	{
		//return;
		// slow so shouldn't be used often
		for (int floor_index = 0; floor_index < floor_count; floor_index++)
		{
			uint8_t items[max_item_count];
			for (int j = 0; j < max_item_count; j++)
			{
				items[j] = (floors[floor_index] >> (j * bits_per_item)) & item_mask;
			}

			sort(items, items + max_item_count, std::less<uint8_t>());

			uint64_t new_floor = 0;
			for (int j = 0; j < max_item_count; j++)
			{
				if (items[j] == 0)
				{
					break;
				}
				new_floor <<= bits_per_item;
				new_floor |= items[j];
			}

			floors[floor_index] = new_floor;
		}
	}

	void print()
	{
		for (int i = floor_count - 1; i >= 0; i--)
		{
			cout << i << ": " << bitset<64>(floors[i]) << endl;
		}
		cout << "lift pos: " << (uint64_t) lift_position << endl << endl;
	}

private:
	void move_gen(uint64_t next_floor, vector<State>& next_states)
	{
		uint64_t curr_floor = floors[lift_position];

		for (uint64_t cf = curr_floor, v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if ((v & 1) == 0) // is generator
			{
				// only move generator out of room if either:
				//		its chip is not in room
				//		its chip is in room and no other generator in room
				bool can_move_out = false;
				uint64_t chip = v | 1;
				if (!in_floor(lift_position, chip))
				{
					can_move_out = true;
				}
				else if (in_floor(lift_position, chip) && all_match(lift_position, 0x1, v))
				{
					can_move_out = true;
				}

				if (can_move_out)
				{
					// only move generator into room :
					//		where all chips have their own generator
					if (all_chips_paired(next_floor))
					{
						State s{ *this };
						s.lift_position = next_floor;
						s.remove_from_floor(v, lift_position);
						s.add_to_floor(v, next_floor);
						next_states.push_back(s);
					}
				}
			}
		}
	}

	void move_chip(uint64_t next_floor, vector<State>& next_states)
	{
		uint64_t curr_floor = floors[lift_position];

		for (uint64_t cf = curr_floor, v = cf & item_mask; cf > 0; cf >>= bits_per_item, v = cf & item_mask)
		{
			if ((v & 1) == 1) // is chip
			{
				// chip can move out of any room

				// only move chip into room if either:
				//		no generators in room
				//		its generator in room
				bool can_move_out = false;
				uint64_t gen = v & item_id_mask;
				if (all_match(next_floor, 0x1))
				{
					can_move_out = true;
				}
				else if (in_floor(next_floor, gen))
				{
					can_move_out = true;
				}

				if (can_move_out)
				{
					State s{ *this };
					s.lift_position = next_floor;
					s.remove_from_floor(v, lift_position);
					s.add_to_floor(v, next_floor);
					next_states.push_back(s);
				}
			}
		}
	}

	void move_gen_gen(uint64_t next_floor, vector<State>& next_states)
	{
		uint64_t curr_floor = floors[lift_position];

		for (uint64_t cf1 = curr_floor, v1 = cf1 & item_mask; cf1 > 0; cf1 >>= bits_per_item, v1 = cf1 & item_mask)
		{
			if ((v1 & 1) == 0) // is generator
			{
				for (uint64_t cf2 = cf1, v2 = cf2 & item_mask; cf2 > 0; cf2 >>= bits_per_item, v2 = cf2 & item_mask)
				{
					if ((v2 & 1) == 0 && v1 != v2) // is generator
					{
						// can only move both generators out:
						//		if either chip is in room, no other generators
						//		both its chips not in room
						bool can_move_out = false;
						uint64_t chip1 = v1 | 1;
						uint64_t chip2 = v2 | 1;
						if (either_in_floor(lift_position, v1, v2) && all_match(lift_position, 0x1, v1, v2))
						{
							can_move_out = true;
						}
						else if (!in_floor(lift_position, chip1) && !in_floor(lift_position, chip2))
						{
							can_move_out = true;
						}

						if (can_move_out)
						{
							// only move generators into room :
							//		where all chips will have their own generators
							if (all_chips_paired(next_floor, chip1, chip2)) // check
							{
								State s{ *this };
								s.lift_position = next_floor;
								s.remove_from_floor(v1, lift_position);
								s.remove_from_floor(v2, lift_position);
								s.add_to_floor(v1, next_floor);
								s.add_to_floor(v2, next_floor);
								next_states.push_back(s);
							}
						}
					}
				}
			}
		}
	}

	void move_chip_chip(uint64_t next_floor, vector<State>& next_states)
	{
		uint64_t curr_floor = floors[lift_position];

		for (uint64_t cf1 = curr_floor, v1 = cf1 & item_mask; cf1 > 0; cf1 >>= bits_per_item, v1 = cf1 & item_mask)
		{
			if ((v1 & 1) == 1) // is chip
			{
				for (uint64_t cf2 = cf1, v2 = cf2 & item_mask; cf2 > 0; cf2 >>= bits_per_item, v2 = cf2 & item_mask)
				{
					if ((v2 & 1) == 1 && v1 != v2) // is chip
					{
						// both chips can move out of any room

						// only move chips into room if either:
						//		no generators in room
						//		both its generators in room
						bool can_move_into = false;
						uint64_t gen1 = v1 & item_id_mask;
						uint64_t gen2 = v2 & item_id_mask;
						if (all_match(next_floor, 0x1))
						{
							can_move_into = true;
						}
						else if (in_floor(next_floor, gen1, gen2))
						{
							can_move_into = true;
						}

						if (can_move_into)
						{
							State s{ *this };
							s.lift_position = next_floor;
							s.remove_from_floor(v1, lift_position);
							s.remove_from_floor(v2, lift_position);
							s.add_to_floor(v1, next_floor);
							s.add_to_floor(v2, next_floor);
							next_states.push_back(s);
						}
					}
				}
			}
		}
	}

	void move_gen_chip(uint64_t next_floor, vector<State>& next_states)
	{
		uint64_t curr_floor = floors[lift_position];

		for (uint64_t cf1 = curr_floor, v1 = cf1 & item_mask; cf1 > 0; cf1 >>= bits_per_item, v1 = cf1 & item_mask)
		{
			if ((v1 & 1) == 1) // is chip
			{
				for (uint64_t cf2 = curr_floor, v2 = cf2 & item_mask; cf2 > 0; cf2 >>= bits_per_item, v2 = cf2 & item_mask)
				{
					if ((v2 & 1) == 0 && (v1 & item_id_mask) == (v2 & item_id_mask)) // is generator
					{
						// chip can move out of any room

						// only move generators into room :
						//		where all chips have their own generators
						if (all_chips_paired(next_floor))
						{
							State s{ *this };
							s.lift_position = next_floor;
							s.remove_from_floor(v1, lift_position);
							s.remove_from_floor(v2, lift_position);
							s.add_to_floor(v1, next_floor);
							s.add_to_floor(v2, next_floor);
							next_states.push_back(s);
						}
					}
				}
			}
		}
	}

public:
	vector<State> get_next_states()
	{
		vector<State> next_states;

		if (this->lift_position < floor_count - 1)
		{
			move_gen(this->lift_position + 1, next_states);
			move_chip(this->lift_position + 1, next_states);
			move_gen_gen(this->lift_position + 1, next_states);
			move_chip_chip(this->lift_position + 1, next_states);
			move_gen_chip(this->lift_position + 1, next_states);
		}

		if (this->lift_position > 0)
		{
			move_gen(this->lift_position - 1, next_states);
			move_chip(this->lift_position - 1, next_states);
			move_gen_gen(this->lift_position - 1, next_states);
			move_chip_chip(this->lift_position - 1, next_states);
			move_gen_chip(this->lift_position - 1, next_states);
		}

		return next_states;
	}

	bool operator==(const State& other) const
	{
		if (this->lift_position != other.lift_position)
		{
			return false;
		}

		for (int i = 0; i < floor_count; i++)
		{
			if (this->floors[i] != other.floors[i])
			{
				return false;
			}
		}

		return true;
	}
};

namespace std
{
	template <>
	struct hash<State>
	{
		size_t operator()(const State& k) const
		{
			// Compute individual hash values for first, second and third
			// http://stackoverflow.com/a/1646913/126995
			size_t res = 17ULL;
			for (int i = 0; i < State::floor_count; i++)
			{
				res = res * 31ULL + hash<uint64_t>()(k.floors[i]);
			}
			res = res * 31ULL + hash<uint64_t>()(k.lift_position);
			return res;
		}
	};
}

class Day11 : public BaseDay
{
public:
	Day11() : BaseDay("11") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		auto bfs = [&](State start, State end)
		{
			deque<State> to_check;
			to_check.push_back(start);

			unordered_map<State, int> dists;
			dists[start] = 0;

			while (to_check.size() > 0)
			{
				State& curr_state = to_check.front();
				int curr_dist = dists[curr_state];

				vector<State> next_states = curr_state.get_next_states();

				to_check.pop_front();

				for (auto& state : next_states)
				{
					if (state == end)
					{
						return curr_dist + 1;
					}
					else
					{
						if (!dists.contains(state) || curr_dist + 1 < dists[state])
						{
							to_check.push_back(state);
							dists[state] = curr_dist + 1;
						}
					}
				}
			}
			cout << "none found" << endl;
			return 0;
		};

		unordered_set<string> names;

		array<vector<pair<string, bool>>, State::floor_count> raw_floors{};

		vector<char*> spaces;
		uint64_t floor_index = 0;

		// parse input
		while (*input != '\0')
		{
			if (*input == ' ' && (*(input + 1) == 'm' || *(input + 1) == 'g'))
			{
				char* last_space = *spaces.rbegin();
				auto f = find(last_space + 1, input, '-');
				if (f != input)
				{
					// is microchip
					raw_floors[floor_index].emplace_back(string{ last_space + 1, f }, true);
				}
				else
				{
					// is generator
					raw_floors[floor_index].emplace_back(string{ last_space + 1, input }, false);
					names.insert(string{ last_space + 1, input });
				}
			}
			else if (*input == ' ')
			{
				spaces.push_back(input);
			}

			else if (*input == '\n')
			{
				spaces.empty();
				floor_index++;
				if (floor_index > State::floor_count - 2)
				{
					break;
				}
			}
			input++;
		}

		unordered_map<string, uint64_t> name_to_id;
		uint8_t id = 1;
		for (auto& name : names)
		{
			name_to_id[name] = id;
			id++;
		}

		State start_state;
		start_state.lift_position = 0;

		for (uint64_t fi = 0; fi < State::floor_count - 1; fi++)
		{
			int value_count = 0;
			for (auto& p : raw_floors[fi])
			{
				uint64_t value = name_to_id[p.first] << 1;
				if (p.second)
				{
					value |= 1; // is microchip
				}

				start_state.add_to_floor(value, fi);

				value_count++;
			}
		}

		State target_state;
		target_state.lift_position = State::floor_count - 1;

		int value_count = 0;
		for (size_t fi = 0; fi < State::floor_count - 1; fi++)
		{
			for (auto& p : raw_floors[fi])
			{
				uint64_t value = name_to_id[p.first] << 1;
				if (p.second)
				{
					value |= 1; // is microchip
				}

				target_state.add_to_floor(value, State::floor_count - 1);

				value_count++;
			}
		}

		// part 1
		part1 = bfs(start_state, target_state);

		// part 2

		// [("elerium", "G"), ("elerium", "M"), ("dilithium", "G"), ("dilithium", "M")]
		vector<string> new_chips = { "elerium", "dilithium" };
		vector<string> new_gens = { "elerium", "dilithium" };

		name_to_id["elerium"] = id;
		id++;
		name_to_id["dilithium"] = id;
		id++;

		start_state.add_to_floor((name_to_id["elerium"] << 1) | 1, 0); // elerium chip
		start_state.add_to_floor(name_to_id["elerium"] << 1, 0); // elerium generator
		start_state.add_to_floor((name_to_id["dilithium"] << 1) | 1, 0); // dilithium chip
		start_state.add_to_floor(name_to_id["dilithium"] << 1, 0); // dilithium generator

		target_state.add_to_floor((name_to_id["elerium"] << 1) | 1, State::floor_count - 1); // elerium chip
		target_state.add_to_floor(name_to_id["elerium"] << 1, State::floor_count - 1); // elerium generator
		target_state.add_to_floor((name_to_id["dilithium"] << 1) | 1, State::floor_count - 1); // dilithium chip
		target_state.add_to_floor(name_to_id["dilithium"] << 1, State::floor_count - 1); // dilithium generator

		part2 = bfs(start_state, target_state);

		return { part1, part2 };
	}
};
