#include <stdio.h>
#include <cs50.h>

int get_height(void);
void print_pyramid(int height);

int main(void)
{
    //assigns height from function below 
    int height = get_height();

    //print pyramid
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
        // spaces before #
        for (int space = 0; space < height - row - 1; space++)
        {
            printf(" ");
        }

        //# on left side
        for (int block = 0; block < row + 1; block++)
        {
            printf("#");
        }

        //two spaces in between 
        printf("  ");

        //repeated blocks on right side
        for (int block = 0; block < row + 1; block++)
        {
            printf("#");
        }

        printf("\n");
    }
}
