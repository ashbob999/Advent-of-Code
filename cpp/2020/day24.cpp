#include "../aocHelper.h"

#include <immintrin.h>

class Day24 : public BaseDay
{
public:
	Day24() : BaseDay("24") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// pack x,y into uint32_t (16 bits each because there is no intrinsic to add 32 packed ints)
		// pack: ((int32_t) x & 0xffff) << 16;
		// unpack: (v >> 16) & 0xffff
		unordered_map<uint32_t, int> tiles;

		// parse
		while (*input != '\0')
		{
			int16_t x = 0;
			int16_t y = 0;

			while (*input != '\n')
			{
				if (*input == 'e')
				{
					x += 2;
					input++;
				}
				else if (*input == 'w')
				{
					x -= 2;
					input++;
				}
				else if (*input == 's')
				{
					y += 1;
					input++;

					if (*input == 'e')
					{
						x += 1;
					}
					else if (*input == 'w')
					{
						x -= 1;
					}
					input++;
				}
				else if (*input == 'n')
				{
					y -= 1;
					input++;

					if (*input == 'e')
					{
						x += 1;
					}
					else if (*input == 'w')
					{
						x -= 1;
					}
					input++;
				}
			}
			input++; // skip newline

			uint32_t pos = 0;
			pos |= ((int32_t) y & 0xffff) << 0;
			pos |= ((int32_t) x & 0xffff) << 16;

			auto f = tiles.find(pos);
			if (f != tiles.end())
			{
				tiles[pos] ^= 1;
			}
			else
			{
				tiles[pos] = 1;
			}
		}

		// part 1
		for (auto& p : tiles)
		{
			if (p.second == 1)
			{
				part1++;
			}
		}

		// part 2

		__m128i adj[6] = { _mm_set_epi16(0, 0, 0, 0, 0, 0, -2,  0),
						   _mm_set_epi16(0, 0, 0, 0, 0, 0,  2,  0),
						   _mm_set_epi16(0, 0, 0, 0, 0, 0, -1, -1),
						   _mm_set_epi16(0, 0, 0, 0, 0, 0,  1, -1),
						   _mm_set_epi16(0, 0, 0, 0, 0, 0, -1,  1),
						   _mm_set_epi16(0, 0, 0, 0, 0, 0,  1,  1)
		};

		for (int i = 0; i < 100; i++)
		{
			unordered_map<uint32_t, int> new_tiles(tiles);

			for (auto& p : tiles)
			{
				int32_t pos = 0;
				pos |= p.first;

				__m128i pos_128 = _mm_set_epi32(0, 0, 0, pos);

				if (p.second == 1)
				{
					for (auto& ad : adj)
					{
						__m128i adj_tile_128 = _mm_adds_epi16(pos_128, ad);
						uint32_t val = _mm_extract_epi32(adj_tile_128, 0);

						auto f = tiles.find(val);
						if (f == tiles.end())
						{
							new_tiles[val] = 0;
						}
					}
				}
			}


			unordered_map<uint32_t, int> new_tiles2(new_tiles);

			for (auto& p : new_tiles)
			{
				int32_t pos = 0;
				pos |= p.first;

				__m128i pos_128 = _mm_set_epi32(0, 0, 0, pos);

				int adj_count = 0;

				for (auto& ad : adj)
				{
					__m128i adj_tile_128 = _mm_adds_epi16(pos_128, ad);
					uint32_t val = _mm_extract_epi32(adj_tile_128, 0);

					auto f = tiles.find(val);
					if (f != tiles.end())
					{
						if (new_tiles[val] == 1)
						{
							adj_count++;
						}
					}
				}

				if (p.second == 1 && (adj_count == 0 || adj_count > 2))
				{
					new_tiles2[p.first] = 0;
				}

				if (p.second == 0 && adj_count == 2)
				{
					new_tiles2[p.first] = 1;
				}
			}

			tiles = move(new_tiles2);
		}

		for (auto& p : tiles)
		{
			if (p.second == 1)
			{
				part2++;
			}
		}

		return { part1, part2 };
	}
};
