/*****************************************
* Creation Date : 07-09-2011
* Last Modified : Sat Sep 17 21:10:27 2011
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : code to print document term frequency  
*****************************************/
#include"invert.hpp"
#include<iostream>
#include<fstream>
#include<streambuf>
#include<istream>
#include<iterator>
#include<sstream>
#include<functional>
#include<math.h>

typedef vector<pair<string,TermNode*> > TermNodeVector;
typedef vector<PostNode> PostNodeVector;


inline bool isDigit(std::string const& s)
 {
   std::istringstream i(s);
   float x;
   if (!(i >> x))
      return true; 
   return false;
 }

template<class T>
struct compareFunc: std::binary_function<T,T,bool>
{  
    inline bool operator()(const T& lhs, const T& rhs) {
            //cout<<lhs.second->tf<<" and "<<rhs.second->tf;
            return lhs.second->tf > rhs.second->tf;  
    }
};

InvertedIndex::~InvertedIndex() {
    delete termList;
}
struct dereferenced_less 
{ 
    template <class T> 
    bool operator () (T& x, T& y) const {return x.docIndx == y.docIndx;} 
};

InvertedIndex::InvertedIndex(int N=0) {
    this->N = N;
    termList = new map<string,TermNode*>(); 
    docs.resize(N);
}

void InvertedIndex::print() {
    TermNodeVector temp(termList->begin(),termList->end());
    for(TermNodeVector::iterator it = temp.begin(); 
                it != temp.end(); ++it) {
            cout<<"\""<<(*it).first<<cout<<"\""<<endl;
            for(PostNodeVector::iterator itb = it->second->postList.begin(); 
                    itb != it->second->postList.end() ; ++itb) {
                    cout<<"file["<<itb->docIndx<<"] Offset into File:";
                    for(list<pair<int,int> >::iterator lt = itb->range.begin(); 
                                                lt != itb->range.end(); ++lt)
                        cout<<lt->first<<"-"<<lt->second<<" ";
                    cout<<endl;
                cout<<"tfd : "<<itb->tfd<<endl; 
                }
            cout<<"tf : "<<it->second->tf<<endl; 
            cout<<endl;
    }
}
void InvertedIndex::setDelimiters(string delimts) {
    delimiters = delimts;
}

