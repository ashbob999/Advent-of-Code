#include "aocHelper.h"

BaseDay::BaseDay(string _day) : time(0), dayStr(_day)
{
	filename = FILEPATH + "day" + dayStr + ".txt";

	stringResult.first = new char[512]{};
	stringResult.second = new char[512]{};
}

void BaseDay::load_input()
{
	if (input_loaded)
	{
		return;
	}

	// open the file
	fstream fp;
	fp.open(filename);

	// go to the end of the file
	fp.seekg(0, fp.end);

	// get length of file
	int len = fp.tellg();
	//cout << "length: " << len << endl;
	length = len;

	// create the char array with length + padding values
	input = new char[len + PADDING];
	input_start = input;

	// fill the end padding with zeros
	fill(input + len, input + len + PADDING, '\0');

	// set position to the beginning
	fp.seekg(0, fp.beg);

	// read the whole file into input
	fp.read(input, len);

	if (fp)
	{
		//cout << "read " << len << " chars" << endl;
		input_loaded = true;
	}
	else
	{
		cout << filename << " error: only " << fp.gcount() << " could be read";
	}

	// close the file
	fp.close();
}

void BaseDay::unload_input()
{
	if (!input_loaded)
	{
		return;
	}

	delete[] input_start;
	input_loaded = false;
}

double BaseDay::run()
{
	auto st = chrono::steady_clock::now();

	auto r = solve();

	auto et = chrono::steady_clock::now();

	auto elapsed = et - st;

	double t = 1e-3 * chrono::duration_cast<chrono::nanoseconds>(elapsed).count();

	time = t;
	result = r;

	input = input_start;

	return time;
}

BaseDay::~BaseDay()
{
	unload_input();

	delete[] stringResult.first;
	delete[] stringResult.second;
	//delete[] input_start;
}

void runDays(vector<BaseDay*> days)
{
	runtimeOptions options;
	runDays(days, options);
}

void runDays(vector<BaseDay*> days, runtimeOptions options)
{
	double minTotal = 0, avgTotal = 0, maxTotal = 0;
	int repetitions = options.repetitions;

	//       ,         Min    ,         Avg    ,         Max   ,
	//=======,================,================,===============,
	//Day 01:, 0000000.000 us,, 0000000.000 us,, 0000000.000 us,

	cout << "                Min             Avg             Max   " << endl;
	cout << "======================================================" << endl;

	for (auto& day: days)
	{
		day->load_input();

		vector<double> times(repetitions);
		for (int i = 0; i < repetitions; i++)
		{
			times[i] = day->run();
			//cout << times[i] << endl;
		}

		double minVal = *min_element(times.begin(), times.end());
		double maxVal = *max_element(times.begin(), times.end());

		double avgVal = accumulate(times.begin(), times.end(), 0.0) / repetitions;

		minTotal += minVal;
		avgTotal += avgVal;
		maxTotal += maxVal;

		cout << "Day " << day->dayStr << ": ";
		cout << right << setw(11) << setfill(' ') << fixed << setprecision(3) << minVal;
		cout << " us, ";
		cout << right << setw(11) << setfill(' ') << fixed << setprecision(3) << avgVal;
		cout << " us, ";
		cout << right << setw(11) << setfill(' ') << fixed << setprecision(3) << maxVal;
		cout << " us";

		cout << endl;

		day->unload_input();
	}

	cout << "======================================================" << endl;
	cout << " Total: ";
	cout << right << setw(11) << setfill(' ') << fixed << setprecision(3) << minTotal;
	cout << " us, ";
	cout << right << setw(11) << setfill(' ') << fixed << setprecision(3) << avgTotal;
	cout << " us, ";
	cout << right << setw(11) << setfill(' ') << fixed << setprecision(3) << maxTotal;
	cout << " us";

	cout << endl;
}
