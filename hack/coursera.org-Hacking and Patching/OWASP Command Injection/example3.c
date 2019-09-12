#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
/*
不兼容的编译错误内置函数'execl'
缺少“系统” 的#include头限定execl（即在Linux <unistd.h>）。

要了解包含的内容，请使用gcc -H -c foo.c并使用gcc -C -E -Wall foo.c > foo.i获取预处理表单。

*/

#define INITCMD "ls"

int main(char* argc, char** argv) {
   char* home=getenv("APPHOME");
   char* cmd=(char*)malloc(strlen(home)+strlen(INITCMD));
   if (cmd) {
           strcpy(cmd,home);
           strcat(cmd,INITCMD);
           execl(cmd, NULL);
   }
  }