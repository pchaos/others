#include <stdio.h>
#include <string.h>

#define CMD_MAX 256

int main(char* argc, char** argv) {
    char cmd[CMD_MAX] = "/usr/bin/cat ";
    strcat(cmd, argv[1]);
    system(cmd);
}