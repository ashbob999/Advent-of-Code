#include "../aocHelper.h"

#include <immintrin.h>

// make sea monster orientations compile time
const uint32_t horizontal_sm[4][3] = { {74898, 923745, 262144},
									   {262144, 923745, 74898},
									   {299592, 549255, 2},
									   {2, 549255, 299592}
};

const uint8_t vertical_sm[4][20] = { {2, 4, 0, 0, 4, 2, 2, 4, 0, 0, 4, 2, 2, 4, 0, 0, 4, 2, 3, 2},
									 {2, 3, 2, 4, 0, 0, 4, 2, 2, 4, 0, 0, 4, 2, 2, 4, 0, 0, 4, 2},
									 {2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 6, 2},
									 {2, 6, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2}
};

struct tile
{
	int id;
	array<uint16_t, 16> rows;
	array<uint16_t, 8> sides;

	tile() : id(0), rows(), sides() {}

	tile(char*& input) : rows(), sides()
	{
		// parse tile
		input += 5;
		id = numericParse<int>(input);
		input += 2;

		for (int y = 0; y < 10; y++)
		{
			for (int x = 0; x < 10; x++)
			{
				rows[y] <<= 1;
				if (*input == '#')
				{
					rows[y] |= 1;
				}
				input++;
			}
			input++;
		}

		// get sides
		sides[0] = rows[0]; // top
		sides[1] = rows[9]; // bottom
		for (int i = 0; i < 10; i++)
		{
			// left
			sides[2] |= ((rows[i] >> 9) & 1) << (9 - i);

			// right
			sides[3] <<= 1;
			sides[3] |= rows[i] & 1;
		}

		sides[4] = reverse(sides[0]); // reverse top
		sides[5] = reverse(sides[1]); // reverse bottom
		sides[6] = reverse(sides[2]); // reverse left
		sides[7] = reverse(sides[3]); // reverse right
	}

	static uint16_t reverse(uint16_t value)
	{
		value = (value & 0x00ff) << 8 | (value & 0xff00) >> 8;
		value = (value & 0x0f0f) << 4 | (value & 0xf0f0) >> 4;
		value = (value & 0x3333) << 2 | (value & 0xcccc) >> 2;
		value = (value & 0x5555) << 1 | (value & 0xaaaa) >> 1;
		return value >> 6;
	}

	static optional<uint16_t> share_sides(const tile& t1, const tile& t2)
	{
		for (auto side1 : t1.sides)
		{
			for (auto side2 : t2.sides)
			{
				if (side1 == side2)
				{
					return { side1 };
				}
			}
		}
		return {};
	}

	void flip(int dir)
	{
		if (dir == 0) // vertical
		{
			for (int i = 0; i < 5; i++)
			{
				swap(rows[i], rows[9 - i]);
			}
		}
		else // horizontal
		{
			for (int i = 0; i < 10; i++)
			{
				rows[i] = reverse(rows[i]);
			}
		}
	}

	// transposes a 16x16 matrix
	void transpose()
	{
		uint16_t j, k, m, t;
		m = 0b0000'0000'1111'1111;
		for (j = 8; j != 0; j >>= 1, m ^= (m << j))
		{
			for (k = 0; k < 16; k = (k + j + 1) & ~j)
			{
				t = (rows[k] ^ (rows[k + j] >> j)) & m;
				rows[k] ^= t;
				rows[k + j] ^= (t << j);
			}
		}

		for (int i = 0; i < 10; i++)
		{
			// shift up 6
			rows[i] = rows[i + 6];
			// clear bottom
			rows[i + 6] = 0;
			// shift left 6
			rows[i] >>= 6;
		}
	}

	void rotate()
	{
		transpose();
		flip(1);
	}
};

struct tile_match_type
{
	int m_k1;
	int m_k2;
	uint16_t m_side1;
	uint16_t m_side2;
	tile_match_type(int k1, int k2, uint16_t side1) : m_k1(k1), m_k2(k2), m_side1(side1), m_side2(tile::reverse(side1)) {}
	inline int get_other(int k)
	{
		if (k == m_k1)
		{
			return m_k2;
		}
		return m_k1;
	}
};

struct tile_match_type_hash
{
	std::size_t operator () (const tile_match_type& tile_type) const
	{
		uint64_t result = 0;
		if (tile_type.m_k1 < tile_type.m_k2)
		{
			result |= (uint64_t) tile_type.m_k1 << 48;
			result |= (uint64_t) tile_type.m_k2 << 32;
		}
		else
		{
			result |= (uint64_t) tile_type.m_k2 << 48;
			result |= (uint64_t) tile_type.m_k1 << 32;
		}

		if (tile_type.m_side1 < tile_type.m_side2)
		{
			result |= (uint64_t) tile_type.m_side1 << 16;
			result |= (uint64_t) tile_type.m_side2;
		}
		else
		{
			result |= (uint64_t) tile_type.m_side2 << 16;
			result |= (uint64_t) tile_type.m_side1;
		}

		return result;
	}
};

