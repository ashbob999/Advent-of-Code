#include "../aocHelper.h"

namespace
{
	template<class T, size_t Size>
	class ArrayVector
	{
	public:
		inline ArrayVector() = default;

		inline T operator[](size_t i) const noexcept { return this->data[i]; }
		inline T& operator[](size_t i) noexcept { return this->data[i]; }

		inline size_t size() const noexcept { return this->data_size; }

		inline void push_back(const T& value) noexcept
		{
			this->data[this->data_size] = value;
			this->data_size++;
		}

		inline void push_back(T&& value) noexcept
		{
			this->data[this->data_size] = std::move(value);
			this->data_size++;
		}

		inline void pop_back() noexcept
		{
			if (this->data_size > 0)
			{
				this->data_size--;
			}
		}

		inline T front() const noexcept { return this->data[0]; }
		inline T& front() noexcept { return this->data[0]; }

		inline T back() const noexcept { return this->data[this->data_size - 1]; }
		inline T& back() noexcept { return this->data[this->data_size - 1]; }

		T* begin() noexcept { return this->data.data(); }
		const T* begin() const noexcept { return this->data.data(); }

		T* end() noexcept { return this->data.data() + this->data_size; }
		const T* end() const noexcept { return this->data.data() + this->data_size; }

	private:
		std::array<T, Size> data{};
		size_t data_size = 0;
	};

	inline int64_t predict_future(ArrayVector<int64_t, 32>& values)
	{
		int64_t front = values[0];
		int64_t back = values[values.size() - 1];

		bool allZero = true;

		for (int i = 0; i < values.size() - 1; i++)
		{
			int64_t diff = values[i + 1] - values[i];
			if (diff != 0)
			{
				allZero = false;
			}
			values[i] = diff;
		}
		values.pop_back();

		if (allZero)
		{
			return front;
		}
		else
		{
			return back + predict_future(values);
		}
	}

	inline int64_t predict_history(ArrayVector<int64_t, 32>& values)
	{
		int64_t front = values[0];
		int64_t back = values[values.size() - 1];

		bool allZero = true;

		for (int i = 0; i < values.size() - 1; i++)
		{
			int64_t diff = values[i + 1] - values[i];
			if (diff != 0)
			{
				allZero = false;
			}
			values[i] = diff;
		}
		values.pop_back();

		if (allZero)
		{
			return front;
		}
		else
		{
			return front - predict_history(values);
		}
	}
}

class Day09 : public BaseDay
{
public:
	Day09() : BaseDay("09") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		ArrayVector<ArrayVector<int64_t, 32>, 210> lists{};
		lists.push_back({});

		while (*input != '\0')
		{
			if (*input == '\n')
			{
				lists.push_back({});
				input++;
			}
			else
			{
				int64_t value = parse_int64_fast_withLeadingSpacing(input);
				lists.back().push_back(value);
			}
		}

		lists.pop_back();

		// part 1
		for (const auto& list : lists)
		{
			ArrayVector<int64_t, 32> values = list;
			part1 += predict_future(values);
		}

		// part 2
		for (const auto& list : lists)
		{
			ArrayVector<int64_t, 32> values = list;
			part2 += predict_history(values);
		}

		return {part1, part2};
	}
};
