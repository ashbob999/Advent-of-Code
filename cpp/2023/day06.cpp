#include "../aocHelper.h"

class Day06 : public BaseDay
{
public:
	Day06() : BaseDay("06") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr int Count = 4;

		std::array<double, Count> times;
		std::array<double, Count> distances;

		// parse input

		input += 5; // skip 'Time:'

		for (int i = 0; i < Count; i++)
		{
			input++;
			uint32_t time = numericParseWithLeadingSpaces<uint32_t>(input);
			times[i] = static_cast<double>(time);
		}

		input++; // skip '\n'

		input += 7; // skip 'Distance:'

		for (int i = 0; i < Count; i++)
		{
			input++;
			uint32_t distance = numericParseWithLeadingSpaces<uint32_t>(input);
			distances[i] = static_cast<double>(distance);
		}

		/*while (*input != '\n')
		{
			input++;
			uint32_t distance = numericParseWithLeadingSpaces<uint32_t>(input);
			distances.push_back(distance);
		}*/

		/*
		y: distance
		x: time passed

		y = x * (total_time - x)


		max_dist < total_time * x - x*x
		max_dist = total_time * x - x*x
		0 = total_time * x - x*x - max_dist

		solve quadratic
		*/

		const auto solve_quadratic = [](double a, double b, double c) -> std::array<double, 2>
		{
			const double det = std::sqrt(b * b - 4.000000001 * a * c);
			const double den = 2 * a;

			double x1 = (-b + det) / den;
			double x2 = (-b - det) / den;

			return {x1, x2};
		};

// part 1
#if 1
		part1 = 1;
		for (int i = 0; i < Count; i++)
		{
			auto&& time = times[i];
			auto&& dist = distances[i];
			// continue;
			auto x_vals = solve_quadratic(-1, time, -static_cast<double>(dist));
			int64_t v1 = static_cast<int64_t>(std::ceil(x_vals[0]));
			int64_t v2 = static_cast<int64_t>(std::floor(x_vals[1]));

			int64_t wins = v2 - v1 + 1;

			if (wins > 0 && true)
			{
				part1 *= wins;
			}
		}
#else

		// use simd
		{
			/*
			Reformat quadratic equation
			x = (-b +- sqrt(b*b - 4ac)) / 2a
			det = sqrt(b*b - 4ac)
			den = 2a
			x1 = (-b + det) / den
			x2 = (-b - det) / den

			a = -1
			b = time
			c = - dist

			det = sqrt(time*time - 4 * -1 * -dist)
				= sqrt(time*time + (-4 * -1 * -dist))
				= sqrt(time*time + (4 * - dist))
				= sqrt(time*time - (4 * dist))

			den = -2 * -1
				= -2

			x1 = (-time + det) / den
			x2 = (-time - det) / den

			x1 = (-1*time + 1*det) / den   # * -1
			   = -1*(-1*time + 1*det) / -den
			   = (1*time + -1*det) / -den
			   = (time - det) / -den
			   = (time - det) / -(-2)
			   = (time - det) / 2
			   = time/2 - det/2

			x2 = (-1*time - 1*det) / den
			   = (-1*time + -1*det) / den   # * -1
			   = -1*(-1*time + -1*det) / -den
			   = (1*time + 1*det) / -den
			   = (time + det) / -den
			   = (time + det) / -(-2)
			   = (time + det) / 2
			   = time/2 + det/2

			det = sqrt(time*time - (4 * dist))
			den = -2
			x1 = time/2 - det/2
			x2 = time/2 + det/2

			*/

			// load the times & distances
			const __m256d time = _mm256_loadu_pd(times.data());
			const __m256d distance = _mm256_loadu_pd(distances.data());

			// load const value 2
			const __m256d value_2 = _mm256_set1_pd(2);

			// load const value 4
			const __m256d value_4 = _mm256_set1_pd(4.000000001);

			// calculate time*time
			const __m256d time_squared = _mm256_mul_pd(time, time);

			// calculate det
			const __m256d det = _mm256_sqrt_pd(_mm256_sub_pd(time_squared, _mm256_mul_pd(value_4, distance)));

			// calculate time/2
			const __m256d time_halved = _mm256_div_pd(time, value_2);

			// calculate det/2
			const __m256d det_halved = _mm256_div_pd(det, value_2);

			// calculate x1 = time/2 - det/2
			const __m256d x1 = _mm256_sub_pd(time_halved, det_halved);

			// calculate x2 = time/2 + det/2
			const __m256d x2 = _mm256_add_pd(time_halved, det_halved);

			__m128i v1 = _mm256_cvttpd_epi32(_mm256_ceil_pd(x1));
			__m128i v2 = _mm256_cvttpd_epi32(_mm256_floor_pd(x2));

			// wins = v2 - v1 + 1
			__m128i wins = _mm_add_epi32(_mm_sub_epi32(v2, v1), _mm_set1_epi32(1));

			// wins > 0
			__m128i mults = _mm_max_epi32(wins, _mm_set1_epi32(1));

			// (a, b, c, d)x32 * (d, c, b, a)x32 = (ad, bc)x64
			//__m128i res = _mm_mul_epi32(mults, _mm_shuffle_epi32(mults, 0b00'01'10'11));
			__m128i res = _mm_mul_epi32(wins, _mm_shuffle_epi32(wins, 0b00'01'10'11));

			int64_t res_low = _mm_extract_epi64(res, 0);
			int64_t res_high = _mm_extract_epi64(res, 1);
			part1 = res_low * res_high;
		}
#endif

		// part 2

		// reset the input and parse again
		input = this->input_data.get();

		uint64_t time = 0;
		uint64_t distance = 0;

		input += 5; // skip 'Time:'
		while (*input != '\n')
		{
			if (*input != ' ')
			{
				time = time * 10 + (*input - '0');
			}

			input++;
		}

		input++; // skip '\n'

		input += 9; // skip 'Distance:'
		while (*input != '\n')
		{
			if (*input != ' ')
			{
				distance = distance * 10 + (*input - '0');
			}

			input++;
		}

		auto x_vals = solve_quadratic(-1, time, -static_cast<double>(distance));
		int64_t v1 = static_cast<int64_t>(std::ceil(x_vals[0]));
		int64_t v2 = static_cast<int64_t>(std::floor(x_vals[1]));

		int64_t wins = v2 - v1 + 1;

		part2 = wins;

		return {part1, part2};
	}
};
