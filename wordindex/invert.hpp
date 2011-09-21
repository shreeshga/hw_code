/*****************************************
* Creation Date : 07-09-2011
* Last Modified : Sat Sep 17 21:40:43 2011
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : code to print document term frequency  
*****************************************/
#include<string>
#include<vector>
#include<map>
#include<iostream>
#include<list>
#include<utility>
using std::map;
using std::vector;
using std::list;
using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::pair;
using std::ofstream;

class PostNode {
    public:
    int docIndx; // Index into InvertedIndex::docs
    //list<string> snippets; //holds  range of letters from doc.
    list<pair<int,int> > range;
    float tfd;
    float tfidf;
    float idf;
    bool operator< ( const PostNode& rhs ) const
    {
        return docIndx < rhs.docIndx;
    }
    
};

class TermNode {
public:
   vector<PostNode> postList;
   bool isStopWord;
   float wt;
   float tf;
   float df;
   

   TermNode() { isStopWord = false;}
   TermNode(int N) { postList.resize(N);
                   for(vector<PostNode>::iterator it = postList.begin();
                        it != postList.end() ; ++it) 
                        it->docIndx = -1; 
       isStopWord = false;}
   TermNode (const TermNode& other);
   ~TermNode();
};

class  InvertedIndex {
    public: 
        map<string, TermNode*> *termList;
        vector<string> docs; 
        string delimiters; 
        int N;
    public:
        InvertedIndex(int N);
        ~InvertedIndex();
        void setDelimiters(string delimts);
        void updateInvertedList();
        void find(string& query);
        void print();
        void calcWeight(); 
        vector<string> tokenize(string& input);
        list<TermNode> searchWords(string words,...);
        bool buildList(string& str,int docIndx,int endOffset);
        void writeData();
};
