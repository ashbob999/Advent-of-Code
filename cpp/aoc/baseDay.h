#pragma once

#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <utility>

using result_type = std::pair<long long, long long>;

class BaseDay
{
public:
	inline BaseDay(const std::string& _day);
	inline virtual ~BaseDay();

	static constexpr int Padding = 256 / 8;
	inline static const std::string Filepath = "input/"; // "../input/";

	// virtual void parseInput() const = 0;
	inline virtual result_type solve() = 0;

	inline bool load_input();
	inline void unload_input();

	std::string dayStr{};
	char* input{nullptr};

	std::unique_ptr<char[]> input_data{};

	int input_length{0};

	static constexpr int StringResultSize = 512;
	std::pair<std::array<char, StringResultSize>, std::array<char, StringResultSize>> stringResult{};

	inline virtual double run() final;

private:
	std::string filename{};
	char* input_start{nullptr};
};

BaseDay::BaseDay(const std::string& day) : dayStr(day)
{
	this->filename = BaseDay::Filepath + "day" + dayStr + ".txt";
}

BaseDay::~BaseDay()
{
	this->unload_input();
}

bool BaseDay::load_input()
{
	if (this->input_data)
	{
		return true;
	}

	// open the file
	std::fstream fp;
	fp.open(filename);

	// go to the end of the file
	fp.seekg(0, fp.end);

	// get length of file
	int len = static_cast<int>(fp.tellg());
	// cout << "length: " << len << endl;
	this->input_length = len;

	// create the char array with length + padding values
	this->input_data = std::make_unique<char[]>(len + BaseDay::Padding);
	this->input = this->input_data.get();
	this->input_start = input;

	// fill the end padding with zeros
	std::fill(this->input + len, this->input + len + BaseDay::Padding, '\0');

	// set position to the beginning
	fp.seekg(0, fp.beg);

	// read the whole file into input
	fp.read(this->input, len);

	bool success = true;

	if (fp)
	{
		// cout << "read " << len << " chars" << endl;
	}
	else
	{
		std::cout << filename << " error: only " << fp.gcount() << " could be read";
		this->unload_input();
		success = false;
	}

	// close the file
	fp.close();

	return success;
}

void BaseDay::unload_input()
{
	this->input_data.reset();
	this->input = nullptr;
	this->input_start = nullptr;
	this->input_length = 0;
}

double BaseDay::run()
{
	// auto st = std::chrono::steady_clock::now();
	auto st = std::chrono::high_resolution_clock::now();

	auto r = this->solve();

	// auto et = std::chrono::steady_clock::now();
	auto et = std::chrono::high_resolution_clock::now();

	auto elapsed = et - st;

	double t = 1e-3 * std::chrono::duration_cast<std::chrono::nanoseconds>(elapsed).count();

	this->input = this->input_start;

	return t;
}

template<std::size_t Size>
std::ostream& operator<<(std::ostream& os, const std::array<char, Size>& data)
{
	for (auto&& c : data)
	{
		if (c == '\0')
		{
			break;
		}
		os.put(c);
	}
	return os;
}
