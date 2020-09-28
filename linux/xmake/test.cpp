#include<string>
#include "fmt/format.h"
#include "config.h"
using namespace std;
using namespace fmt;

int main(int argc, char** argv)
{
    auto hello = "你好？"s;
    print("hello {}\n",hello);
    //輸出 hello 你好?
    
    auto name = "Alan"s;
    print("{0} is playing {1}", name, "balls");
    // 輸出 Alan is playing balls
    
    //也可以將1-n個數值變成String，用以取代stringstream
    auto s = format("{0} {1}     {2}",12,55,22);
    print("{0}",s);
    //輸出是 12 55     22
    
    return 0;
}