vector<string> InvertedIndex::tokenize(string& input) {
    vector<string> tokens;
    std::istringstream iss(input);
    std::copy(std::istream_iterator<string>(iss),
             std::istream_iterator<string>(),
             back_inserter(tokens));
   return tokens; 
}
void InvertedIndex::find(string& query) {
    TermNodeVector queryList;
    PostNodeVector iterList;
    PostNodeVector finalList;
    PostNodeVector tempList;
    vector<string> qTokens = tokenize(query);
    for(vector<string>::iterator qToken = qTokens.begin(); qToken != qTokens.end(); ++qToken) {
        map<string,TermNode*>::iterator it  = termList->find(*qToken);
            if(it == termList->end()){
                cout<<*qToken<<" - Term not Found"<<endl;
                return;
            } else if(it->second->isStopWord) {
                cout<<*qToken<<" - Ignoring Stop Word"<<endl;
            }
            else {
                queryList.push_back(*it);  
            }
    }
    if(queryList.size() > 1) {
        /* More than one words,merge the lists */
        TermNodeVector::iterator first = queryList.begin();
        TermNodeVector::iterator second = first + 1; 
   
        set_intersection(first->second->postList.begin(),first->second->postList.end(),
                          second->second->postList.begin(),second->second->postList.end(),
                          std::back_inserter(finalList));
        while(++second!= queryList.end()) {
            set_intersection(finalList.begin(),finalList.end(),
                          second->second->postList.begin(),second->second->postList.end(),
                          std::back_inserter(tempList));
            finalList = tempList;
        }
        iterList = finalList;
    } else if (queryList.size() == 1){
        finalList = iterList = queryList[0].second->postList;
    }

    if(queryList.size() > 1) {
        vector<pair<float,int> > sums;
         for(PostNodeVector::iterator itb = finalList.begin(); itb != finalList.end()
                                                ; ++itb) {
                float sum = 0;
                if(itb->docIndx != -1) {
                    for(TermNodeVector::iterator ft = queryList.begin();
                                            ft != queryList.end() ; ++ft) {
                        sum += ft->second->postList[itb->docIndx].tfidf;
                    }
                    sums.push_back(pair<float,int>(sum,itb->docIndx));
                }
                sort(sums.begin(),sums.end());
                for(vector<pair<float,int> >::iterator it = sums.begin(); it != sums.end(); ++it)
                    cout<<it->first<<" "<<"file:"<<it->second<<endl;
                sums.clear();
         }
    }
    else if (queryList.size() == 1){
        for(PostNodeVector::iterator itb = finalList.begin(); itb != finalList.end()
                                                ; ++itb) {
                if(itb->docIndx != -1) {
                cout<<"tf= "<<(itb)->tfd<<" df= "<<queryList[0].second->df<<" idf= "<<(itb)->idf<<" tf.idf= "<<(itb)->tfidf<<" file["<<(itb)->docIndx<<"] :"<<endl;
                for(list<pair<int,int> >::iterator lt = (itb)->range.begin(); 
                                            lt != (itb)->range.end(); ++lt) {
                   string snip;
                   if(lt == (itb)->range.begin()) {
                        snip = docs[(itb)->docIndx].substr(lt->first,lt->second - lt->first);
                        cout<<"\""<<snip<<"\""<<endl;
                } 
                   cout<<lt->first<<"-"<<lt->second<<" ";
                    
            }
                    cout<<endl;
                    cout<<endl;
                    cout<<endl;
                }
            }
    cout<<endl;
    }
}
void InvertedIndex::calcWeight() {
    for(map<string,TermNode*>::iterator it = termList->begin(); 
                it != termList->end(); ++it) {
        for(PostNodeVector::iterator itb = it->second->postList.begin(); 
                itb != it->second->postList.end() ; ++itb) {
                itb->idf = (log10(N * 1.0/ it->second->df));
               itb->tfidf = (1 + log10(itb->tfd)  ) * itb->idf; 

        }
        if(it->second->df > (N * 2.0)/3 && !it->second->isStopWord)
        { it->second->isStopWord = true;}
    }
}
void InvertedIndex::writeData() {
   TermNodeVector temp(termList->begin(),termList->end());
    sort(temp.begin(),temp.end(),compareFunc<pair<string,TermNode*> >());
    ofstream outputFile("Zipfdata.txt");

    for(TermNodeVector::iterator it = temp.begin(); 
                it != temp.end(); ++it) {
            outputFile<<it->second->tf<<" "; 
    }
    outputFile<<"\n";
}
bool InvertedIndex::buildList(string& str,int docIndx,int endOffset)
{
    int startpos = 0;
    int pos;
    string strTemp;

    transform(str.begin(), str.end(), str.begin(), ::tolower);
    pos  = str.find_first_of(delimiters, startpos);
    do
    {
        strTemp = str.substr(startpos, pos - startpos);
        if(strTemp[0] <  '0' || strTemp[0] > '9' ) {
            /* Valid word, check its already there */
            map<string,TermNode*>::iterator lb = termList->find(strTemp);
            if(lb != termList->end()) {
                TermNode *tNode = (*termList)[strTemp];
                PostNodeVector::iterator it;
                for(it = tNode->postList.begin();
                        it != tNode->postList.end() ; ++it) {
                        if(it->docIndx == docIndx)
                            break;
                }
                if(it != tNode->postList.end()) {
                    int st = (pos - 35) < 0 ? startpos: (pos - 35);
                    int end = (pos + 35) > endOffset ? endOffset: (pos + 35);     
                    (it)->range.push_back(pair<int,int>(st,end)); 
                    (it)->tfd++;
                }
                else {
                    PostNode pNode;
                    pNode.docIndx = docIndx;
                    pNode.tfd = 1;
                    int st = (pos - 25) < 0 ? startpos: (pos - 25);
                    int end = (pos + 25) > endOffset ? endOffset: (pos + 25);     
                    pNode.range.push_back(pair<int,int>(st,end)); 
                    tNode->postList[docIndx] = pNode;
                    tNode->df++;
                } 
                lb->second->tf++;
            } else {
                TermNode* tNode = new TermNode(N);
                PostNode pNode;
                
                pNode.docIndx = docIndx;
                tNode->df = tNode->tf = pNode.tfd = 1;
                int st = (pos - 25) < 0 ? startpos: (pos - 25);
                int end = (pos + 25) > endOffset ? endOffset: (pos + 25);     
                pNode.range.push_back(pair<int,int>(st,end)); 
                tNode->postList[docIndx] = pNode;
                termList->insert(make_pair(strTemp,tNode));
            }
        }

        startpos = str.find_first_not_of(delimiters, pos);
        pos = str.find_first_of(delimiters, startpos);
    } while (string::npos != pos || string::npos != startpos);
}


int main () {
    std::ifstream infile;
    int indx = 0;
    string query;
    InvertedIndex* wList = new InvertedIndex(40);
    wList->setDelimiters(string(" "));
    do {
        char filename[10];
        string fileString;
        int length = 0; 
        int endOffset = 0;
        sprintf(filename,"test/file%02d.txt",indx);
        infile.open(filename);
        if(!infile.is_open()) {
            cout<<"Please keep the test fils in \"test\" folder in the current directory"<<filename<<endl;
            /* Why not? gotos are in vogue now. */
            goto clean; 
        }

        infile.seekg(0,std::ios::end);
        endOffset = infile.tellg();
        wList->docs[indx].reserve();
        infile.seekg(0,std::ios::beg);
        wList->docs[indx].assign(std::istreambuf_iterator<char>(infile),
                        std::istreambuf_iterator<char>());
        wList->buildList(wList->docs[indx],indx,endOffset);
        infile.close();
    }while(++indx < wList->N);
    wList->calcWeight();
    wList->writeData();
    cout<<"tokenization Done"<<endl;
    cout<<"Search Box[press zzz to get out]"<<endl;
    while(query.compare("zzz") != 0) { 
        cout<<"Enter a term to search: ";
        std::getline(cin,query);
        if(query.empty()) continue;
        if(!isDigit(query)) 
            wList->print();
        else
            wList->find(query);
    }
clean:    
    delete wList;
}
