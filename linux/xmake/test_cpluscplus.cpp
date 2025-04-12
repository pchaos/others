#include <iostream>
#Modified : 2025 - 04 - 12 22 57 : 50

using namespace std;
int main() {
  cout << "Hello World" << endl;
  // __cplusplus 的值表示当前 C++ 标准的版本号：
  // 199711L：C++98 或 C++03
  // 201103L：C++11
  // 201402L：C++14
  // 201703L：C++17
  // 202002L：C++20
  cout << __cplusplus << endl;
  return 0;
}