struct tile_match_type_equal
{
	bool operator () (const tile_match_type& lhs, const tile_match_type& rhs) const
	{
		return (lhs.m_k1 == rhs.m_k1) && (lhs.m_k2 == rhs.m_k2) && (lhs.m_side1 == rhs.m_side1) && (lhs.m_side2 == rhs.m_side2);
	}
};

struct grid
{
	unordered_map<int, tile> tiles;
	unordered_set<uint16_t> all_sides;

	unordered_map<int, unordered_set<int>> m_count;
	unordered_set<tile_match_type, tile_match_type_hash, tile_match_type_equal> m_boards;
	array<vector<int>, 5> c_id;

	array<array<uint32_t, 3>, 96> g;
	tile tile_grid[12][12];
	array<array<int, 12>, 12> ids;
	unordered_set<int> been_placed;

	grid()
	{
		for (int y = 0; y < 96; y++)
		{
			g[y][0] = 0;
			g[y][1] = 0;
			g[y][2] = 0;
		}
	}

	void load_tiles(char*& input)
	{
		while (*input != '\0')
		{
			tile t(input);
			tiles.insert({ t.id, t });
			input++;
		}
	}

	long long part1()
	{
		long long part1 = 1;

		for (auto& p : tiles)
		{
			int k = p.first;
			tile& v = p.second;

			for (auto& p2 : tiles)
			{
				if (k == p2.first)
				{
					continue;
				}

				int k2 = p2.first;
				auto& v2 = p2.second;

				auto match = tile::share_sides(v, v2);
				if (match)
				{
					auto inserted = m_boards.insert({ k,k2,match.value() });
					m_count[k].insert(k2);
					all_sides.insert(inserted.first->m_side1);
					all_sides.insert(inserted.first->m_side2);
				}
			}
		}

		part1 = 1;
		for (auto& p : m_count)
		{
			int id = p.first;
			auto& ms = p.second;
			c_id[ms.size()].push_back(id);
			if (ms.size() == 2)
			{
				part1 *= id;
			}
		}

		return part1;
	}

	// gets a list of adjacent tiles
	vector<tile_match_type> get_adj(int id)
	{
		vector<tile_match_type> matches;
		for (auto& data : m_boards)
		{
			if (id == data.m_k1 || id == data.m_k2)
			{
				matches.push_back(data);
			}
		}

		return matches;
	}

	// gets the next tile
	int get_next(vector<tile_match_type>& adj, int pid, int count)
	{
		for (auto& ad : adj)
		{
			int n_id = ad.get_other(pid);
			auto f1 = find(c_id[count].begin(), c_id[count].end(), n_id);
			if (f1 != c_id[count].end())
			{
				auto f2 = been_placed.find(n_id);
				if (f2 == been_placed.end())
				{
					return n_id;
				}
			}
		}
		return 0;
	}

	// fills up a row
	void fill_row(int start, int end, int col, int count)
	{
		for (int x = start; x <= end - 1; x++)
		{
			int pid = ids[col][x - 1];
			auto adj = get_adj(pid);
			int curr_id = get_next(adj, pid, count);

			ids[col][x] = curr_id;
			been_placed.insert(curr_id);
		}
	}

	// fills up a column
	void fill_col(int start, int end, int row, int count)
	{
		for (int y = start; y <= end - 1; y++)
		{
			int pid = ids[y - 1][row];
			auto adj = get_adj(pid);
			int curr_id = get_next(adj, pid, count);

			ids[y][row] = curr_id;
			been_placed.insert(curr_id);
		}
	}

	// gets a specified side, from x,y coords
	inline uint16_t get_side_xy(int x, int y, int loc)
	{
		return get_side(tile_grid[y][x], loc);
	}

	// gets a side from a tile
	uint16_t get_side(tile& t, int loc)
	{
		switch (loc)
		{
			case 0: // top
			{
				return t.rows[0];
			}
			case 1: // right
			{
				uint16_t res = 0;
				for (int i = 0; i < 10; i++)
				{
					res <<= 1;
					res |= t.rows[i] & 1;
				}
				return res;
			}
			case 2: // bottom
			{
				return t.rows[9];
			}
			case 3: // left
			{
				uint16_t res = 0;
				for (int i = 0; i < 10; i++)
				{
					res |= ((t.rows[i] >> 9) & 1) << (9 - i);
				}
				return res;
			}
		}
		return 0;
	}

