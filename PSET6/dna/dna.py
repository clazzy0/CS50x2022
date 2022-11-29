import csv
from sys import argv


def main():

    # Check for command-line usage
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # Read database and DNA sequence files into variables
    else:
        with open(f"{argv[1]}", "r") as csvfile:
            database_file = csv.DictReader(csvfile)
            # Database list containing each dictionary
            database = []
            for row in database_file:
                database.append(row)

        with open(f"{argv[2]}", "r") as csvfile:
            sequence_file = csv.reader(csvfile)
            # Finds sequence, making it just a string
            for strand in sequence_file:
                sequence = strand[0]
                break

    # Find longest match of each STR in DNA sequence
    '''
    First finding all valuable keys needed for comparing the STR, using STR_keys
    '''
    for dict in database:
        STR_keys = list(dict.keys())[1:]
        break

    STR_values = []
    for STR in STR_keys:
        STR_values.append(longest_match(sequence, STR))

    # Check database for matching profiles
    name = "No match"
    # For one dict
    for dict in database:
        # For each strand
        counter = 0
        for i in range(len(STR_values)):
            if dict[STR_keys[i]] == str(STR_values[i]):
                counter += 1
        if counter == len(STR_keys):
            name = dict["name"]
            break
    print(name)
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()