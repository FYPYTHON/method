// g++ -o libpyc.so -shared -fPIC pyctest.cpp
#include <iostream>
#include <memory.h>
using namespace std;
#define CCALL extern "C"

typedef struct KeyValue
{
	KeyValue()
	{
		memset(achKey, 0, sizeof(achKey));
		memset(achValue, 0, sizeof(achValue));
		nLen = 0;
	}
	char achKey[1024];
	char achValue[1024];
	int  nLen;
}TKeyValue;
CCALL int add(int &a, int b)
{
  cout<<"add: \n input args:" << a << "," <<b << endl;
  return a+b;
}
CCALL float sub(float *num1, float num2)
{
    cout << "sub:\n input args:" << *num1 << "," << num2 << endl;
    float sub_res = num2 - *num1;
    cout << sub_res << endl;
    return sub_res;
}
CCALL TKeyValue GetKeyValue(TKeyValue kv)
{
    char testkey[100] = "TEST_KEY";
    char testval[100] = "TEST_VALUE";
    memcpy(kv.achKey, testkey, sizeof(testkey));
    memcpy(kv.achValue, testval, sizeof(testval));
//    kv.achKey = "TEST_KEY";
//    kv.achValue = "TEST_VALUE";
    kv.nLen = 99;
    return kv;
}