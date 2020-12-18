#include<iostream>

class MySingle
{
public:
    static MySingle* create();
    static void destory(MySingle* mys);
    /*
    MySingle* create()
    {
        if(m_s){
            return m_s;
        } else {
            m_s = new MySingle();
            return m_s;
        }
    }
    */
private:
    MySingle();
    ~MySingle();
    static MySingle* m_s;

};

// 类的静态数据成员在使用前必须进行初始化
MySingle* MySingle::m_s = NULL;
// 类外定义的静态成员函数，使用静态成员。
MySingle* MySingle::create()
{
    if(MySingle::m_s)
    {
        std::cout<<"is exist"<<std::endl;
        return MySingle::m_s;
    }
    MySingle::m_s = new MySingle();
    return MySingle::m_s;
}

void MySingle::destory(MySingle* mys)
{
    if(mys){
        delete mys;
        mys = NULL;
    }
}
MySingle::MySingle()
{
    std::cout<<"construct"<<std::endl;

}
MySingle::~MySingle()
{
    std::cout<<"desconstruct"<<std::endl;
}
int main()
{

    MySingle *a = MySingle::create();
    MySingle *b = MySingle::create();
    MySingle *c = MySingle::create();
    std::cout<<"a="<<a<<std::endl
             <<"b="<<b<<std::endl
             <<"c="<<c<<std::endl;
    MySingle::destory(a);
    return 0;
}
