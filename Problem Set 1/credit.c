#include <cs50.h>
#include <stdio.h>
#include <math.h>

long long card_num(void);
int LuhnsAlgorithm(long long card_number);
void card_company(long long card_number, int checksum);

int main(void)
{
    //possible card number
    long long card_number = card_num();

    //returns either 0 (true) or 1 (false) of whether card num works using Luhn's Algorithm
    int check_card = LuhnsAlgorithm(card_number);

    //prints card company
    card_company(card_number, check_card);
}

long long card_num(void)
{
    long long card_number;
    do
    {
        card_number = get_long_long("Number: ");
    }
    while (card_number <= 0);
    //returns only a possible card num
    return card_number;
}

int LuhnsAlgorithm(long long card_number)
{
    int m2 = 0, not_m2 = 0;

    while (card_number != 0)
    {
        //the not muliplied by 2 sum, starting from last value, skips 1 per iteration
        not_m2 += card_number % 10;
        //the muliplied by 2 sum, starting from second to last value, skips 1 per iteration
        card_number /= 10;
        int m2_check = (card_number % 10) * 2;
        if (m2_check > 9)
        {
            int digit_ones = m2_check % 10;
            int digit_tens = m2_check / 10;
            m2 += digit_tens += digit_ones;
        }
        else
        {
            m2 += m2_check;
        }
        card_number /= 10;
    }

    if ((m2 + not_m2) % 10 == 0)
    {
        return 0; //true
    }
    else
    {
        return 1; //false
    }
}

void card_company(long long card_number, int check_card)
{
    //AMEX = size: 15 and start 34 or 37, MC = size: 16 and start 51, 52, 53, 54, 55, Visa = size: 13 or 16 and start 4
    long long thirteen_digit = pow(10, 12);
    long long fourteen_digit = pow(10, 13);
    long long fifteen_digit = pow(10, 14);
    long long sixteen_digit = pow(10, 15);
    long long seventeen_digit = pow(10, 16);
    //validate if card_number follows Luhn's Algorithm
    if (check_card == 1)
    {
        printf("INVALID\n");
    }
    else if (card_number >= fifteen_digit && card_number < sixteen_digit && (card_number / fourteen_digit == 34
             || card_number / fourteen_digit == 37))
    {
        printf("AMEX\n");
    }
    else if (card_number >= sixteen_digit && card_number < seventeen_digit && (card_number / fifteen_digit == 51
             || card_number / fifteen_digit == 52  || card_number / fifteen_digit == 53 || card_number / fifteen_digit == 54
             || card_number / fifteen_digit == 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((card_number >= thirteen_digit && card_number < fourteen_digit && (card_number / thirteen_digit == 4))
             || (card_number >= sixteen_digit && card_number < seventeen_digit && (card_number / sixteen_digit == 4)))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}