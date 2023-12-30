#include "../aocHelper.h"
// modify z3 cmakelists.txt to fix pyenv issues
// set(PYTHON_EXECUTABLE %userprofile%/.pyenv/pyenv-win/versions/3.8.3/python.exe)
#include <z3++.h>

#include <cassert>
#include <immintrin.h>

namespace
{
	using PositionT = int64_t;
	using VelocityT = int64_t;

	struct Hailstone
	{
		PositionT x{};
		PositionT y{};
		PositionT z{};

		VelocityT vx{};
		VelocityT vy{};
		VelocityT vz{};

		double m{0};
		double c{0};
	};

	template<typename T>
	int sgn(T val)
	{
		return (T(0) < val) - (val < T(0));
	}

	inline __m256d int64_to_double(__m256i values)
	{
		values = _mm256_add_epi64(values, _mm256_castpd_si256(_mm256_set1_pd(0x0018000000000000)));
		return _mm256_sub_pd(_mm256_castsi256_pd(values), _mm256_set1_pd(0x0018000000000000));
	}

	std::array<int64_t, 3> solve_part2_z3(const Hailstone& h1, const Hailstone& h2, const Hailstone& h3)
	{
		z3::context ctx{};

		z3::expr x = ctx.int_const("x");
		z3::expr y = ctx.int_const("y");
		z3::expr z = ctx.int_const("z");

		z3::expr vx = ctx.int_const("vx");
		z3::expr vy = ctx.int_const("vy");
		z3::expr vz = ctx.int_const("vz");

		z3::expr t0 = ctx.int_const("t0");
		z3::expr t1 = ctx.int_const("t1");
		z3::expr t2 = ctx.int_const("t2");

		z3::solver solver{ctx};

		solver.add(ctx.int_val(h1.x) + ctx.int_val(h1.vx) * t0 == x + vx * t0);
		solver.add(ctx.int_val(h1.y) + ctx.int_val(h1.vy) * t0 == y + vy * t0);
		solver.add(ctx.int_val(h1.z) + ctx.int_val(h1.vz) * t0 == z + vz * t0);

		solver.add(ctx.int_val(h2.x) + ctx.int_val(h2.vx) * t1 == x + vx * t1);
		solver.add(ctx.int_val(h2.y) + ctx.int_val(h2.vy) * t1 == y + vy * t1);
		solver.add(ctx.int_val(h2.z) + ctx.int_val(h2.vz) * t1 == z + vz * t1);

		solver.add(ctx.int_val(h3.x) + ctx.int_val(h3.vx) * t2 == x + vx * t2);
		solver.add(ctx.int_val(h3.y) + ctx.int_val(h3.vy) * t2 == y + vy * t2);
		solver.add(ctx.int_val(h3.z) + ctx.int_val(h3.vz) * t2 == z + vz * t2);

		if (solver.check() != z3::sat)
		{
			assert(false && "Solver equations invalid");
		}

		auto&& model = solver.get_model();

		int64_t rx = model.eval(x).as_int64();
		int64_t ry = model.eval(y).as_int64();
		int64_t rz = model.eval(z).as_int64();

		return {rx, ry, rz};
		return {0, 0, 0};
	}
}

class Day24 : public BaseDay
{
public:
	Day24() : BaseDay("24") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<Hailstone> hailstones;
		hailstones.reserve(300);

		while (*input != '\0')
		{
			PositionT x = parse_int64_fast(input);
			input += 2; // skip ', '
			PositionT y = parse_int64_fast(input);
			input += 2; // skip ', '
			PositionT z = parse_int64_fast(input);

			input += 3; // skip ' @ '

			VelocityT vx = parse_int64_fast(input);
			input += 2; // skip ', '
			VelocityT vy = parse_int64_fast(input);
			input += 2; // skip ', '
			VelocityT vz = parse_int64_fast(input);

			input++; // skip '\n'

			/*
			Calculate the 2d gradient and y-intercept
			px, py
			vx, vy

			y = mx + c
			m = vy / vx
			c = py - m * px
			*/
			double m = static_cast<double>(vy) / static_cast<double>(vx);
			double c = y - m * x;

			Hailstone hailstone{x, y, z, vx, vy, vz, m, c};
			hailstones.push_back(std::move(hailstone));
		}

		//  part 1

		constexpr int Count = 256 / 8 / sizeof(double);

		constexpr int64_t MinArea = 200000000000000;
		constexpr int64_t MaxArea = 400000000000000;

		const auto future = [](const Hailstone& h1, const Hailstone& h2, const std::pair<double, double> pos) -> bool
		{
			return (sgn(h1.vx) == sgn(pos.first - h1.x)) && (sgn(h1.vy) == sgn(pos.second - h1.y)) &&
				(sgn(h2.vx) == sgn(pos.first - h2.x)) && (sgn(h2.vy) == sgn(pos.second - h2.y));
		};

		const auto collide = [](const Hailstone& h1, const Hailstone& h2) -> std::pair<double, double>
		{
			/*
			y = ax + c
			y = bx + d
			ax - bx =  d - c

			x = (d - c) / (a - b)
			y = a * x + c
			y = a * (d - c) / (a - b) + c
			*/
			auto&& a = h1.m;
			auto&& c = h1.c;

			auto&& b = h2.m;
			auto&& d = h2.c;

			if (a == b)
			{
				return {std::numeric_limits<double>::infinity(), std::numeric_limits<double>::infinity()};
			}

			double x = (d - c) / (a - b);
			double y = a * x + c;

			return {x, y};
		};

		const __m256d min_area = _mm256_set1_pd(MinArea);
		const __m256d max_area = _mm256_set1_pd(MaxArea);

