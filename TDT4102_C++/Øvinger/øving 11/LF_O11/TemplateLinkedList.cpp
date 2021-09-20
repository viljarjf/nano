#include "TemplateLinkedList.h"

#include <iostream>
#include <string>

using namespace TemplateLinkedList;

namespace { // anonymous namespace to hide functions from other compilation units
namespace StringTest {
void assertEqual(const LinkedList<std::string>& ll, const std::string& s) {
    std::stringstream ss;
    ss << ll;
    assert(ss.str() == s);
}

void insert_at_end_test() {
    LinkedList<std::string> ll;
    for (auto x : {"A", "B", "C"}) {
        ll.insert(ll.end(), x);
    }
    assertEqual(ll, "[A B C]");
}

void insert_at_head_test() {
    LinkedList<std::string> ll;
    for (auto x : {"A", "B", "C"}) {
        ll.insert(ll.begin(), x);
    }
    assertEqual(ll, "[C B A]");
}

void insert_test() {
    LinkedList<std::string> ll;
    ll.insert(ll.begin(), "A");
    ll.insert(ll.end(), "D");
    ll.insert(ll.end()->getPrev(), "C");
    ll.insert(ll.begin()->getNext(), "B");
    assertEqual(ll, "[A B C D]");
}

void find_test() {
    LinkedList<std::string> ll;
    for (auto x : {"A", "B", "C", "D"}) {
        ll.insert(ll.end(), x);
    }
    auto c = ll.find("C");
    assert(c->getValue() == "C");
}

void remove_test() {
    LinkedList<std::string> ll;
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
} // StringTest
namespace IntTest {
void assertEqual(const LinkedList<int>& ll, const std::string& s) {
    std::stringstream ss;
    ss << ll;
    assert(ss.str() == s);
}

void insert_at_end_test() {
    LinkedList<int> ll;
    for (auto x : {1, 2, 3}) {
        ll.insert(ll.end(), x);
    }
    assertEqual(ll, "[1 2 3]");
}

void insert_at_head_test() {
    LinkedList<int> ll;
    for (auto x : {1, 2, 3}) {
        ll.insert(ll.begin(), x);
    }
    assertEqual(ll, "[3 2 1]");
}

void insert_test() {
    LinkedList<int> ll;
    ll.insert(ll.begin(), 1);
    ll.insert(ll.end(), 4);
    ll.insert(ll.end()->getPrev(), 3);
    ll.insert(ll.begin()->getNext(), 2);
    assertEqual(ll, "[1 2 3 4]");
}

void find_test() {
    LinkedList<int> ll;
    for (auto x : {1, 2, 3, 4}) {
        ll.insert(ll.end(), x);
    }
    auto c = ll.find(3);
    assert(c->getValue() == 3);
}

void remove_test() {
    LinkedList<int> ll;
    for (auto x : {1, 2, 3, 4}) {
        ll.insert(ll.end(), x);
    }
    auto c = ll.find(3);
    ll.remove(c);
    assertEqual(ll, "[1 2 4]");
    ll.remove(ll.begin());
    ll.remove(ll.begin()->getNext());
    ll.remove(ll.end()->getPrev());
    assert(ll.isEmpty());
}
} // StringTest
} // anonymous namespace

void testTemplateLinkedList() {
    StringTest::insert_at_end_test();
    StringTest::insert_at_head_test();
    StringTest::insert_test();
    StringTest::find_test();
    StringTest::remove_test();
    IntTest::insert_at_end_test();
    IntTest::insert_at_head_test();
    IntTest::insert_test();
    IntTest::find_test();
    IntTest::remove_test();
    std::cout << "All TemplateLinkedList tests succeeded\n";
}

