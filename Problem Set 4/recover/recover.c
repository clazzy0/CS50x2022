#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (!(argc == 2))
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[BLOCK_SIZE];
    int jpg_counter = 0;
    char jpeg[8];
    FILE *image = NULL;

    while (fread(buffer, 1, BLOCK_SIZE, input) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpg_counter > 0)
            {
                fclose(image);
            }

            sprintf(jpeg, "%03i.jpg", jpg_counter);
            image = fopen(jpeg, "w");

            fwrite(&buffer, BLOCK_SIZE, 1, image);
            jpg_counter++;
        }
        else if (jpg_counter > 0)
        {
            fwrite(&buffer, BLOCK_SIZE, 1, image);
        }
    }
    fclose(input);
    fclose(image);
}