#include "../aocHelper.h"

#include <bit>
#include <span>

namespace
{
	struct custom_hash_fnv1a
	{
		size_t operator()(const std::pair<const std::string_view&, const std::string_view>& v) const noexcept
		{
			// fnv1a hash
			constexpr size_t fnv_offset_basis = 0xcbf29ce484222325;
			constexpr size_t fnv_prime = 0x100000001b3;

			size_t hash = fnv_offset_basis;
			for (auto& c : v.first)
			{
				hash = hash ^ c;
				hash *= fnv_prime;
			}

			for (auto& c : v.second)
			{
				hash = hash ^ c;
				hash *= fnv_prime;
			}

			return hash;
		}
	};

	using custom_hash = custom_hash_fnv1a;

	long long count_perms(
		const std::string_view str,
		const std::string_view counts,
		std::unordered_map<std::pair<const std::string_view, const std::string_view>, long long, custom_hash>& mem)
	{
		auto it = mem.find({str, counts});
		if (it != mem.end())
		{
			return it->second;
		}

		if (counts.size() == 0)
		{
			if (str.find('#') != std::string::npos)
			{
				// still more #, but no counts left
				return 0;
			}
			return 1;
		}

		// check length is valid
		if (str.size() < counts[0])
		{
			return 0;
		}

		long long count = 0;

		std::string_view sub{str.data(), str.data() + counts[0]};
		if (sub.find('.') == std::string::npos)
		{
			// check char after count is valid
			if (str.size() == counts[0] || str[counts[0]] != '#')
			{
				if (counts[0] + 1 > str.size())
				{
					count += count_perms({}, counts.substr(1), mem);
				}
				else
				{
					count += count_perms(str.substr(counts[0] + 1), counts.substr(1), mem);
				}
			}
		}

		if (str[0] != '#')
		{
			count += count_perms(str.substr(1), counts, mem);
		}

		mem[{str, counts}] = count;
		return count;
	}
}

class Day12 : public BaseDay
{
public:
	Day12() : BaseDay("12") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// using string for counts array because we can compare string_view's
		std::vector<std::pair<std::string, std::string>> data{};

		while (*input != '\0')
		{
			char* start = input;
			while (*input != ' ')
			{
				input++;
			}

			std::string str{start, input};

			input++; // skip ' '

			std::string counts{};
			counts.push_back(numericParse<uint8_t>(input));
			while (*input != '\n')
			{
				input++; // skip ','
				counts.push_back(numericParse<uint8_t>(input));
			}

			input++; // skip '\n'

			data.emplace_back(std::move(str), std::move(counts));
		}

		std::unordered_map<std::pair<const std::string_view, const std::string_view>, long long, custom_hash> mem{};

		int custom_bucket_count = 0;
		for (auto& line : data)
		{
			custom_bucket_count += line.first.size() * 5 * line.second.size();
		}
		mem.max_load_factor(1.5);
		mem.rehash(custom_bucket_count);

		for (auto& line : data)
		{
			long long count = count_perms(line.first, line.second, mem);
			part1 += count;
		}

		std::vector<std::pair<std::string, std::string>> data_part2{};
		for (auto& line : data)
		{
			std::string str{};
			std::string counts{};

			for (int i = 0; i < 5; i++)
			{
				if (i != 0)
				{
					str += '?';
				}
				str += line.first;
				counts += line.second;
			}

			data_part2.emplace_back(std::move(str), std::move(counts));
		}

		for (auto& line : data_part2)
		{
			long long count = count_perms(line.first, line.second, mem);
			part2 += count;
		}

		return {part1, part2};
	}
};
