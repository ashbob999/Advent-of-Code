#include "../aocHelper.h"

class Day20 : public BaseDay
{
public:
	Day20() : BaseDay("20") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		using particle = array<array<int, 3>, 3>;

		vector<particle> particles;

		// parse input
		while (*input != '\0')
		{
			particle p;

			input += 3; // skip "p=<"

			p[0][0] = numericParse<int>(input);
			input++; // skip ','
			p[0][1] = numericParse<int>(input);
			input++; // skip ','
			p[0][2] = numericParse<int>(input);

			input += 6; // skip ">, v=<"

			p[1][0] = numericParse<int>(input);
			input++; // skip ','
			p[1][1] = numericParse<int>(input);
			input++; // skip ','
			p[1][2] = numericParse<int>(input);

			input += 6; // skip ">, v=<"

			p[2][0] = numericParse<int>(input);
			input++; // skip ','
			p[2][1] = numericParse<int>(input);
			input++; // skip ','
			p[2][2] = numericParse<int>(input);

			input++; // skip '>'

			particles.push_back(p);

			input++; // skip '\n'
		}

		auto tick = [](vector<particle>& particles)
		{
			for (auto& p : particles)
			{
				for (int i = 0; i < 3; i++)
				{
					p[1][i] += p[2][i]; // update velocity
					p[0][i] += p[1][i]; // update position
				}
			}
		};

		// part 1
		vector<particle> p1_particles = particles;
		sort(p1_particles.begin(), p1_particles.end(), [](const particle& a, const particle& b)
		{
			int a_acc = abs(a[2][0]) + abs(a[2][1]) + abs(a[2][2]);
			int b_acc = abs(b[2][0]) + abs(b[2][1]) + abs(b[2][2]);

			if (a_acc == b_acc)
			{
				int a_vel = abs(a[1][0]) + abs(a[1][1]) + abs(a[1][2]);
				int b_vel = abs(b[1][0]) + abs(b[1][1]) + abs(b[1][2]);

				if (a_vel == b_vel)
				{
					int a_pos = abs(a[0][0]) + abs(a[0][1]) + abs(a[0][2]);
					int b_pos = abs(b[0][0]) + abs(b[0][1]) + abs(b[0][2]);

					return a_pos < b_pos;
				}
				else
				{
					return a_vel < b_vel;
				}
			}
			else
			{
				return a_acc < b_acc;
			}
		});

		for (int i = 0; i < particles.size(); i++)
		{
			if (particles[i] == p1_particles[0])
			{
				part1 = i;
				break;
			}
		}

		// part 2
		vector<particle> p2_particles = particles;

		int last_count = 0;
		int check_every = 100;

		while (true)
		{
			tick(p2_particles);

			vector<particle> new_particles;
			for (int i = 0; i < p2_particles.size(); i++)
			{
				bool collided = false;

				for (int j = 0; j < p2_particles.size(); j++)
				{
					if (i == j)
					{
						continue;
					}

					if (p2_particles[i][0] == p2_particles[j][0])
					{
						collided = true;
						break;
					}
				}

				if (!collided)
				{
					new_particles.push_back(p2_particles[i]);
				}
			}

			p2_particles = new_particles;

			if (part2 % check_every == 0)
			{
				if (last_count == new_particles.size() && last_count < particles.size())
				{
					part2 = last_count;
					break;
				}
			}

			last_count = p2_particles.size();
			part2++;
		}

		return { part1, part2 };
	}
};
