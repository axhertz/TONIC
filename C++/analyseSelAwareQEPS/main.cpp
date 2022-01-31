#include <iostream>
#include "Node.h"
#include <fstream>
#include <vector>
#include <sstream>
#include <experimental/filesystem>
#include <regex>
#include <chrono>
#include <iomanip>

namespace fs = std::experimental::filesystem;
using namespace std;


vector<std::string> split(const string& subject)
{
    istringstream ss{subject};
    using StrIt = std::istream_iterator<std::string>;
    vector<std::string> container{StrIt{ss}, StrIt{}};
    return container;
}


double run_trace(string path, Node & planCache){

    ifstream ifs(path);

    string line;
    double time  = 0;
    Node dummyNode("dummy_root");
    Node * reference_branch = &planCache;
    Node * dummy_branch = &planCache;
    vector<string> params;
    while (std::getline(ifs, line)){

       // cout<<line<<endl;
        auto t1 = std::chrono::high_resolution_clock::now();
            if (line.find("start") != string::npos || line.find("reference_branch = plan_cache") != string::npos) {
            reference_branch = &planCache;
        } else if (line.find("dummy_branch = reference_branch getNext") != string::npos ){
            params =  split(line);
            dummy_branch = reference_branch->getNext(params[4],stof(params[5]));
            if (dummy_branch->getKey() == "dummy") {
                delete (dummy_branch);
                dummy_branch = &dummyNode;
            }
        }else if (line.find("dummy_branch getRecommended") != string::npos){
            dummy_branch->getRecommended();
        }else if (line.find("reference_branch updateKey") != string::npos){
            params =  split(line);
            bool immutable = ("True" == params[6]);
            reference_branch->updateKey(params[2],stof(params[3]),stof(params[4]), stof(params[5]), immutable);

        } else if (line.find("reference_branch = reference_branch getNext") != string::npos ) {
            params = split(line);
            reference_branch = reference_branch->getNext(params[4], stof(params[5]));
        } else{
            cout<<line<<endl;
            cout<<"unsuccessful"<<endl;
            return -1;
        }
        auto t2 = std::chrono::high_resolution_clock::now();
        time += std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count() ;
    }

    return  time;
}

int main() {

    cout<<" ### analyse selectivity-aware QEP-S: "<<endl;
    Node qeps("root");
    double updateTime, lookupTime;

    for(int i = 0; i < 1000; i++){
    updateTime += run_trace("./analyseSelAwareQEPS/selAwareTrace/sel_aware_trace_1.txt", qeps);
    }
    updateTime = updateTime/1000;

    cout<<"nodes: "<< std::setw(18)<<qeps.getKeyCount()<<endl;

    for(int i = 0; i < 1000; i++){
    lookupTime += run_trace("./analyseSelAwareQEPS/selAwareTrace/sel_aware_trace_2.txt", qeps);
    }
    lookupTime = lookupTime/1000;

    cout << "size: " << std::setw(17) << qeps.getSize()/1000.0 << "KB " <<endl;
    cout << "maintenance: " <<std::setw(10)<< updateTime/1000.0<<"ms"<<endl;
    cout << "usage (lookup): "<<std::setw(7)<< lookupTime/1000.0<<"ms"<<endl;


}


