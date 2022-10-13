/* #include "utdelt.h"
#include <iostream>

namespace LinkedList{

std::ostream & operator<<(std::ostream & os, const Node & node){
    os << node.getValue();
    return os;
}

Node* LinkedList::insert(Node *pos, const std::string& value){
    auto prev = pos->prev;
    Node ins{value, std::move(prev->next), prev};
    prev->next = std::make_unique<Node>(ins);
}

std::ostream & operator<<(std::ostream & os, const LinkedList& list){
    auto start = list.begin();
    while (start != list.end()){
        os << start << "\n";
        start = start->getNext();
    }
}
}//namespace LinkedList


void testLinkedLists(){
    LinkedList::LinkedList l{};
    l.insert(l.end(), "first");
    std::cout << l;

    l.insert(l.end(), "second");
    std::cout << l;
}
*/