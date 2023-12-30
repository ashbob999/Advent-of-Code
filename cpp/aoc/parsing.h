#pragma once

#include <immintrin.h>

template<typename T>
inline T numericParse(char*& p)
{
	bool have = false;
	T neg = 1;
	if (*p == '-')
	{
		neg = -1;
		p++;
	}
	else if (*p == '+')
	{
		neg = 1;
		p++;
	}
	T n = 0;
	for (; *p != '\0'; p++)
	{
		// cout << "n: " << n << " ";
		// cout << "char: " << *p << " ";
		T d = *p - '0';
		// cout << "digit: " << d << " ";
		if (d >= 0 && d <= 9)
		{
			n = 10 * n + d;
			have = true;
		}
		else if (have)
		{
			return n * neg;
		}
	}
	if (have)
	{
		return n * neg;
	}
	return 0;
}

namespace
{
	inline __m128i get_numeric_mask(__m128i chunk)
	{
		const __m128i wrap = _mm_set1_epi8(-128);
		const __m128i digit_upper_bound = _mm_add_epi8(wrap, _mm_set1_epi8(10));
		return _mm_cmplt_epi8(_mm_add_epi8(chunk, wrap), digit_upper_bound);
	}

	inline uint64_t get_digit_count_from_numeric_mask(__m128i mask)
	{
		auto condensed_mask = _mm_movemask_epi8(mask);
		// cannot use leading zeros, because digits can be present in the string that
		// are not part of the first numeric sequence
		return _tzcnt_u64(~condensed_mask);
	}

	inline __m128i shift_bytes_left_branchless(__m128i a, uint64_t num_bytes)
	{
		constexpr auto mask = static_cast<char>(-128);
		static constexpr char shift_shuffle_lookup[32]{mask, mask, mask, mask, mask, mask, mask, mask, mask, mask, mask,
													   mask, mask, mask, mask, mask, 0,	   1,	 2,	   3,	 4,	   5,
													   6,	 7,	   8,	 9,	   10,	 11,   12,	 13,   14,	 15};

		const char* lookup_center = shift_shuffle_lookup + 16;
		const __m128i shuffle = _mm_lddqu_si128(reinterpret_cast<const __m128i*>(lookup_center - num_bytes));
		return _mm_shuffle_epi8(a, shuffle);
	}
}

/*
	Fast parsing of a uint64 value, maximum 16 digits

	Copied from: https://github.com/KholdStare/qnd-integer-parsing-experiments
*/
inline uint64_t parse_uint64_fast(char*& data)
{
	__m128i chunk = _mm_loadu_si128(reinterpret_cast<__m128i*>(data));

	const __m128i zeros = _mm_set1_epi8('0');

	chunk = _mm_sub_epi8(chunk, zeros);

	const __m128i numeric_mask = get_numeric_mask(chunk);
	const uint64_t num_digits = get_digit_count_from_numeric_mask(numeric_mask);
	data += num_digits;
	const uint64_t num_non_digits = sizeof(chunk) - num_digits;

	chunk = shift_bytes_left_branchless(chunk, num_non_digits);

	{
		const __m128i mult = _mm_set_epi8(1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10);
		chunk = _mm_maddubs_epi16(chunk, mult);
	}
	{
		const __m128i mult = _mm_set_epi16(1, 100, 1, 100, 1, 100, 1, 100);
		chunk = _mm_madd_epi16(chunk, mult);
	}
	{
		chunk = _mm_packus_epi32(chunk, chunk);
		const __m128i mult = _mm_set_epi16(0, 0, 0, 0, 1, 10000, 1, 10000);
		chunk = _mm_madd_epi16(chunk, mult);
	}

	uint64_t low = _mm_extract_epi64(chunk, 0);

	uint64_t result = ((low & 0xffffffff) * 100000000) + (low >> 32);

	return result;
}

/*
	Fast parsing of a int64 value, maximum 16 digits
*/
inline int64_t parse_int64_fast(char*& data)
{
	int64_t neg = 1;
	if (*data == '-')
	{
		neg = -1;
		data++;
	}
	return neg * parse_uint64_fast(data);
}
