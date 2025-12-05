#include "../aocHelper.h"

template<class T>
inline T negMod(T n, T m) {
	return ((n % m) + m) % m;
}

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		std::vector<std::pair<bool, int16_t>> moves{};
		
		while (*input != '\0') {
			char c = *input;
			input++;
			
			int16_t v = numericParse<uint16_t>(input);
			
			moves.push_back({c == 'L', v});
			
			input++;
		}
		
		// part 1
		int16_t curr = 50;
		for (auto& [dir, count] : moves) {
			if (dir) {
				curr += count;
			} else {
				curr -= count;
			}

			curr = negMod(curr, static_cast<int16_t>(100));

			if (curr == 0) {
				part1++;
			}
		}
		
		// part 2
		curr = 50;
		for (auto& [dir, count] : moves) {
			if (dir) {
				if (curr + count <= 99) {
					curr += count;
				} else {
					for (int16_t i = 0; i< count; i++) {
						if (curr == 99) {
							curr = 0;
						} else {
							curr++;
						}
						
						if (curr == 0) {
							part2++;
						}
					}
				}
			} else {
				if (curr > count) {
					curr -= count;
				} else {
					for (int16_t i = 0; i< count; i++) {
						if (curr == 0) {
							curr = 99;
						} else {
							curr--;
						}
						
						if (curr == 0) {
							part2++;
						}
					}
				}
			}
		}

		return {part1, part2};
	}
};
