#include "../aocHelper.h"

#include "md5_simd/md5-simd.h"

class Day17 : public BaseDay
{
public:
	Day17() : BaseDay("17") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		constexpr char char_map[10] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };

		auto digit_count = [](int number)
		{
			if (number < 10) return 1;
			if (number < 100) return 2;
			if (number < 1000) return 3;
			if (number < 10000) return 4;
			if (number < 100000) return 5;
			if (number < 1000000) return 6;
			if (number < 10000000) return 7;
			if (number < 100000000) return 8;
			if (number < 1000000000) return 9;
			return 10;
		};

		// parse input
		char buffer[100]{ '\0' };
		string input_str;

		int id_length = 0;
		while (*input != '\n')
		{
			buffer[id_length] = *input;
			input_str += *input;
			input++;
			id_length++;
		}

		// setup md5
		uint64_t lengths[8];

		char* buffers[8];
		buffers[0] = new char[128];
		buffers[1] = new char[128];
		buffers[2] = new char[128];
		buffers[3] = new char[128];
		buffers[4] = new char[128];
		buffers[5] = new char[128];
		buffers[6] = new char[128];
		buffers[7] = new char[128];

		md5_simd::MD5_SIMD md5;

		auto check = [&](string& code, string& path)->array<bool, 4>
		{
			string inputs[1] = { code + path };
			md5.calculate<1, false>(inputs); // calculate the hashes

			string hex = md5.hexdigest(0);

			array<bool, 4> dirs{ true };

			for (int i = 0; i < 4; i++)
			{
				if ((hex[i] >= '0' && hex[i] <= '9') || hex[i] == 'a')
				{
					dirs[i] = false;
				}
				else
				{
					dirs[i] = true;
				}
			}

			return dirs;
		};

		struct place
		{
			array<int, 2> pos;
			string path;
		};

		function<void(set<string>&, string&, string, array<int, 2>, array<int, 2>&)> solve;
		solve = [&](set<string>& paths, string& code, string path, array<int, 2> curr_pos, array<int, 2>& end_pos)
		{
			auto dirs = check(code, path);

			vector<place> next_places;

			if (curr_pos[1] > 0 && dirs[0])
			{
				next_places.emplace_back(array<int, 2>{ curr_pos[0], curr_pos[1] - 1 }, path + 'U');
			}
			if (curr_pos[1] < 3 && dirs[1])
			{
				next_places.emplace_back(array<int, 2>{ curr_pos[0], curr_pos[1] + 1 }, path + 'D');
			}
			if (curr_pos[0] > 0 && dirs[2])
			{
				next_places.emplace_back(array<int, 2>{ curr_pos[0] - 1, curr_pos[1] }, path + 'L');
			}
			if (curr_pos[0] < 3 && dirs[3])
			{
				next_places.emplace_back(array<int, 2>{ curr_pos[0] + 1, curr_pos[1] }, path + 'R');
			}

			for (auto& np : next_places)
			{
				if (np.pos[0] == end_pos[0] && np.pos[1] == end_pos[1])
				{
					paths.insert(np.path);
				}
				else
				{
					solve(paths, code, np.path, np.pos, end_pos);
				}
			}
		};

		array<int, 2> start_pos = { 0, 0 };
		array<int, 2> end_pos = { 3,3 };

		set<string> paths;
		solve(paths, input_str, "", start_pos, end_pos);

		// part 1
		string p1_str = *min_element(paths.begin(), paths.end(), [&](const string& a, const string& b)
		{
			return a.length() < b.length();
		});

		memcpy(this->stringResult.first, p1_str.c_str(), p1_str.length());

		// part 2
		string p2_str = *max_element(paths.begin(), paths.end(), [&](const string& a, const string& b)
		{
			return a.length() < b.length();
		});

		part2 = p2_str.length();

		return { part1, part2 };
	}
};
