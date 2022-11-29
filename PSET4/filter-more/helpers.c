#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int rgbt = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = rgbt;
            image[i][j].rgbtGreen = rgbt;
            image[i][j].rgbtBlue = rgbt;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //tmp_image to keep for reference
    RGBTRIPLE tmp_image[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmp_image[i][j] = image[i][j];
        }
    }
    //modify old image based on tmp_image
    //different for middle value, and values on sides top bottom left right and corner cases
    //check for edge cases (corners (part of width and height = 0 or other))
    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            int counter = 0, red = 0, green = 0, blue = 0;
            //current pixel (1 out of possible 9)
            red += tmp_image[k][l].rgbtRed;
            green += tmp_image[k][l].rgbtGreen;
            blue += tmp_image[k][l].rgbtBlue;
            counter++;

            //top left (2 out of possible 9)
            if ((k - 1 >= 0) && (l - 1 >= 0))
            {
                red += tmp_image[k - 1][l - 1].rgbtRed;
                green += tmp_image[k - 1][l - 1].rgbtGreen;
                blue += tmp_image[k - 1][l - 1].rgbtBlue;
                counter++;
            }
            //top (3 out of possible 9)
            if (k - 1 >= 0)
            {
                red += tmp_image[k - 1][l].rgbtRed;
                green += tmp_image[k - 1][l].rgbtGreen;
                blue += tmp_image[k - 1][l].rgbtBlue;
                counter++;
            }
            //top right (4 out of possible 9)
            if ((k - 1 >= 0) && (l + 1 < width))
            {
                red += tmp_image[k - 1][l + 1].rgbtRed;
                green += tmp_image[k - 1][l + 1].rgbtGreen;
                blue += tmp_image[k - 1][l + 1].rgbtBlue;
                counter++;
            }
            //left (5 out of possible 9)
            if (l - 1 >= 0)
            {
                red += tmp_image[k][l - 1].rgbtRed;
                green += tmp_image[k][l - 1].rgbtGreen;
                blue += tmp_image[k][l - 1].rgbtBlue;
                counter++;
            }
            //right (6 out of possible 9)
            if (l + 1 < width)
            {
                red += tmp_image[k][l + 1].rgbtRed;
                green += tmp_image[k][l + 1].rgbtGreen;
                blue += tmp_image[k][l + 1].rgbtBlue;
                counter++;
            }
            //bottom left (7 out of possible 9)
            if ((k + 1 < height) && (l - 1 >= 0))
            {
                red += tmp_image[k + 1][l - 1].rgbtRed;
                green += tmp_image[k + 1][l - 1].rgbtGreen;
                blue += tmp_image[k + 1][l - 1].rgbtBlue;
                counter++;
            }
            //bottom (8 out of possible 9)
            if (k + 1 < height)
            {
                red += tmp_image[k + 1][l].rgbtRed;
                green += tmp_image[k + 1][l].rgbtGreen;
                blue += tmp_image[k + 1][l].rgbtBlue;
                counter++;
            }
            //bottom right (9 out of possible 9)
            if ((k + 1 < height) && (l + 1 < width))
            {
                red += tmp_image[k + 1][l + 1].rgbtRed;
                green += tmp_image[k + 1][l + 1].rgbtGreen;
                blue += tmp_image[k + 1][l + 1].rgbtBlue;
                counter++;
            }
            //manipulate pixel to blur
            image[k][l].rgbtRed = round(red / (counter * 1.0));
            image[k][l].rgbtGreen = round(green / (counter * 1.0));
            image[k][l].rgbtBlue = round(blue / (counter * 1.0));
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp_image[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmp_image[i][j] = image[i][j];
        }
    }

    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            //finding gx
            int gx_red = 0, gx_green = 0, gx_blue = 0, gy_red = 0, gy_green = 0, gy_blue = 0;

            //using previous code, but modified slightly
            //top left
            if ((k - 1 >= 0) && (l - 1 >= 0))
            {
                gx_red += -1 * tmp_image[k - 1][l - 1].rgbtRed;
                gx_green += -1 * tmp_image[k - 1][l - 1].rgbtGreen;
                gx_blue += -1 * tmp_image[k - 1][l - 1].rgbtBlue;
                gy_red += -1 * tmp_image[k - 1][l - 1].rgbtRed;
                gy_green += -1 * tmp_image[k - 1][l - 1].rgbtGreen;
                gy_blue += -1 * tmp_image[k - 1][l - 1].rgbtBlue;
            }
            //top
            if (k - 1 >= 0)
            {
                gy_red += -2 * tmp_image[k - 1][l].rgbtRed;
                gy_green += -2 * tmp_image[k - 1][l].rgbtGreen;
                gy_blue += -2 * tmp_image[k - 1][l].rgbtBlue;
            }
            //top right
            if ((k - 1 >= 0) && (l + 1 < width))
            {
                gx_red += tmp_image[k - 1][l + 1].rgbtRed;
                gx_green += tmp_image[k - 1][l + 1].rgbtGreen;
                gx_blue += tmp_image[k - 1][l + 1].rgbtBlue;
                gy_red += -1 * tmp_image[k - 1][l + 1].rgbtRed;
                gy_green += -1 * tmp_image[k - 1][l + 1].rgbtGreen;
                gy_blue += -1 * tmp_image[k - 1][l + 1].rgbtBlue;

            }
            //left
            if (l - 1 >= 0)
            {
                gx_red += -2 * tmp_image[k][l - 1].rgbtRed;
                gx_green += -2 * tmp_image[k][l - 1].rgbtGreen;
                gx_blue += -2 * tmp_image[k][l - 1].rgbtBlue;
            }
            //right
            if (l + 1 < width)
            {
                gx_red += 2 * tmp_image[k][l + 1].rgbtRed;
                gx_green += 2 * tmp_image[k][l + 1].rgbtGreen;
                gx_blue += 2 * tmp_image[k][l + 1].rgbtBlue;
            }
            //bottom left
            if ((k + 1 < height) && (l - 1 >= 0))
            {
                gx_red += -1 * tmp_image[k + 1][l - 1].rgbtRed;
                gx_green += -1 * tmp_image[k + 1][l - 1].rgbtGreen;
                gx_blue += -1 * tmp_image[k + 1][l - 1].rgbtBlue;
                gy_red += tmp_image[k + 1][l - 1].rgbtRed;
                gy_green += tmp_image[k + 1][l - 1].rgbtGreen;
                gy_blue += tmp_image[k + 1][l - 1].rgbtBlue;
            }
            //bottom
            if (k + 1 < height)
            {
                gy_red += 2 * tmp_image[k + 1][l].rgbtRed;
                gy_green += 2 * tmp_image[k + 1][l].rgbtGreen;
                gy_blue += 2 * tmp_image[k + 1][l].rgbtBlue;
            }
            //bottom right
            if ((k + 1 < height) && (l + 1 < width))
            {
                gx_red += tmp_image[k + 1][l + 1].rgbtRed;
                gx_green += tmp_image[k + 1][l + 1].rgbtGreen;
                gx_blue += tmp_image[k + 1][l + 1].rgbtBlue;
                gy_red += tmp_image[k + 1][l + 1].rgbtRed;
                gy_green += tmp_image[k + 1][l + 1].rgbtGreen;
                gy_blue += tmp_image[k + 1][l + 1].rgbtBlue;
            }
            int red = round(sqrt(pow(gx_red, 2.0) + pow(gy_red, 2.0)));
            int green = round(sqrt(pow(gx_green, 2.0) + pow(gy_green, 2.0)));
            int blue = round(sqrt(pow(gx_blue, 2.0) + pow(gy_blue, 2.0)));
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }
            image[k][l].rgbtRed = red;
            image[k][l].rgbtGreen = green;
            image[k][l].rgbtBlue = blue;
        }
    }
    return;
}