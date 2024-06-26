import csv
import sys
import random
import cowsay
from tabulate import tabulate
from pyfiglet import Figlet
from termcolor import colored
from time import sleep


# Class to represent each country and its attributes
class Country:
    def __init__(self, name, area, population, alt_spellings=None):
        self.name = name
        try:
            self.area = "{:,} km\u00B2".format(int(area))
        except ValueError:
            self.area = "{} km\u00B2".format(area)
        self.population = "{:,}".format(int(population))
        self.alt_spellings = alt_spellings
        with open(
            f"/workspaces/125834830/Final Project/ASCII art generation/ascii.txt files/{self.name}_ascii.txt"
        ) as file:
            self.ascii = file.read()

    def __str__(self):
        return f"\n{self.ascii}\n"


def main():
    initialise_countries()
    difficulty, num_questions = menu()
    questions(difficulty, num_questions)


# initialise all the country object instances
def initialise_countries():
    countries_data = []
    with open("Country Data.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            countries_data.append(row)

    # Create dictionary with country name as key and country object as value, global as we want to access this in other functions
    global country_obj_dict
    country_obj_dict = {}
    for country in countries_data:
        country_obj_dict[country["name"]] = Country(
            country["name"],
            country["area"],
            country["population"],
            country["alternate_spellings"].split(","),
        )
    # Useful to have a golbal list of the countries/keys
    global country_list
    country_list = list(country_obj_dict.keys())


# Start menu to select difficulty level, num questions etc.
def menu():
    f = Figlet()
    f.setFont(font="big")
    print(
        colored(f.renderText("European Country Outline Quiz!"), "red", attrs=["bold"])
    )
    print(
        colored(
            "Instructions:\n1. Type skip at any time to skip question. You will avoid losing a life but will not score a point for that question.\n\
2. When you run out of lives its game over!\n3. Press ctrl + c at any time to quit!\n4. Have fun!\n\n",
            "grey",
        )
    )
    options = [
        ["1. Easy (hints + unlimited lives)"],
        ["2. Normal (10 lives)"],
        ["3. Hard (1 life + no skips)"],
    ]
    table = tabulate(
        options, ["Please select difficulty level"], tablefmt="rounded_grid"
    )
    print(colored(table, "blue", attrs=["bold"]) + "\n")
    while True:
        try:
            diff = int(input("Please make your selection: ").strip().rstrip("."))
        except ValueError:
            print("Try again! Please select 1, 2 or 3\n")
        except KeyboardInterrupt:
            sys.exit("\n\nThanks for playing!\n")
        else:
            if not (diff in [1, 2, 3]):
                print("Try again! Please select 1, 2 or 3\n")
            else:
                break

    match diff:
        case 1:
            print("Easy mode selected\n")
        case 2:
            print("Normal mode selected\n")
        case 3:
            print("Hard mode selected\n")

    while True:
        try:
            num_q = int(
                input("How many questions do you want to answer? (possible 1-46) ")
            )
        except ValueError:
            print("Try again! Please select a number between 1 and 46\n")
        except KeyboardInterrupt:
            sys.exit("\n\nThanks for playing!\n")
        else:
            if not (num_q in [_ for _ in range(1, 47)]):
                print("Try again! Please select a number between 1 and 46\n")
            else:
                break

    return (diff, num_q)


# Gives player lives based on selected difficulty, -1 will allow for infinite lives.
def get_lives(diff):
    match diff:
        case 1:
            return -1
        case 2:
            return 10
        case 3:
            return 1


def nonzero_lives(lives):
    if lives != 0:
        return True
    else:
        return False


def all_correct(score, num_q):
    score_ratio = score / num_q
    if score_ratio == 1:
        return True
    else:
        return False


# Ask questions, keep score etc.
def questions(diff, num_q):
    lives = get_lives(diff)

    score = 0
    for i in range(num_q):
        print(f"\nQuestion {i + 1}:\n")
        rand_country = random.choice(country_list)
        # Remove country from list to avoid duplicate questions
        country_list.remove(rand_country)
        print(country_obj_dict[rand_country], end="\n\n")
        if not diff == 3:
            print(
                f"Population: {country_obj_dict[rand_country].population}",
                f"Area: {country_obj_dict[rand_country].area}\n",
                sep="\n",
            )

        # Print hint for easy mode
        if diff == 1:
            hint(rand_country)

        while nonzero_lives(lives):
            if lives < 0:
                print(colored("\u2764\uFE0F  \u221E", "red"))
            else:
                print(colored(f"\u2764\uFE0F  {lives}", "red"))
            try:
                user_guess = input("Guess: ").strip().lower()
            except KeyboardInterrupt:
                sys.exit("\n\nThanks for playing!\n")
            if user_guess == rand_country.lower() or user_guess in [
                x.lower() for x in country_obj_dict[rand_country].alt_spellings
            ]:
                score += 1
                print(colored("Correct!\n", "green"))
                sleep(1)
                break
            elif user_guess == "skip":
                if diff != 3:
                    print(colored(f"Correct answer: {rand_country}\n", "yellow"))
                    sleep(1)
                    break
                print(colored("No skips on hard mode!\n", "yellow"))
                sleep(1)
                continue
            else:
                lives -= 1
                if lives != 0:
                    print(colored("Incorrect, try again!\n", "red"))
                    sleep(1)

        if lives == 0:
            print(colored(f"Correct answer: {rand_country}\n", "red"))
            print(
                colored("Out of lives! ", "red")
                + colored(f"Score: {score}/{num_q}", "blue", attrs=["bold"])
            )
            break
    if nonzero_lives(lives):
        print(
            colored("Finished! ", "green")
            + colored(f"Score: {score}/{num_q}", "blue", attrs=["bold"])
        )

    if all_correct(score, num_q) and num_q == 46 and diff == 3:
        cowsay.trex(colored("Achievement unlocked: Master!", "cyan", attrs=["bold"]))
        sleep(1)
    elif all_correct(score, num_q):
        sleep(1)
        cowsay.cow(colored("Achievement unlocked: \n100% Congratulations!", "cyan", attrs=["bold"]))


def hint(rand_country):
    num_chars = len(rand_country)
    num_hints = num_chars // 2
    hints_index = random.sample(range(0, num_chars), num_hints)
    blank = list(rand_country)
    for i in range(len(blank)):
        if blank[i] != " ":
            blank[i] = "-"
    for i in hints_index:
        blank[i] = list(rand_country)[i]
    blank = "".join(blank)
    print(colored(f"Hint: {blank}\n", "magenta"))


if __name__ == "__main__":
    main()
