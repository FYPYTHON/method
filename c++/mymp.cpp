#include<iostream>
#include<ctime>
#include<cstdlib>  // 随机数 rand()
#include<mem.h>    // memcpy
#define DEL_PTR(p) if(p) delete p; p=NULL;
#define DEL_PTR_ARRAY( p ) if(p) delete [] p; p = NULL;
#define varName(x) #x

#define MaxArray 5
#define MaxData 100
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
    char* p;
    size_t len;
public:
    PointerInfo():p(NULL),len(0){}
    PointerInfo(char* p1, size_t len1):p(p1),len(len1){
        cout<<"PointerInfo()"<<endl;
    }
    ~PointerInfo(){
        DEL_PTR(p);
        cout<<"~PointerInfo()"<<endl;
    }
    char* getPointer(){
        return p;
    }
    size_t getLen(){
        return len;
    }
    void pfprint(){ cout<<"pointer info:"<<p<<","<<len<<endl;}
    void setPointer(char* p1){ p = p1;}
    void setLen(const size_t len1){ len = len1;}
};


class MemPool
{
    PointerInfo* pflist;
    char* mp;
// public:
    static size_t offset;
    static size_t pos;
public:
    MemPool()
    {
        if(pflist == NULL)
        {
            pflist = new PointerInfo[MaxArray];
        }
        if(mp == NULL)
        {
            mp = new char[MaxData];
        }
        cout<<"MemPool()"<<endl;

    }
    ~MemPool()
    {
        DEL_PTR_ARRAY(pflist);
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
    int writeData(char* data, size_t datalen)
    {
        if((offset + datalen) > MaxData)
        {
            tprint("no enough memory to write data.");
            return 1;
        }
        memcpy(mp+offset, data, datalen);
        cout<<"mp data:"<<mp+offset<<endl;
        cout<<"dd: "<< data<<"\tnow offset:"<<offset<<endl;
        (pflist+pos)->setPointer(mp+offset);
        (pflist+pos)->setLen(datalen);
        //pflist[pos]->setPointer(mp+offset);
        //pflist[pos]->setLen(datalen);
        offset += datalen+1;
        pos++;

        return 0;
    }
};
size_t MemPool::pos = 0;
size_t MemPool::offset = 0;

int main()
{
    /*
    double start_time = 0.0f, end_time = 0.0f;
    std::cout<<"----" << endl;
    std::cout<<start_time<<","<<end_time<<endl;
    char* summary = "mypp.cpp start...";
    pprint(summary);

    start_time = clock();


    end_time = clock();
    tprint(end_time - start_time);
    tprint(MaxArray, varName(MaxArray));

    initSeed();
    for(size_t i=0;i<10;i++)
    {
        size_t n1 = getRandNum();
        tprint(n1);
    }
    char a[20];
    tprint(getRandStr(a, 16), "getRandStr");
    */
    MemPool* mymp = new MemPool();
    tprint(sizeof(*mymp), "mymp");
    cout<<"offset:"<<mymp->getOffset() <<endl;
    initSeed();
    while (mymp->getOffset() < MaxData)
    {

        size_t slen = getRandNum();
        char data[20];
        getRandStr(data, slen);
        // tprint(slen,"slen");
        if ((mymp->getOffset() + slen) > MaxData)
        {
            break;
        }
        if(mymp->writeData(data, slen))
        {
            cout << "error write data." <<endl;
            break;
        }

    }
    cout<<"---over-----"<< endl;
    //tprint(MemPool::offset, "offset");
    //tprint(mymp->getMPV(), "mp");
    PointerInfo* pflist = mymp->getPFL();
    for(size_t i=0;i < MaxArray; i++)
    {
        (pflist+i)->pfprint();
    }
    mymp->~MemPool();

}
