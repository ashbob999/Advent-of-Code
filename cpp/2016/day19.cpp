#include "../aocHelper.h"

#include "skiplist/SkipList.h"

class Elf
{
public:
	int id;
	int presents = 1;
	Elf* prev = nullptr;
	Elf* next = nullptr;
	Elf(int id) : id(id) {}

	void take_v1()
	{
		this->presents += this->next->presents;
		this->next = this->next->next;
	}

	void take_v2(OrderedStructs::SkipList::HeadNode<int>& skiplist, Elf** elves, int elf_count)
	{
		int steal_count = elf_count / 2;
		int curr_index = skiplist.index(this->id);

		int steal_index = (curr_index + steal_count) % elf_count;

		int steal_id = skiplist.at(steal_index);
		Elf* steal_from = elves[steal_id - 1];

		this->presents += steal_from->presents;
		steal_from->prev->next = steal_from->next;
		steal_from->next->prev = steal_from->prev;

		skiplist.remove(steal_id);
	}
};

class Day19 : public BaseDay
{
public:
	Day19() : BaseDay("19") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		int elf_count = numericParse<int>(input);

		// create the elves
		Elf** elves = new Elf * [elf_count];

		for (int i = 0; i < elf_count; i++)
		{
			elves[i] = new Elf(i + 1);
		}

		// part 1

		// setup pointers
		Elf* elf1 = elves[0];
		Elf* prev_elf = elf1;
		for (int i = 1; i < elf_count; i++)
		{
			Elf* curr_elf = elves[i];
			curr_elf->prev = prev_elf;
			prev_elf->next = curr_elf;
			prev_elf = curr_elf;
		}
		prev_elf->next = elf1;
		elf1->prev = prev_elf;

		Elf* curr_elf = elf1;
		while (curr_elf != curr_elf->next)
		{
			curr_elf->take_v1();
			curr_elf = curr_elf->next;
		}

		part1 = curr_elf->id;


		// part 2
		int current_elf_count = elf_count;

		OrderedStructs::SkipList::HeadNode<int> skiplist;

		elf1 = elves[0];
		prev_elf = elf1;
		skiplist.insert(elf1->id);
		for (int i = 1; i < elf_count; i++)
		{
			Elf* curr_elf = elves[i];
			curr_elf->prev = prev_elf;
			prev_elf->next = curr_elf;
			skiplist.insert(curr_elf->id);
			prev_elf = curr_elf;
		}
		prev_elf->next = elf1;
		elf1->prev = prev_elf;


		curr_elf = elf1;
		while (curr_elf != curr_elf->next)
		{
			curr_elf->take_v2(skiplist, elves, current_elf_count);
			curr_elf = curr_elf->next;
			current_elf_count--;
		}

		part2 = curr_elf->id;

		// delete the elves
		for (int i = 0; i < elf_count; i++)
		{
			delete elves[i];
		}

		delete[] elves;

		return { part1, part2 };
	}
};
