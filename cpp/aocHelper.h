#pragma once

#include <iostream>
#include <fstream>
#include <chrono>
#include <string>
#include <cstring>
#include <cstdio>
#include <cstdint>
#include <vector>
#include <array>
#include <set>
#include <unordered_set>
#include <map>
#include <unordered_map>
#include <deque>
#include <algorithm>
#include <numeric>
#include <functional>
#include <bitset>
#include <iomanip>
#include <optional>
#include <list>
#include <variant>
#include <memory>
//#include <immintrin.h>

using namespace std;

using result_type = pair<long long, long long>;

class BaseDay
{
public:
	static const int PADDING = 10;
	inline static const string FILEPATH = "input/";// "../input/";

	//virtual void parseInput() const = 0;
	virtual result_type solve() = 0;

	void load_input();
	void unload_input();

	bool input_loaded = false;

	string filename;
	double time;
	string dayStr;
	char* input;
	char* input_start;
	int length;

	result_type result;
	pair<char*, char*> stringResult;

	BaseDay(string _day);
	virtual ~BaseDay();

	virtual double run() final;
};

template<typename T>
T numericParse(char*& p)
{
	bool have = false;
	T n = 0;
	for (; *p != '\0'; p++)
	{
		//cout << "n: " << n << " ";
		//cout << "char: " << *p << " ";
		T d = *p - '0';
		//cout << "digit: " << d << " ";
		if (d >= 0 && d <= 9)
		{
			n = 10 * n + d;
			have = true;
		}
		else if (have)
		{
			return n;
		}
	}
	if (have)
	{
		return n;
	}
	return 0;
}

struct runtimeOptions
{
	int repetitions = 1000;
};

void runDays(vector<BaseDay*> days);
void runDays(vector<BaseDay*> days, runtimeOptions options);
