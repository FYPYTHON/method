#include<iostream>
#include<ctime>
#include<cstdlib>  // 随机数 rand()
#include<memory.h>    // memcpy
#include "mythreadlock.h"


#define DEL_PTR(p) if(p) delete p; p=NULL;
#define DEL_PTR_ARRAY( p ) if(p) delete [] p; p = NULL;
#define varName(x) #x

#define MaxArray 8000
#define MaxData  100000
using std::cout;
using std::endl;
void pprint(char* p)
{
    cout<<p<<"  地址"<<static_cast<void*>(p)<<endl;
}
template <typename T>
void tprint(T t, const char* varname = "")
{
    cout<<varname<<":"<<t<<endl;
}
void initSeed()
{
    unsigned seed;
    seed = time(0);
    srand(seed);
}
size_t getRandNum()
{
    int maxValue = 16;
    int minValue = 5;
    size_t number = (rand()%(maxValue - minValue +1)) + minValue;
    return number;
}
char *getRandStr(char* str,const int len)
{
    // srand(time(NULL));
    int i;

    for (i = 0; i < len; ++i)
    {
        switch ((rand() % 3))
        {
        case 1:
            str[i] = 'A' + rand() % 26;
            break;
        case 2:
            str[i] = 'a' + rand() % 26;
            break;
        default:
            str[i] = '0' + rand() % 10;
            break;
        }
    }
    str[++i] = '\0';
    return str;
}

class PointerInfo
{
    size_t p;
    size_t len;
public:
    PointerInfo():p(0),len(0)
    {
        // cout<<"PointerInfo()"<<endl;
    }
    PointerInfo(size_t p1, size_t len1):p(p1),len(len1){
        // cout<<"PointerInfo()"<<endl;
    }
    ~PointerInfo(){
        // cout<<"~PointerInfo()"<<endl;
    }
    size_t getPointer()
    {
        return p;
    }
    size_t getLen()
    {
        return len;
    }
    void pfprint(){ cout<<"pointer info:"<<len<<","<<p<<endl;}
    void setPointer(const size_t p1){ p = p1;}
    void setLen(const size_t len1){ len = len1;}
};


class MemPool
{
    PointerInfo* pflist;
    char* mp;
// public:
    static size_t offset;
    static size_t pos;

    MyThreadLock mp_lock;
    size_t rounds;
public:
    MemPool():pflist(NULL),mp(NULL),rounds(0)
    {
        if(pflist) DEL_PTR_ARRAY(pflist);
        if(mp) DEL_PTR_ARRAY(mp);

        if(pflist == NULL)
        {
            cout<<"MemPool() pflist"<<endl;
            pflist = new PointerInfo[MaxArray];
        }
        if(mp == NULL)
        {
            cout<<"MemPool() mp"<<endl;
            mp = new char[MaxData];
            // memset(mp, 0, MaxData*sizeof(char));
        }
        // cout<<"MemPool()"<<endl;

    }
    ~MemPool()
    {
        DEL_PTR_ARRAY(pflist);
        //cout<<"free pflist ok"<<endl;
        DEL_PTR_ARRAY(mp);
        cout<<"~MemPool()"<<endl;
    }

    size_t getOffset(){return offset;}
    size_t getPos(){return pos;}
    char* getMPV()
    {
        return mp;
    }
    PointerInfo* getPFL()
    {
        return pflist;
    }
    void printMP()
    {
        cout<<"mp:";
        for(size_t i=0;i<MaxData;i++)
        {
            cout<<*(mp+i);
        }
        cout<<endl;
    }
    int writeData(char* data, size_t datalen)
    {
        MyAutoLock mplock(&mp_lock);  // thread lock
        if((offset + datalen) > MaxData)
        {
            tprint("no enough memory to write data.");
            // cout<<"offset + datalen:"<<offset + datalen<<endl;
            rounds++;
            if(rounds > 1)
            {
                cout<<"1 rounds. then break"<<endl;
                return 1;
            }
            else
            {
                cout << "\t";
                cout << rounds << " rounds ..." << endl;
                offset = 0;
                pos = 0;
            }

        }

        if(pos > MaxArray - 1)
        {
            pos = 0;
            cout << "\t";
            cout << pos << " new pos start ..." << endl;
        }

        memcpy(mp + offset, data, datalen);

        // cout<<"pos:"<<pos<<",offset:"<<offset<<",mp data:"<<mp+offset<<endl;

        // (pflist+pos)->setPointer(mp+offset);
        (pflist+pos)->setPointer(offset);
        (pflist+pos)->setLen(datalen);

        offset += datalen;
        pos++;


        return 0;
    }
};
size_t MemPool::pos = 0;
size_t MemPool::offset = 0;

int main()
{
    float starttime=.0f, endtime=.0f;
    starttime = clock();
    MemPool* mymp = new MemPool();
    tprint(sizeof(*mymp), "mymp");

    initSeed();

    while (mymp->getOffset() + 1 < MaxData)
    {

        size_t slen = getRandNum();
        char data[20] = {'0'};
        getRandStr(data, slen);

        // cout <<"rand data:"<< data << "," <<slen<<endl;

        if(mymp->writeData(data, slen + 1))
        {
            cout << "error write data." <<endl;
            break;
        }

    }

    cout<<"---over-----"<< endl;
    cout<<"offset:"<<mymp->getOffset() <<",pos:"<<mymp->getPos()<<endl;

    // tprint(mymp->getMPV(), "mp");

    PointerInfo* pflist = mymp->getPFL();
    for(size_t i=0;i < MaxArray; i++)
    {
        if((pflist+i)->getLen()> 0){

            // size_t pos = (pflist+i)->getPointer();
            // cout<<mymp->getMPV() + pos<<endl;
        }
        else
        {
            // cout<< i <<" no pointer"<<endl;
        }

    }
    // cout<<"offset:"<<mymp->getOffset() <<",pos:"<<mymp->getPos()<<endl;
    cout<<"go free"<<endl;
    // mymp->printMP();
    delete mymp;
    endtime = clock();
    cout<<"used:" << endtime - starttime << endl;
    //mymp->~MemPool();

}
