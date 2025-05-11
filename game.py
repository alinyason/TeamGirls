import random

def guess_number(input_func=input):
    number = random.randint(1, 5)  # ОШИБКА: теперь число от 1 до 5, а не до 10
    attempts = 0
    max_attempts = 3

    print("Guess a number between 1 and 10! You have 3 attempts.")  # Но пишем, что до 10

    while attempts < max_attempts:
        try:
            guess = int(input_func("Your guess: "))
            if guess < 1 or guess > 10:
                print("Number must be between 1 and 10!")
                continue

            attempts += 1

            if guess == number:
                print(f"Congratulations! You guessed it in {attempts} attempts!")
                return True
            elif guess < number:
                print("The secret number is higher.")
            else:
                print("The secret number is lower.")

        except ValueError:
            print("Please enter a number, not text!")

    print(f"Game over. The secret number was: {number}")
    return False

if __name__ == "__main__":
    guess_number()