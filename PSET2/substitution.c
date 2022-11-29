#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

string cipher(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    //integers in array representing ASCII value of letter
    int exist[26];
    string key = argv[1];

    for (int i = 0; i < 26; i++)
    {
        //uppercase - uppercase to get a spot in the array of 26
        //adds 1 if there is one occurance at that on spot
        exist[toupper(key[i]) - 'A']++;
    }

    for (int i = 0; i < 26; i++)
    {
        //if two  occurances at 1 index,
        if (exist[i] != 1)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    string plaintext = get_string("plaintext: ");
    string ciphertext = cipher(plaintext, argv[1]);
    printf("ciphertext: %s\n", ciphertext);
}

string cipher(string plaintext, string key)
{
    //creates an uppercase_keyset and lowercase_keyset
    char uppercase_key[26];
    char lowercase_key[26];
    for (int i = 0; i < strlen(key); i++)
    {
        uppercase_key[i] = toupper(key[i]);
        lowercase_key[i] = tolower(key[i]);
    }

    //switches out plaintext using key
    for (int j = 0; j < strlen(plaintext); j++)
    {
        if (plaintext[j] >= 'a' && plaintext[j] <= 'z')
        {
            int current_value_lower = plaintext[j] - 97;
            plaintext[j] = lowercase_key[current_value_lower];
        }
        else if (plaintext[j] >= 'A' && plaintext[j] <= 'Z')
        {
            int current_value_upper = plaintext[j] - 65;
            plaintext[j] = uppercase_key[current_value_upper];
        }
    }
    return plaintext;
}