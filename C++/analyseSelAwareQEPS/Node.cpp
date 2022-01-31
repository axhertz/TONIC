
#include "Node.h"
#include <iostream>


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
        for (auto & iter2 : iter.second) {
            sumHash += iter2.second.getSumHash();
        }
    }
    return  sumHash;
}

float Node::getSumNest(){
    float sumNest = nestCost;
    for(auto & iter : child_nodes){
        for (auto & iter2 : iter.second) {
            sumNest += iter2.second.getSumNest();
        }
    }
    return  sumNest;
}

int Node::getKeyCount(){
    int key_count = 1;
    for(auto & iter : child_nodes){
        for (auto & iter2 : iter.second) {
            key_count += iter2.second.getKeyCount();
        }
    }
    return  key_count;
}

int Node::getMaxBranch(){
    int branch_cnt = 0;
    if (child_nodes.size() > branch_cnt){
        branch_cnt = child_nodes.size();
    }
    for(auto & iter : child_nodes){
        if (iter.second.size() > branch_cnt){
            branch_cnt =iter.second.size();
        }
        for (auto & iter2 : iter.second) {
            int testB = iter2.second.getMaxBranch();
            if(testB> branch_cnt){
                branch_cnt = testB;
            }
        }
    }
    return  branch_cnt;
}


Node * Node::getNext(string key_, float selectivity_) {
    if (child_nodes.find(key_)==child_nodes.end()) {
        Node tempNode(key_);
        return  new Node("dummy");
    }

    Node* nearestNode = nullptr;
    pair<float,float> theIntervall;
    float proximity  =1;
    for (auto & iter : child_nodes[key_]) {
        if (min(abs(selectivity_-iter.first.first),abs(selectivity_-iter.first.second)) < proximity){
            proximity = min(abs(selectivity_-iter.first.first),abs(selectivity_-iter.first.second));
            nearestNode = &iter.second;
            theIntervall = make_pair(iter.first.first,iter.first.second);
        }
    }

    if (nearestNode != nullptr){
        return nearestNode;
    }

    return  new Node("dummy");
}



void Node::updateKey(const string& key_, float hashCost_, float nestCost_, float selectivity, bool immutable) {
    if (child_nodes.find(key_)==child_nodes.end()){
        Node newNode(key_);
        newNode.addHashCost(hashCost_);
        newNode.addNestCost(nestCost_);
        map<pair<float, float>, Node> newPath;
        if (immutable){// immutable: join sub-query node instead of single relation
            newPath.insert(pair<pair<float,float>,Node>(make_pair(0,1),newNode));
        } else{
            newPath.insert(pair<pair<float,float>,Node>(make_pair(selectivity,selectivity),newNode));
        }
        child_nodes[key_] = newPath;
        return;
    }
    Node* nearestNode = nullptr;
    pair<float,float> theIntervall;
    float proximity  =1;
    for (auto & iter : child_nodes[key_]) {
        if (iter.first.first <= selectivity && iter.first.second >= selectivity){
            iter.second.addHashCost(hashCost_);
            iter.second.addNestCost(nestCost_);
            return;
        }
        if (min(abs(selectivity-iter.first.first),abs(selectivity-iter.first.second)) < proximity){
           // cout<<"update node with closest proximity"<<endl;
            proximity = min(abs(selectivity-iter.first.first),abs(selectivity-iter.first.second));
            nearestNode = &iter.second;
            theIntervall = make_pair(iter.first.first,iter.first.second);
        }
    }

    if (nearestNode != nullptr){
        if((nearestNode->getRecommended()=="HashJoin" && hashCost_ <= nestCost_ )||
           (nearestNode->getRecommended()=="NestLoop" && nestCost_ <= hashCost_) || abs(nestCost_-hashCost_)< 0.01){


            nearestNode->addHashCost(hashCost_);
            nearestNode->addNestCost(nestCost_);

            auto nodeHandler = child_nodes[key_].extract(theIntervall);
            nodeHandler.key() = make_pair(min(selectivity, theIntervall.first), max(selectivity, theIntervall.second));
            child_nodes[key_].insert(move(nodeHandler));

            child_nodes[key_].erase(theIntervall);
            return;
        }
    }

    Node newNode(key_);
    newNode.addHashCost(hashCost_);
    newNode.addNestCost(nestCost_);

    child_nodes[key_].insert(pair<pair<float,float>,Node>(make_pair(selectivity,selectivity),newNode));

}

unsigned long Node::getSize() {
    unsigned long size = sizeof(child_nodes);
    size += sizeof(nestCost);

    for (auto child: child_nodes){
        size += sizeof(child.first);
        size += sizeof(child.second);
        for (auto interval: child.second){
            size += sizeof(interval.first);
            size += sizeof(interval.first.first);
            size += sizeof(interval.first.second);
            size += interval.second.getSize();
        }
    }
    return size;
}