	// rotates a tile to fit
	void rotate_to_fit(int cid, uint16_t side, int loc)
	{
		tile& t = tiles[cid];

		while (get_side(t, loc) != side && get_side(t, loc) != tile::reverse(side))
		{
			t.rotate();
		}
		if (get_side(t, loc) == side)
		{
			return;
		}
		else if (loc == 0 || loc == 2)
		{
			t.flip(1);
		}
		else if (loc == 1 || loc == 3)
		{
			t.flip(0);
		}
	}

	void fill_tiles()
	{
		int c1 = c_id[2][0];

		auto c1_adj = get_adj(c1);

		// top left
		ids[0][0] = c1;
		been_placed.insert(c1);

		// top row
		fill_row(1, 11, 0, 3);

		// top right
		int pid = ids[0][10];
		auto adj = get_adj(pid);
		ids[0][11] = get_next(adj, pid, 2);
		been_placed.insert(ids[0][11]);

		// left col
		fill_col(1, 11, 0, 3);

		// bottom left
		pid = ids[10][0];
		adj = get_adj(pid);
		ids[11][0] = get_next(adj, pid, 2);
		been_placed.insert(ids[11][0]);

		// bottom row
		fill_row(1, 11, 11, 3);

		// right col
		fill_col(1, 11, 11, 3);

		// bottom right
		pid = ids[11][10];
		adj = get_adj(pid);
		ids[11][11] = get_next(adj, pid, 2);
		been_placed.insert(ids[11][11]);

		// fill guts
		for (int y = 1; y < 11; y++)
		{
			for (int x = 1; x < 11; x++)
			{
				int pid1 = ids[y - 1][x];
				int pid2 = ids[y][x - 1];

				auto adj1 = get_adj(pid1);
				auto adj2 = get_adj(pid2);

				int n_id;

				for (auto& ad1 : adj1)
				{
					for (auto& ad2 : adj2)
					{
						int nv1 = ad1.get_other(pid1);
						int nv2 = ad2.get_other(pid2);
						if (nv1 == nv2)
						{
							auto f = been_placed.find(nv1);
							if (f == been_placed.end())
							{
								n_id = nv1;
								goto found;
							}
						}
					}
				}
				continue;
			found:
				ids[y][x] = n_id;
				been_placed.insert(n_id);
			}
		}
	}

	void rotate_tiles()
	{
		// rotate first tile
		auto& t = tiles[ids[0][0]];
		int cid = ids[0][0];
		int tid = ids[0][1];

		auto all_adj = get_adj(cid);
		auto& adj_side = *find_if(all_adj.begin(), all_adj.end(), [&](const tile_match_type& a)
		{
			if (tid == a.m_k1 || tid == a.m_k2)
			{
				return true;
			}
			return false;
		});

		auto& tar_side = adj_side.m_side1;

		while (get_side(t, 1) != adj_side.m_side1 && get_side(t, 1) != adj_side.m_side2)
		{
			t.rotate();
		}

		auto f = all_sides.find(get_side(t, 2));
		if (f == all_sides.end())
		{
			t.flip(0);
		}

		tile_grid[0][0] = t;

		// top row
		for (int x = 1; x < 12; x++)
		{
			cid = ids[0][x];

			auto side = get_side_xy(x - 1, 0, 1);

			rotate_to_fit(cid, side, 3);

			tile_grid[0][x] = tiles[cid];
		}

		// left col
		for (int y = 1; y < 12; y++)
		{
			cid = ids[y][0];

			auto side = get_side_xy(0, y - 1, 2);

			rotate_to_fit(cid, side, 0);

			tile_grid[y][0] = tiles[cid];
		}

		// rotate guts
		for (int y = 1; y < 12; y++)
		{
			for (int x = 1; x < 12; x++)
			{
				cid = ids[y][x];

				auto side = get_side_xy(x, y - 1, 2);

				rotate_to_fit(cid, side, 0);

				tile_grid[y][x] = tiles[cid];
			}
		}
	}

	void create_grid()
	{
		// loop over every tile
		// remove the outer border so tile becomes 8x8
		// add tile to final grid
		for (int y = 0; y < 12; y++)
		{
			// use x=0 as right most tile
			for (int x = 0; x < 12; x++)
			{
				// get tile stored as left index using right index x: (11,10,9,8,7,6,5,4,3,2,1,0) => (0,1,2,3,4,5,6,7,8,9,10,11)
				auto& t = tile_grid[y][11 - x];

				// g: x-index = x*8 >> 5 == (x << 3) >> 5 == x >> 2
				int x_index = x >> 2;
				// g: x-offset = x & 0b11
				uint32_t x_offset = x & 0b11;

				// loop over the inner 8 rows
				for (int r = 1; r < 9; r++)
				{
					// g: y-index = y*8 + r - 1
					int y_index = y * 8 + r - 1;

					// fixed row value
					uint32_t fixed_row = (t.rows[r] >> 1) & 0b011111111;

					g[y_index][x_index] |= fixed_row << (x_offset * 8);
				}
			}
		}
	}

