
#include "Node.h"


using namespace std;

Node::Node(string key_):key(key_), hashCost(0), child_nodes(), nestCost(0),gamma(1){
}

string Node::getKey() {
    return key;
}

void Node::setGamma(float gamma_) {
    gamma = gamma_;
}

void Node::addHashCost(float hashCost_) {
    hashCost = gamma*hashCost+hashCost_;
}

void Node::addNestCost(float nestCost_) {
    nestCost = gamma*nestCost+nestCost_;
}

string Node::getRecommended() {
    if(hashCost <= nestCost){
        return "HashJoin";
    } else{
        return "NestLoop";
    }
}


float Node::getSumHash(){
    float sumHash = hashCost;
    for(auto & iter : child_nodes){
            sumHash += iter.second.getSumHash();

    }
    return  sumHash;
}

float Node::getSumNest(){
    float sumNest = nestCost;
    for(auto & iter : child_nodes){
            sumNest += iter.second.getSumNest();

    }
    return  sumNest;
}

int Node::getKeyCount(){
    int key_count = 1;
    for(auto & iter : child_nodes){
            key_count += iter.second.getKeyCount();
        }
    return  key_count;
}


Node * Node::getNext(string key_) {
    if (child_nodes.find(key_)==child_nodes.end()) {
        Node tempNode(key_);
        Node * tempNodePtr = &tempNode;
        return  new Node("dummy");

    }
    Node* nextNode = &child_nodes.find(key_)->second;
    return  nextNode;
}



void Node::updateKey(const string & key_, float hashCost_, float nestCost_) {
    if (child_nodes.find(key_) == child_nodes.end()) {
        Node newNode(key_);
        newNode.addHashCost(hashCost_);
        newNode.addNestCost(nestCost_);
        child_nodes.insert(pair<string, Node>(string(key_), newNode));
        return;
    }
    child_nodes.find(key_)->second.addHashCost(hashCost_);
    child_nodes.find(key_)->second.addNestCost(nestCost_);
}


unsigned long Node::getSize() {
    unsigned long size = sizeof(child_nodes);
    size += sizeof(hashCost);
    size += sizeof(nestCost);
    for (auto child: child_nodes){
        size += sizeof(char)*child.first.size()+sizeof(string);
        size += child.second.getSize();

    }
    return size;
}
