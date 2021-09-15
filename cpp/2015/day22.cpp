#include "../aocHelper.h"

class Day22 : public BaseDay
{
public:
	Day22() : BaseDay("22") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		class Player
		{
		public:
			int health;
			int damage;
			int armour;
			int mana;
			int spent;

			Player(int h, int d, int a, int m) : health(h), damage(d), armour(a), mana(m), spent(0) {}
		};

		enum class spell_type :int
		{
			magic_missile = 0,
			drain = 1,
			shield = 2,
			poison = 3,
			recharge = 4
		};

		struct spell_data
		{
			int cost;
			int damage;
			int health;
			int armour;
			int mana;
			int duration;
		};

		constexpr int spell_count = 5;

		static constexpr spell_data spells[spell_count] = {
			{53,  4, 0, 0, 0,   0}, // Magic Missle
			{73,  2, 2, 0, 0,   0}, // Drain
			{113, 0, 0, 7, 0,   6}, // Shield
			{173, 3, 0, 0, 0,   6}, // Poison
			{229, 0, 0, 0, 101, 5}  // Recharge
		};

		constexpr int min_spell_cost = (*min_element(spells, spells + spell_count, [](const spell_data& a, const spell_data& b)
		{
			return a.cost < b.cost;
		})).cost;

		class Effects
		{
		public:
			bool running[spell_count]{};
			int left[spell_count]{};

			void use(spell_type spell, Player& person, Player& boss)
			{
				person.mana -= spells[(int) spell].cost;
				person.spent += spells[(int) spell].cost;

				if (spell == spell_type::magic_missile)
				{
					boss.health -= spells[(int) spell].damage; // does damage
				}
				else if (spell == spell_type::drain)
				{
					boss.health -= spells[(int) spell].damage; // does damage
					person.health += spells[(int) spell].health; // heals
				}
				else
				{
					running[(int) spell] = true;
					left[(int) spell] = spells[(int) spell].duration;
				}
			}

			void tick(Player& person, Player& boss)
			{
				for (int i = 0; i < spell_count; i++)
				{
					if (running[i])
					{
						if ((spell_type) i == spell_type::shield)
						{
							person.armour = spells[(int) spell_type::shield].armour; // increase armour
						}
						if ((spell_type) i == spell_type::poison)
						{
							boss.health -= spells[(int) spell_type::poison].damage; // does damage
						}
						if ((spell_type) i == spell_type::recharge)
						{
							person.mana += spells[(int) spell_type::recharge].mana; // increase mana
						}

						left[i]--;
						if (left[i] == 0)
						{
							if ((spell_type) i == spell_type::shield)
							{
								person.armour = 0;
							}
							running[i] = false;
						}
					}
				}
			}
		};

		int min_mana = 100'000'000;

		function<int(Player&, Player&, Effects&, bool)> get_min_mana;
		get_min_mana = [&get_min_mana, &min_mana](Player& person, Player& boss, Effects& effects, bool hardmode)
		{
			if (person.spent >= min_mana)
			{
				return min_mana;
			}

			// handle player
			if (hardmode)
			{
				person.health--;
				if (person.health <= 0)
				{
					return min_mana; // lost
				}
			}

			effects.tick(person, boss);

			// check boss health
			if (boss.health <= 0)
			{
				return person.spent; // won
			}

			// can't afford any spells
			if (person.mana < min_spell_cost)
			{
				return min_mana; // lost
			}

			// recursively choose spells
			for (int i = spell_count - 1; i >= 0; i--)
			{
				auto spell = (spell_type) i;
				auto& stats = spells[i];

				if (person.mana >= stats.cost && !effects.running[(int) spell]) // can afford spall, and spell not running

				{
					// copy player, boss, effects
					Player p{ person };
					Player b{ boss };
					Effects e{ effects };

					// buy spell
					e.use(spell, p, b);

					if (p.spent >= min_mana)
					{
						continue;
					}

					// handle boss
					e.tick(p, b);

					// check boss health
					if (b.health <= 0)
					{
						min_mana = min(min_mana, p.spent);
						continue; // won
					}

					// do boss damage
					int b_damage = (b.damage > p.armour) ? (b.damage - p.armour) : 1;
					p.health -= b_damage;

					// check person health
					if (p.health <= 0)
					{
						continue; // lost
					}

					// get min_mana from next turn, only if person won
					int mana = get_min_mana(p, b, e, hardmode);
					min_mana = min(min_mana, mana);
				}
			}

			return min_mana;
		};

		// parse input
		input += 12; // skip 'Hit Points: '

		int boss_health = numericParse<int>(input);

		input += 9; // skip '\nDamage: '

		int boss_damage = numericParse<int>(input);

		Player boss_og{ boss_health, boss_damage, 0, 0 };

		Player person_og{ 50, 0, 0, 500 };

		// part 1
		Player person{ person_og };
		Player boss{ boss_og };
		Effects effects{};

		part1 = get_min_mana(person, boss, effects, false);

		// part 2
		min_mana = 100'000'000;
		person = Player{ person_og };
		boss = Player{ boss_og };
		effects = Effects{};

		part2 = get_min_mana(person, boss, effects, true);

		return { part1, part2 };
	}
};