		constexpr int hailstone_value_size = sizeof(decltype(hailstones)::value_type);
		const __m128i hailstone_offsets = _mm_setr_epi32(
			0 * hailstone_value_size,
			1 * hailstone_value_size,
			2 * hailstone_value_size,
			3 * hailstone_value_size);

		const __m256d signbit = _mm256_set1_pd(-0.0);

		for (int i = 0; i < hailstones.size(); i++)
		{
			auto&& h1 = hailstones[i];

			// load gradient of e1
			const __m256d a = _mm256_set1_pd(h1.m);
			// load y-intercept of e1
			const __m256d c = _mm256_set1_pd(h1.c);

			// load x value
			const __m256d h1_x = _mm256_set1_pd(h1.x);

			// load y value
			const __m256d h1_y = _mm256_set1_pd(h1.y);

			// load velocity
			const __m256d h1_vx = _mm256_set1_pd(h1.vx);
			const __m256d h1_vy = _mm256_set1_pd(h1.vy);

			// get sign of velocity
			const __m256d h1_vx_sign = _mm256_and_pd(h1_vx, signbit);
			const __m256d h1_vy_sign = _mm256_and_pd(h1_vy, signbit);

			int j = i + 1;
			for (; j <= hailstones.size() - Count; j += Count)
			{
				// load mulitple gradient values
				__m256d b = _mm256_i32gather_pd(&hailstones[j].m, hailstone_offsets, 1);

				// load multiple y-intercept values
				__m256d d = _mm256_i32gather_pd(&hailstones[j].c, hailstone_offsets, 1);

				// calculate a-b
				__m256d a_sub_b = _mm256_sub_pd(a, b);

				// calculate d - c
				__m256d d_sub_c = _mm256_sub_pd(d, c);

				// calculate x values (d-c) / (a-b)
				__m256d x = _mm256_div_pd(d_sub_c, a_sub_b);

				// calculate y values a*x + c
				__m256d y = _mm256_fmadd_pd(a, x, c);

				// check intersection is in the future

				// load multiple x values
				__m256d x_values = int64_to_double(_mm256_i32gather_epi64(&hailstones[j].x, hailstone_offsets, 1));

				// load multiple y values
				__m256d y_values = int64_to_double(_mm256_i32gather_epi64(&hailstones[j].y, hailstone_offsets, 1));

				// load multiple vx values
				__m256d vx_values = int64_to_double(_mm256_i32gather_epi64(&hailstones[j].vx, hailstone_offsets, 1));

				// load multiple vy values
				__m256d vy_values = int64_to_double(_mm256_i32gather_epi64(&hailstones[j].vy, hailstone_offsets, 1));

				// calculate the sign values
				__m256d h1_x_diff_sign = _mm256_and_pd(_mm256_sub_pd(x, h1_x), signbit);
				__m256d h1_y_diff_sign = _mm256_and_pd(_mm256_sub_pd(y, h1_y), signbit);
				__m256d vx_sign = _mm256_and_pd(vx_values, signbit);
				__m256d vy_sign = _mm256_and_pd(vy_values, signbit);
				__m256d x_diff_sign = _mm256_and_pd(_mm256_sub_pd(x, x_values), signbit);
				__m256d y_diff_sign = _mm256_and_pd(_mm256_sub_pd(y, y_values), signbit);

				// check sign values are the same
				// cast to __m256i then bit cmp then cast back to __m256d then movemask
				int sign_h1_x_mask = _mm256_movemask_pd(_mm256_castsi256_pd(
					_mm256_cmpeq_epi64(_mm256_castpd_si256(h1_vx_sign), _mm256_castpd_si256(h1_x_diff_sign))));
				int sign_h1_y_mask = _mm256_movemask_pd(_mm256_castsi256_pd(
					_mm256_cmpeq_epi64(_mm256_castpd_si256(h1_vy_sign), _mm256_castpd_si256(h1_y_diff_sign))));
				int sign_x_mask = _mm256_movemask_pd(_mm256_castsi256_pd(
					_mm256_cmpeq_epi64(_mm256_castpd_si256(vx_sign), _mm256_castpd_si256(x_diff_sign))));
				int sign_y_mask = _mm256_movemask_pd(_mm256_castsi256_pd(
					_mm256_cmpeq_epi64(_mm256_castpd_si256(vy_sign), _mm256_castpd_si256(y_diff_sign))));

				int sign_mask = sign_h1_x_mask & sign_h1_y_mask & sign_x_mask & sign_y_mask;

				// check for x range
				int x_mask_min = _mm256_movemask_pd(_mm256_cmp_pd(x, min_area, _CMP_NLT_UQ));
				int x_mask_max = _mm256_movemask_pd(_mm256_cmp_pd(x, max_area, _CMP_NGT_UQ));
				int x_mask = x_mask_min & x_mask_max;

				// check for y range
				int y_mask_min = _mm256_movemask_pd(_mm256_cmp_pd(y, min_area, _CMP_NLT_UQ));
				int y_mask_max = _mm256_movemask_pd(_mm256_cmp_pd(y, max_area, _CMP_NGT_UQ));
				int y_mask = y_mask_min & y_mask_max;

				int pos_mask = x_mask & y_mask;

				int mask = pos_mask & sign_mask;

				part1 += _mm_popcnt_u32(mask);
			}

			// fallback
			for (; j < hailstones.size(); j++)
			{
				auto r = collide(h1, hailstones[j]);
				if (future(h1, hailstones[j], r))
				{
					if (r.first >= MinArea && r.first <= MaxArea && r.second >= MinArea && r.second <= MaxArea)
					{
						part1++;
					}
				}
			}
		}

		// part 2

		auto&& result = solve_part2_z3(hailstones[0], hailstones[1], hailstones[2]);
		part2 = result[0] + result[1] + result[2];

		return {part1, part2};
	}
};
