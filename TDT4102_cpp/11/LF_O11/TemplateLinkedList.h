#pragma once

#include <memory>
#include <ostream>
#include <string>
#include <sstream>
#include <cassert>
#include <iostream>


// test code 
void testTemplateLinkedList();

namespace TemplateLinkedList {
// We need to forward declare this, so that it is known
// when declaring it as a friend 
template<typename T>
class LinkedList;

template<typename T>
class Node {
private:
    const T value;    // The data held by the LinkedList
    std::unique_ptr<Node<T>> next; // unique_ptr to the next node
    Node<T>* prev;                 // raw (non-owning) ptr to the previous node
public:
    Node() : value(), next(nullptr), prev(nullptr) {}
    // construct a node with string value, a unique_ptr to the next node, and a pointer to the previous node
    Node(const T& value, std::unique_ptr<Node<T>> next, Node<T>* prev)
        : value(value)
        , next(std::move(next))
        , prev(prev)
    {}
    // We can use the default constructor, since unique_ptr takes care of deleting memory
    ~Node() = default;
    // return the value of the node
    T getValue() const { return value; }

    // return a raw (non-owning) pointer to the next node
    Node<T>* getNext() const { return next.get(); }
    // return a raw (non-owning) pointer to the previous node
    Node<T>* getPrev() const { return prev; }

    // write the value of the node to the ostream
    friend std::ostream & operator<<(std::ostream & os, const Node<T> & node) {
      return os << node.getValue();
  }

    friend class LinkedList<T>;
};

template<typename T>
class LinkedList {
private:
    // ptr to the first node
    std::unique_ptr<Node<T>> head;
    // a raw pointer to the last node, the last node is always a dummy node
    // this is declared as a const ptr to a Node, so that tail never can
    // point anywhere else
    Node<T>* const tail;
public:
    //create the dummy node, and make tail point to it
    LinkedList()
        : head(std::make_unique<Node<T>>())
        , tail(head.get())
    {}
    ~LinkedList() = default;

    //if next is a nullptr (i.e. head is the dummy node), the list is emtpy
    bool isEmpty() const { return !head->next; }


    //return a pointer to first element
    Node<T>* begin() const { return head.get(); }
    //return a pointer to beyond-end element
    Node<T>* end() const { return tail; }

    // The insert function takes a pointer to node (pos) and a string (value). It creates a new
    // node which contains value. The new node is inserted into the LinkedList BEFORE the
    // node pointed to by pos.
    Node<T>* insert(Node<T> *pos, const T& value);

    // The find function traverses the linked list and returns a pointer to the first node
    // that contains the value given.
    // If the value isn't in the list, find returns a pointer to the dummy node at the end
    // of the list.
    Node<T>* find(const T& value);

    // The remove function takes a pointer to a node, and removes the node from the list. The
    // function returns a pointer to the element after the removed node.
    Node<T>* remove(Node<T>* pos);

    // The remove function takes a string and removes the first node which contains the value.
    void remove(const T& value);

    // write a string representation of the list to the ostream
    friend std::ostream & operator<<(std::ostream & os, const LinkedList<T>& list) {
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
};

// ===  implementation of functions
template<typename T>
Node<T>* LinkedList<T>::insert(Node<T> *pos, const T& value) {
    // make sure pos isn't nullptr (for debugging purposes)
    assert(pos);
    if (pos == begin()) { // if pos is the first node
        // create a new head node, point to the old head node
        head = std::make_unique<Node<T>>(value, std::move(head), nullptr);
        // and make the old head node point back to the new one
        pos->prev = begin();
    } else {
        // find the previous node
        auto prevNode = pos->prev;
        // make the previous node point to (and own) the new node
        prevNode->next = std::make_unique<Node<T>>(value, std::move(prevNode->next), prevNode);
        // make the given node point back to the new node
        pos->prev = prevNode->getNext();
    }
    // return a pointer to the new node
    return pos->prev;
}

template<typename T>
Node<T>* LinkedList<T>::find(const T& value) {
    // node points to the first node
    auto node = begin();
    // traverse the list untill we reach the end, ord finds the value
    while(node != end() && node->value != value) {
        // make node point to the next node
        node = node->getNext();
    }
    // return the node with the given value,
    // or end() if the value wasn't found
    return node;
}

template<typename T>
Node<T>* LinkedList<T>::remove(Node<T>* pos) {
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

template<typename T>
void LinkedList<T>::remove(const T& value) {
    // use the member method find to find the wanted node
    auto node = find(value);
    // check if the value was found
    if (node != end()) {
        // remove the node
        remove(node);
    }
}

} // namespace TemplateLinkedList

