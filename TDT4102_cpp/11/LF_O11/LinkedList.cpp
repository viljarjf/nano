#include "LinkedList.h"

#include <cassert>
#include <iostream>
#include <memory>
#include <ostream>
#include <sstream>
#include <string>

/*

Teorispørsmål fra oppgave 3 b):

1) I en lenket liste kan man sette inn og fjerne elementer i konstant tid O(1), men hvis man skal
finne et element må man iterere gjennom hele listen, noe som er sakte. I en vektor er det raskt å
finne et element, men det krever O(n) tid å sette inn et element. Hvis man tror at man kommer til å
sette inn og fjerne elementer mye er derfor lenkede lister mer effektive enn vektorer.

2) Se f.eks.:

http://www.labri.fr/perso/strandh/Teaching/MTP/Common/Strandh-Tutorial/queue-list.html
https://www.cs.bu.edu/teaching/c/stack/linked-list/

*/

namespace LinkedList {
std::ostream& operator<<(std::ostream& os, const Node& node)
{
	return os << node.getValue();
}

Node* LinkedList::insert(Node* pos, const std::string& value)
{
	// make sure pos isn't nullptr (for debugging purposes)
	assert(pos);
	if (pos == begin()) { // if pos is the first node
		// create a new head node, point to the old head node
		head = std::make_unique<Node>(value, std::move(head), nullptr);
		// and make the old head node point back to the new one
		pos->prev = begin();
	} else {
		// find the previous node
		auto prevNode = pos->prev;
		// make the previous node point to (and own) the new node
		prevNode->next = std::make_unique<Node>(value, std::move(prevNode->next), prevNode);
		// make the given node point back to the new node
		pos->prev = prevNode->getNext();
	}
	// return a pointer to the new node
	return pos->prev;
}

Node* LinkedList::find(const std::string& value)
{
	// node points to the first node
	auto node = begin();
	// traverse the list untill we reach the end, ord finds the value
	while (node != end() && node->value != value) {
		// make node point to the next node
		node = node->getNext();
	}
	// return the node with the given value,
	// or end() if the value wasn't found
	return node;
}

Node* LinkedList::remove(Node* pos)
{
	// make sure pos isn't nullptr
	assert(pos);
	// it's illegal to remove the last node, since it's a "dummy node"
	assert(pos != end());
	// if we want to remove the head
	if (pos == begin()) {
		// make head point to the next node
		// note: the previous head node is deallocated when it's no longer pointed to
		head = std::move(pos->next);
		// the new head doesn't have a previous node
		head->prev = nullptr;
		// return a pointer to the node after the deleted node, which
		// is the new head in this case
		return begin();
	}

	// store the return value for later use
	auto ret = pos->getNext();
	// make the node after pos point to the node before pos
	// note: this have to be done before deleting pos
	pos->next->prev = pos->prev;
	// make the node before pos point to (and own) the node after pos
	// note: pos is deallocated when the previous node no longer has
	// a unique_ptr to it, so pos no longer points to a valid node
	pos->prev->next = std::move(pos->next);
	// return the node after the deleted node
	return ret;
}

void LinkedList::remove(const std::string& value)
{
	// use the member method find to find the wanted node
	auto node = find(value);
	// check if the value was found
	if (node != end()) {
		// remove the node
		remove(node);
	}
}

std::ostream& operator<<(std::ostream& os, const LinkedList& list)
{
	auto x = list.begin();
	os << "[" << *x;
	x = x->getNext();
	while (x != list.end()) {
		os << " " << *x;
		x = x->getNext();
	}
	os << "]";
	return os;
}


namespace { // anonymous namespace to hide functions from other compilation units
	void assertEqual(const LinkedList& ll, const std::string& s)
	{
		std::stringstream ss;
		ss << ll;
		assert(ss.str() == s);
	}

	void insert_at_end_test()
	{
		LinkedList ll;
		for (auto x : {"A", "B", "C"}) {
			ll.insert(ll.end(), x);
		}
		assertEqual(ll, "[A B C]");
	}

	void insert_at_head_test()
	{
		LinkedList ll;
		for (auto x : {"A", "B", "C"}) {
			ll.insert(ll.begin(), x);
		}
		assertEqual(ll, "[C B A]");
	}

	void insert_test()
	{
		LinkedList ll;
		ll.insert(ll.begin(), "A");
		ll.insert(ll.end(), "D");
		ll.insert(ll.end()->getPrev(), "C");
		ll.insert(ll.begin()->getNext(), "B");
		assertEqual(ll, "[A B C D]");
	}

	void find_test()
	{
		LinkedList ll;
		for (auto x : {"A", "B", "C", "D"}) {
			ll.insert(ll.end(), x);
		}
		auto c = ll.find("C");
		assert(c->getValue() == "C");
	}

	void remove_test()
	{
		LinkedList ll;
		for (auto x : {"A", "B", "C", "D"}) {
			ll.insert(ll.end(), x);
		}
		auto c = ll.find("C");
		ll.remove(c);
		assertEqual(ll, "[A B D]");
		ll.remove(ll.begin());
		ll.remove(ll.begin()->getNext());
		ll.remove(ll.end()->getPrev());
		assert(ll.isEmpty());
	}
} // namespace
} // namespace LinkedList

void testLinkedList()
{
	// using namespace ::LinkedList;
	using LinkedList::LinkedList;
	using namespace std;

	LinkedList list;
	list.insert(list.begin(), "yankee");
	list.insert(list.begin(), "dollar");
	cout << list <<'\n';
	list.insert(list.find("dollar"), "doodle");
	list.insert(list.end(), ";)");
	cout << list << '\n';
	// list.remove(list.end());
	list.remove(list.find("dollar"));
	cout << list << '\n';


	// insert_at_end_test();
	// insert_at_head_test();
	// insert_test();
	// find_test();
	// remove_test();
	// std::cout << "All LinkedList tests succeeded\n";
}
