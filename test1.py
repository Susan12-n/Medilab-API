def add(num1, num2):
    answer = num1 + num2
    print("The answer is:",answer)

# add(2, 3)


def BMI(weight, height):
    bmi = weight / (height*height)
    print("Your BMI is:",bmi)

# BMI(80, 1.92)

def area(pi , radius):
    area = pi * radius * radius
    print("The area is:",area)

# area(3.142, 14)

# def check():
#     x= 50
#     y = 30

#     if x > y:
#         print("X is greater than y")
#     else:
#         print("x is less than y")


# check()

def check(x,y):
    if x > y:
        print("X is greater than y")

    else:
        print("x is less than y")

# check(50,30)

def check (x,y,z):
    if x > y and x > z:
        print("x is largest")
    elif x < y and y> z:
        print(" Y is gratest")
    else:
        print("z is gratest")


# check(50, 20 ,30)
        

#function to check if number is odd or even
def find(number):
 
    if number %2 != 0:
        print( number," is an odd number")
    else:
        print(number, "is an even number")

find(3)

import random
def number(n=6, start=1, end=9):
    return random.sample(range(start,end+1),n)

random_number = number()
print(random_number)

import re

def phone(phone_number):
    # Simplified regular expression to match Kenyan phone numbers
    regex = r"^07[0-9]{8}$|^\+254\d{9}"

    # Check if the phone number matches the regex pattern
    return re.match(regex, phone_number) is not None

# Example usage:
phone_number = "+254719345679"
if phone(phone_number):
    print(f"The phone number {phone_number} is in correct Kenyan format.")
else:
    print(f"The phone number {phone_number} is not in correct Kenyan format.")

