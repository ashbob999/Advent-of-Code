#pragma once

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
