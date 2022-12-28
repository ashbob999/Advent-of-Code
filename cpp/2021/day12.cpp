#include "../aocHelper.h"

struct string_hash
{
	using is_transparent = void;
	[[nodiscard]] size_t operator()(std::string_view txt) const
	{
		return std::hash<std::string_view>{}(txt);
	}
};

class Day12 : public BaseDay
{
public:
	Day12() : BaseDay("12") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// https://www.cppstories.com/2021/heterogeneous-access-cpp20/
		unordered_map<string, unordered_set<string>, string_hash, std::equal_to<>> graph;

		while (*input != '\0')
		{
			string s1;

			while (*input != '-')
			{
				s1 += *input;
				input++;
			}

			input++;

			string s2;

			while (*input != '\n')
			{
				s2 += *input;
				input++;
			}

			input++;

			graph[s1].insert(s2);
			graph[s2].insert(s1);
		}

		// part 1
		function<void(set<vector<string_view>>&, vector<string_view>&)> find_paths_p1;
		find_paths_p1 = [&graph, &find_paths_p1](set<vector<string_view>>& paths, vector<string_view>& curr_path)
		{
			if (curr_path.back() == "end")
			{
				paths.insert(std::move(curr_path));
				return;
			}

			string_view last = curr_path.back();

			for (auto& node : graph.find(last)->second)
			{
				if (node == "start")
				{
					continue;
				}

				if (node == "end")
				{
					vector<string_view> new_path = curr_path;
					new_path.push_back(node);
					find_paths_p1(paths, new_path);
				}
				else
				{
					if (node[0] >= 'a' && node[0] <= 'z')
					{
						if (find(curr_path.begin(), curr_path.end(), node) == curr_path.end())
						{
							vector<string_view> new_path = curr_path;
							new_path.push_back(node);
							find_paths_p1(paths, new_path);
						}
					}
					else
					{
						vector<string_view> new_path = curr_path;
						new_path.push_back(node);
						find_paths_p1(paths, new_path);
					}
				}
			}
		};

		set<vector<string_view>> paths_p1;
		string start = "start";
		vector<string_view> path = { string_view{start} };
		find_paths_p1(paths_p1, path);
		part1 = paths_p1.size();

		// part 2
		function<void(set<vector<string_view>>&, vector<string_view>&, bool)> find_paths_p2;
		find_paths_p2 = [&graph, &find_paths_p2](set<vector<string_view>>& paths, vector<string_view>& curr_path, bool has_2)
		{
			if (curr_path.back() == "end")
			{
				paths.insert(std::move(curr_path));
				return;
			}

			string_view last = curr_path.back();

			for (auto& node : graph.find(last)->second)
			{
				if (node == "start")
				{
					continue;
				}

				if (node == "end")
				{
					vector<string_view> new_path = curr_path;
					new_path.push_back(node);
					find_paths_p2(paths, new_path, has_2);
				}
				else
				{
					if (node[0] >= 'a' && node[0] <= 'z')
					{
						if (find(curr_path.begin(), curr_path.end(), node) == curr_path.end())
						{
							vector<string_view> new_path = curr_path;
							new_path.push_back(node);
							find_paths_p2(paths, new_path, has_2);
						}
						else if (!has_2)
						{
							vector<string_view> new_path = curr_path;
							new_path.push_back(node);
							find_paths_p2(paths, new_path, true);
						}
					}
					else
					{
						vector<string_view> new_path = curr_path;
						new_path.push_back(node);
						find_paths_p2(paths, new_path, has_2);
					}
				}
			}
		};

		set<vector<string_view>> paths_p2;
		path = { string_view{start} };
		find_paths_p2(paths_p2, path, false);
		part2 = paths_p2.size();

		return { part1, part2 };
	}
};
