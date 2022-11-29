#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
void print_index(float letters, float word_count, float sentence_count);

int main(void)
{
    string input_text = get_string("Text: ");

    int letter_count = count_letters(input_text);
    int word_count = count_words(input_text);
    int sentence_count = count_sentences(input_text);

    print_index(letter_count, word_count, sentence_count);
}

int count_letters(string text)
{
    int total_letters = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            total_letters += 1;
        }
        else if (text[i] >= 'A' && text[i] <= 'Z')
        {
            total_letters += 1;
        }
    }

    return total_letters;
}

int count_words(string text)
{
    //period can be ignored when calculating words because there will still be a space between two sentences
    int total_words = 1;

    for (int j = 0; j < strlen(text); j++)
    {
        if (text[j] == ' ')
        {
            total_words += 1;
        }
    }

    return total_words;
}

int count_sentences(string text)
{
    int total_sentences = 0;

    for (int n = 0; n < strlen(text); n++)
    {
        if (text[n] == '.' || text[n] == '?' || text[n] == '!')
        {
            total_sentences += 1;
        }
    }
    return total_sentences;
}

//changed to float so computations work
void print_index(float letter_count, float word_count, float sentence_count)
{
    //Coleman-Liau index to calculate grade level based on text
    float grade_level = 0.0588 * (letter_count / word_count) * 100 - 0.296 * (sentence_count / word_count) * 100 - 15.8;

    //rounded using math.h
    int grade_level_rounded = roundf(grade_level);

    if (grade_level_rounded < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade_level_rounded >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade_level_rounded);
    }
}
