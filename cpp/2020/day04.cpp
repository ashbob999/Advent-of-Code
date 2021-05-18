#include "../aocHelper.h"

class Day04 : public BaseDay
{
public:
	Day04() : BaseDay("04") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// byr = 1621234
		// cid = 1635556
		// ecl = 1667564
		// eyr = 1670386
		// hcl = 1716716
		// hgt = 1717236
		// iyr = 1735922
		// pid = 1848548
		static constexpr auto hash = [](const char* str)
		{
			return (str[0] << 14) + (str[1] << 7) + (str[2]);
		};

		enum field_codes :int
		{
			byr = 1621234,
			cid = 1635556,
			ecl = 1667564,
			eyr = 1670386,
			hcl = 1716716,
			hgt = 1717236,
			iyr = 1735922,
			pid = 1848548
		};

		enum class field_index : int
		{
			byr, cid, ecl, eyr, hcl, hgt, iyr, pid
		};

		auto check_range = [](char* str, int min, int max, int digits)
		{
			int n = numericParse<int>(str);
			if (n >= min && n <= max)
			{
				return true;
			}
			return false;
		};


		auto check = [&check_range](int field_hash, char* str)
		{
			switch (field_hash)
			{
				case field_codes::byr: return check_range(str, 1920, 2002, 4);
				case field_codes::iyr: return check_range(str, 2010, 2020, 4);
				case field_codes::eyr: return check_range(str, 2020, 2030, 4);
				case field_codes::hgt:
				{
					char* s = str;

					if (*s == 'c' && *(s + 1) == 'm')
					{
						return check_range(str, 150, 193, 1);
					}
					else if (*s == 'i' && *(s + 1) == 'n')
					{
						return check_range(str, 59, 76, 1);
					}
					return false;
				}
				case field_codes::hcl:
				{
					if (str[0] == '#')
					{
						for (int i = 1; i <= 6; i++)
						{
							//cout << "char " << str[i] << endl;
							if (str[i] < '0' || str[i] > 'f')
							{
								//cout << "first exit" << endl;
								return false;
							}
							if (str[i] > '9' && str[i] < 'a')
							{
								//cout << "second exit" << endl;
								return false;
							}
						}
						return true;
					}
					return false;
				}
				case field_codes::ecl:
				{
					if (*(str + 3) != '\0')
					{
						return false;
					}
					static constexpr int valid_values[7] = { hash("amb"), hash("blu"),
						hash("brn"), hash("gry"), hash("grn"), hash("hzl"), hash("oth")
					};
					int h = hash(str);

					for (int i = 0; i < 7; i++)
					{
						if (h == valid_values[i])
						{
							return true;
						}
					}
					return false;
				}
				case field_codes::pid:
				{
					for (int i = 0; i < 9; i++)
					{
						if (str[i] < '0' || str[i] > '9')
						{
							return false;
						}
					}
					if (str[9] != '\0')
					{
						return false;
					}
					return true;
				}
				case field_codes::cid: return true;
			}
			return true;
		};

		//char* value = new char[10]{};
		char value[15];
		int hash_value = 0;
		int i = 0;
		int p1_count = 0, p2_count = 0;

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				if (p1_count >= 7)
				{
					part1++;
					if (p2_count >= 7)
					{
						part2++;
					}
				}
				p1_count = 0;
				p2_count = 0;
				input++;
			}
			else if (*input == ':')
			{
				input++;
				i = 0;
				while (*input != ' ' && *input != '\n')
				{
					value[i] = *input;
					i++;
					input++;
				}

				value[i] = '\0';
				input++;

				if (hash_value != field_codes::cid)
				{
					p1_count++;
					p2_count += check(hash_value, value);
				}
			}
			else
			{
				hash_value = hash(input);
				input += 3;
			}
		}

		if (p1_count >= 7)
		{
			part1++;
			if (p2_count >= 7)
			{
				part2++;
			}
		}

		return { part1, part2 };
	}
};
