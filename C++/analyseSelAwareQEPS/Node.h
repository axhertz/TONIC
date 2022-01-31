

#ifndef PLANCACHE_NODE_H
#define PLANCACHE_NODE_H

#include <string>
#include <map>



using namespace std;

class Node {

    string key;
    float gamma;
    //todo: use (smart) pointers instead of real nodes
    map<string,map<pair<float,float>,Node>> child_nodes;


public:
    float getSumHash();
    float getSumNest();
    float hashCost;
    float nestCost;
    int getKeyCount();
    int getMaxBranch();
    unsigned  long getSize();
    Node(string key_);
    string getKey();
    void setGamma(float gamma_);
    void addHashCost(float hashCost_);
    void addNestCost(float nestCost_);
    string getRecommended();
    Node * getNext(string key_, float selectivity_);
    void updateKey(const string& key_,float hashCost_, float nestCost_, float selectivity, bool immutable = false);
};


#endif //PLANCACHE_NODE_H
