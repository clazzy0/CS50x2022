#include <stdio.h>
#include <cs50.h>

int get_height(void);
void print_pyramid(int height);

int main(void)
{
    //instead of do while loop
    int height = get_height();

    //print grid
    print_pyramid(height);
}

int get_height(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    return height;
}

void print_pyramid(int height)
{
    //number of rows
    for (int row = 0; row < height; row++)
    {
        // space
        for (int space = 0; space < height - row - 1; space++)
        {
            printf(" ");
        }

        //#
        for (int block = 0; block < row + 1; block++)
        {
            printf("#");
        }

        printf("\n");
    }
}
