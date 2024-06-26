Description
My project is a command-line interface quiz game in which the player must guess the European country based on an ASCII art image of the country outline. The features of the game include: Title screen with menu, three difficulty levels, lives, score, hints, skip question option, area and population country data, acceptance of alternate/abbreviated spellings and achievements. Please see the video link above for a full demo of the game.

image_to_ascii.py
My first task for this project was to write a file to convert a folder of .png images of country outlines to a corresponding folder of .txt ASCII art files. I used the os module, specifically the os.listdir() method to create a list of all the .png file names in the images folder. I then used the Image module from the Python Imaging Library (PIL) to open and manipulate each of the .png images. The manipulations required were as follows:

Image rescaling to an appropriate size for the terminal and resizing as ASCII characters distort the image vertically.
Convert the image to greyscale and read each pixel value (0-255).
Convert each pixel to an ASCII character based on the greyscale pixel value.
This str datatype was then saved as a .txt file in the ascii.txt files folder.

project.py
Now to discuss the main code of my project. I decided to represent each country in the quiz as a class object. This allowed me to create attributes for each country such as area, population, alternative spellings, ASCII image etc. that were easily accessible and specific to that country.

I created a csv file with the data for all the countries that I used to initialise the country object attributes (via the csv.DictReader() method). I also created a global dictionary with the country name as the key and the country object as the value pair to make it easy to access each country object.

I then used the pyfiglet and tabulate modules to construct the in terminal game menu. The user is prompted to select a difficulty level and the number of questions they wish to answer.

The questions are then posed randomly to the played with the ASCII art outline of the country displayed in the terminal. The player is prompted to make a guess at which country they believe it to be. The player lives and question number are also displayed. On easy and normal mode, the played is also provided with the area and population statistics of that country to aid in their guess. On easy mode the player is provided a hint of half (or half - 1 via //2 floor division) of the letters of the country by random. On hard mode the player receives no such assistance.

Upon making a guess if the player is correct they notified as such, receive +1 to their score and proceed to the next question. If the player is incorrect they are reprompted to make another guess and lose a life. At any time if a player feels stuck, they can type skip into the terminal to skip the current question. A message displaying what the correct answer was is shown before proceeding to the next question. The player does not lose a life for this action, however they will forfeit the point for that question. Skips are disbled in hard mode.

The player receives infinite lives in easy mode, 10 lives in normal mode and only 1 life in hard mode.

If the player runs out of lives, they are shown a game over message along with what the correct answer was for their current question and their final score. If a player reaches the end of the quiz with lives remaining, they are shown a completion message and their final score.

There are two achievements, the first for receiving 100% in any difficulty and the second for answering all 46/46 questions correctly on hard mode (not an easy feat!). Upon completing either of these achievements the played is shown a special achievement message utilising the cowsay package.

test_project.py
I also created a file to test some of simpler functions of my project using the pytest module. I will be the first to admit the this is by no means a comprehensive test of my project and is the weakest component of my submission. I found it very difficult to attempt to test my more complex functions with pytest as most of them require user input and have elements of randomness.
