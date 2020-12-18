#include<pthread.h>

class MyThreadLock
{
    pthread_mutex_t m_lock;
public:
    MyThreadLock(void)
    {
        Init();
    }
    ~MyThreadLock()
    {
        Close();
    }
    void Init()
    {
        pthread_mutex_init(&m_lock, NULL);
    }
    void Close()
    {
        pthread_mutex_destroy(&m_lock);
    }
    void Lock()
    {
        pthread_mutex_lock(&m_lock);
    }
    void UnLock()
    {
        pthread_mutex_unlock(&m_lock);
    }
};
class MyAutoLock
{
    MyThreadLock* m_pThreadLock;
public:
    MyAutoLock(MyThreadLock* pThreadLock)
    {
        m_pThreadLock = pThreadLock;
        if(NULL != m_pThreadLock)
		{
			m_pThreadLock->Lock();
		}
		// std::cout<<"Lock."<<std::endl;
    }
    ~MyAutoLock()
    {
        if(NULL != m_pThreadLock)
		{
			m_pThreadLock->UnLock();
		}
		//std::cout<<"UnLock."<<std::endl;
    }
};
