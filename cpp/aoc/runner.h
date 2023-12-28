#pragma once

#include "./baseDay.h"

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

struct RuntimeOptions
{
	int repetitions = 1000;
};

inline void runDays(std::vector<BaseDay*> days);
inline void runDays(std::vector<BaseDay*> days, const RuntimeOptions& options);

void runDays(std::vector<BaseDay*> days)
{
	RuntimeOptions options{};
	runDays(days, options);
}

void runDays(std::vector<BaseDay*> days, const RuntimeOptions& options)
{
	double minTotal = 0, avgTotal = 0, maxTotal = 0;
	int repetitions = options.repetitions;

	//       ,         Min    ,         Avg    ,         Max   ,
	//=======,================,================,===============,
	// Day 01:, 0000000.000 us,, 0000000.000 us,, 0000000.000 us,

	std::cout << "                Min             Avg             Max   " << std::endl;
	std::cout << "======================================================" << std::endl;

	for (auto& day : days)
	{
		day->load_input();

		std::vector<double> times(repetitions);
		for (int i = 0; i < repetitions; i++)
		{
			times[i] = day->run();
			// cout << times[i] << endl;
		}

		double minVal = *std::min_element(times.begin(), times.end());
		double maxVal = *std::max_element(times.begin(), times.end());

		double avgVal = std::accumulate(times.begin(), times.end(), 0.0) / repetitions;

		minTotal += minVal;
		avgTotal += avgVal;
		maxTotal += maxVal;

		std::cout << "Day " << day->dayStr << ": ";
		std::cout << std::right << std::setw(11) << std::setfill(' ') << std::fixed << std::setprecision(3) << minVal;
		std::cout << " us, ";
		std::cout << std::right << std::setw(11) << std::setfill(' ') << std::fixed << std::setprecision(3) << avgVal;
		std::cout << " us, ";
		std::cout << std::right << std::setw(11) << std::setfill(' ') << std::fixed << std::setprecision(3) << maxVal;
		std::cout << " us";

		std::cout << std::endl;

		day->unload_input();
	}

	std::cout << "======================================================" << std::endl;
	std::cout << " Total: ";
	std::cout << std::right << std::setw(11) << std::setfill(' ') << std::fixed << std::setprecision(3) << minTotal;
	std::cout << " us, ";
	std::cout << std::right << std::setw(11) << std::setfill(' ') << std::fixed << std::setprecision(3) << avgTotal;
	std::cout << " us, ";
	std::cout << std::right << std::setw(11) << std::setfill(' ') << std::fixed << std::setprecision(3) << maxTotal;
	std::cout << " us";

	std::cout << std::endl;
}
