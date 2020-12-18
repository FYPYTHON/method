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

// ��ľ�̬���ݳ�Ա��ʹ��ǰ������г�ʼ��
MySingle* MySingle::m_s = NULL;
// ���ⶨ��ľ�̬��Ա������ʹ�þ�̬��Ա��
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