	int find_sea_monsters()
	{
		int max_sea_monsters = 0;

		// find horizontal sea monsters
		for (auto& sm : horizontal_sm)
		{
			int sm_count = 0;
			for (int y = 0; y < 96 - 2; y++)
			{
				// x=0 is right indexed
				for (int x = 19; x < 96; x++)
				{
					int x_index = x >> 5; // x / 32
					int x_offset = x & 0b11111; // x % 32

					if (x_index == 0 || x_offset >= 19)
					{
						int match1 = g[y][x_index] & (sm[0] << (x_offset - 19));
						int match2 = g[y + 1][x_index] & (sm[1] << (x_offset - 19));
						int match3 = g[y + 2][x_index] & (sm[2] << (x_offset - 19));

						int count = _mm_popcnt_u32(match1) + _mm_popcnt_u32(match2) + _mm_popcnt_u32(match3);

						if (count == 15)
						{
							sm_count++;
						}
					}
					else
					{
						int match1_p1 = g[y][x_index] & (sm[0] >> (19 - x_offset));
						int match2_p1 = g[y + 1][x_index] & (sm[1] >> (19 - x_offset));
						int match3_p1 = g[y + 2][x_index] & (sm[2] >> (19 - x_offset));

						int match1_p2 = g[y][x_index - 1] & (sm[0] << (13 + x_offset));
						int match2_p2 = g[y + 1][x_index - 1] & (sm[1] << (13 + x_offset));
						int match3_p2 = g[y + 2][x_index - 1] & (sm[2] << (13 + x_offset));

						int count = _mm_popcnt_u32(match1_p1) + _mm_popcnt_u32(match2_p1) + _mm_popcnt_u32(match3_p1);
						count += _mm_popcnt_u32(match1_p2) + _mm_popcnt_u32(match2_p2) + _mm_popcnt_u32(match3_p2);

						if (count == 15)
						{
							sm_count++;
						}
					}
				}
			}
			max_sea_monsters = max(max_sea_monsters, sm_count);
		}

		// find vertical sea monsters
		for (auto& sm : vertical_sm)
		{
			int sm_count = 0;
			for (int y = 0; y < 96 - 19; y++)
			{
				// x=0 is right indexed
				for (int x = 2; x < 96; x++)
				{
					int x_index = x >> 5; // x / 32
					int x_offset = x & 0b11111; // x % 32

					if (x_index == 0 || x_offset >= 2)
					{
						int count = 0;
						for (int i = 0; i < 20; i++)
						{
							int match = g[y + i][x_index] & (sm[i] << (x_offset - 2));
							count += _mm_popcnt_u32(match);
						}

						if (count == 15)
						{
							sm_count++;
						}
					}
					else
					{
						int count = 0;

						for (int i = 0; i < 20; i++)
						{
							int match_p1 = g[y + i][x_index] & (sm[i] >> (2 - x_offset));
							int match_p2 = g[y + i][x_index - 1] & (sm[i] << (30 + x_offset));
							count += _mm_popcnt_u64(match_p1) + _mm_popcnt_u32(match_p2);
						}

						if (count == 15)
						{
							sm_count++;
						}
					}
				}
			}
			max_sea_monsters = max(max_sea_monsters, sm_count);
		}

		return max_sea_monsters;
	}

	long long part2()
	{
		fill_tiles();

		rotate_tiles();

		create_grid();

		int sea_monsters = find_sea_monsters();

		int total_sea_monster_spaces = sea_monsters * 15;

		int total_spaces = 0;
		for (int y = 0; y < 96; y++)
		{
			total_spaces += _mm_popcnt_u32(g[y][0]) + _mm_popcnt_u32(g[y][1]) + _mm_popcnt_u32(g[y][2]);
		}

		int safe_spaces = total_spaces - total_sea_monster_spaces;

		return safe_spaces;
	}
};

class Day20 : public BaseDay
{
public:
	Day20() : BaseDay("20") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		grid grid_solve;

		// parse
		grid_solve.load_tiles(input);

		// part 1
		part1 = grid_solve.part1();

		// part 2
		part2 = grid_solve.part2();

		return { part1, part2 };
	}
};
