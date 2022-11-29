from cs50 import get_int

# Get card number
while True:
    try:
        card_number = get_int("Number: ")
        if card_number >= 0:
            break
    except ValueError:
        pass

# Luhns algorithm
# Function to check valid card num, return true or false


def luhns_algorithm(num):
    m2, not_m2 = 0, 0

    while (num != 0):
        # the not muliplied by 2 sum, starting from last value, skips 1 per iteration
        not_m2 += num % 10

        # the muliplied by 2 sum, starting from second to last value, skips 1 per iteration
        num = int(num / 10)

        m2_check = (num % 10) * 2
        if (m2_check > 9):
            digit_ones = m2_check % 10
            digit_tens = int(m2_check / 10)
            m2 += (digit_tens + digit_ones)
        else:
            m2 += m2_check
        num = int(num / 10)

    if (m2 + not_m2) % 10 == 0:
        return True
    else:
        return False


# Checking for card company and status
if (luhns_algorithm(card_number) == False):
    print("INVALID")
else:
    AMEX = [34, 37]
    MASTERCARD = [51, 52, 53, 54, 55]
    VISA = [4]
    card_num_str = str(card_number)
    first_two_nums = int(card_num_str[0] + card_num_str[1])

    # Checking card num length with str and beginning with int
    if (len(card_num_str) == 15 and (first_two_nums in AMEX)):
        print("AMEX")
    elif (len(card_num_str) == 16 and (first_two_nums in MASTERCARD)):
        print("MASTERCARD")
    elif ((len(card_num_str) == 13 or len(card_num_str) == 16) and (int(card_num_str[0]) in VISA)):
        print("VISA")
    else:
        print("INVALID")