from cs50 import get_string

# Get text
text = get_string("Text: ")

# Letter count
letters = 0
invalid = [" ", ".", "?", "!", ":", ",", '"', "'"]
for i in text:
    if i not in invalid:
        letters += 1

# Word count
words = 1
for i in text:
    if i == " ":
        words += 1

# Sentence count
sentences = 0
check = [".", "!", "?"]
for i in text:
    if i in check:
        sentences += 1

# CHECK
# print(f"{letters} letters")
# print(f"{words} words")
# print(f"{sentences} sentences")


L = letters / words * 100
S = sentences / words * 100

index = 0.0588 * L - 0.296 * S - 15.8

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {int(round(index))}")