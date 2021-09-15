#include "../aocHelper.h"



class Day21 : public BaseDay
{
public:
	Day21() : BaseDay("21") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct item
		{
			uint8_t id;
			uint8_t cost;
			uint8_t damage;
			uint8_t armour;
		};

		static constexpr array<item, 5> weapons = { {
			{0, 8,  4, 0}, // Dagger
			{1, 10, 5, 0}, // Shortsword
			{2, 25, 6, 0}, // Warhammer
			{3, 40, 7, 0}, // Longsword
			{4, 74, 8, 0}  // Greataxe
		} };

		static constexpr array<item, 6> armour = { {
			{5,  0,   0, 0}, // None
			{6,  13,  0, 1}, // Leather
			{7,  31,  0, 2}, // Chainmail
			{8,  53,  0, 3}, // Splintmail
			{9,  75,  0, 4}, // Blademail
			{10, 102, 0, 5}  // Platemail
		} };

		static constexpr array<item, 8> rings = { {
			{11, 0,   0, 0}, // None 1
			{12, 0,   0, 0}, // None 2
			{13, 25,  1, 0}, // Damage +1
			{14, 50,  2, 0}, // Damage +2
			{15, 100, 3, 0}, // Damage +3
			{16, 20,  0, 1}, // Defense +1
			{17, 40,  0, 2}, // Defense +2
			{18, 80,  0, 3}  // Defense +3
		} };

		static_assert(rings[4].cost == 100);

		auto cartesian_product = []() constexpr
		{
			constexpr int size = weapons.size() * armour.size() * rings.size() * rings.size();
			array<array<item, 4>, size> arr{};

			int i = 0;

			for (int a = 0; a < weapons.size(); a++)
			{
				for (int b = 0; b < armour.size(); b++)
				{
					for (int c = 0; c < rings.size(); c++)
					{
						for (int d = 0; d < rings.size(); d++)
						{
							arr[i] = { weapons[a], armour[b], rings[c], rings[d] };
							i++;
						}
					}
				}
			}

			return arr;
		};

		static constexpr auto prod = cartesian_product();

		static_assert(prod[0][0].cost == 8 && prod[0][1].cost == 0);

		struct person
		{
			int health;
			int damage;
			int armour;
		};

		auto calc_gold = [](person player, person boss, int const& (*cmp)(int const&, int const&), int starting_value, bool win)
		{
			int gold = starting_value;

			for (auto& p : prod)
			{
				if (p[2].id == p[3].id)
				{
					continue;
				}

				int cost = accumulate(p.begin(), p.end(), 0, [](int a, item b) { return a + b.cost; });

				int damage = accumulate(p.begin(), p.end(), 0, [](int a, item b) { return a + b.damage; }) - boss.armour;
				if (damage < 1)
				{
					damage = 1;
				}

				int protection = accumulate(p.begin(), p.end(), 0, [](int a, item b) { return a + b.armour; });

				int boss_dmg = boss.damage - protection;
				if (boss_dmg < 1)
				{
					boss_dmg = 1;
				}

				int win_turns = boss.health / damage;
				if (boss.health % damage == 0)
				{
					win_turns++;
				}

				int loss_turns = player.health / boss_dmg;
				if (player.health % boss_dmg == 0)
				{
					loss_turns++;
				}

				if ((win && win_turns <= loss_turns) || (!win && loss_turns < win_turns))
				{
					gold = cmp(gold, cost);
				}
			}

			return gold;
		};

		person player = { 100, 0, 0 };

		// parse input
		person boss;

		input += 12; // skip 'Hit Points: '

		boss.health = numericParse<int>(input);

		input += 9; // skip '\nDamage: '

		boss.damage = numericParse<int>(input);

		input += 8; // skip '\nArmor: '

		boss.armour = numericParse<int>(input);

		// part 1
		part1 = calc_gold(player, boss, min<int>, 100'000'000, true);

		// part 2
		part2 = calc_gold(player, boss, max<int>, 0, false);

		return { part1, part2 };
	}
};
