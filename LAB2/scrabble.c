#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int compute_score(string word);
void print_winner(int score1, int score2);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);
    
    // Print the winner
    print_winner(score1, score2);
}

int compute_score(string word)
{
    int total = 0;
    //set to 50 to prevent against especially long words
    char lower_word[50];

    //converts uppercase to lowercase
    for (int i = 0; i < strlen(word); i++)
    {
        //only accepts letters, uppercase and lowercase
        if (word[i] >= 'A' && word[i] <= 'Z')
        {
            lower_word[i] = tolower(word[i]);
        }
        else if (word[i] >= 'a' && word[i] <= 'z')
        {
            lower_word[i] = word[i];
        }
        else
        {
            NULL;
        }
    }

    for (int j = 0; j < strlen(word); j++)
    {
        //current_point_location changes, thus could be defined in loop
        int current_point_location = lower_word[j] - 97;
        total += POINTS[current_point_location];
    }

    return total;

}

//checks for winnner
void print_winner(int score1, int score2)
{
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie\n");
    }
}