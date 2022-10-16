#include <cs50.h> //.h = header file
#include <stdio.h>

int main(void)
{
    string name = get_string("What is your name? ");
    printf("hello, %s\n", name);
}