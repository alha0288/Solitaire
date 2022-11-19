# Solitaire Game
This is a Solitaire game project using Python.

## Introduction
The software development project complies with the Agile Software Engineering 
methodology that our development team works with customers to analyze their business needs, 
determine computer system requirements, model system designs, build prototypes, code tests, 
and deliver final product.

## Project Requirements
This project implements the Solitaire game.
1. Refer to the reference rules: https://bicyclecards.com/how-to-play/solitaire/
2. The project has a working UI that meets the following requirements:
    * Basic rules:
		* Cards must display both the back side and front side of the card, as appropriately based on their discard/discovery status.
		* Card suits must be appropriately displayed
		* Card values must be appropriately displayed
		* The Tableau must be displayed and functional
		* Foundations are clearly outlined and functional
		* The stockpile must be displayed and functional
		* The talon pile must be clearly outlined and functional
		* Clicking/tapping a card will auto-stack it if an appropriate spot is available
	* Logic:
		* Rank of cards must be functional as outlined by the rules
		* A full deck of cards that can be shuffled must be implemented.
		* As cards are sorted into their piles, they must be subtracted from the full deck of cards.
		* Tableau cards can only be stacked in alternating colors
		* Spare tableau spots can only be filled with kings
		* Foundations can only be filled starting with an ace
		* Foundations can only be stacked by matching suits
		* Foundations can only be stacked in ascending order.
		* Tableau undiscovered cards must be stacked in the order outlined by the rules.
		* Stacks of cards can only be moved when appropriately stacked by alternating suits.
		* Stockpile must only contain cards that have not already been dealt
		* Talon pile must maintain order in which stockpile cards were discarded
		* Stockpile must maintain order set by talon pile when re-stocking.
		* User must be able to start a new game, thus receiving a freshly shuffled deck of cards

## Distribution
The project is deployed as a package that is built and uploaded to the PyPI(Python Package Index).
To register an account on [PyPI](https://pypi.org/), complete the steps on that page. 
It will need to verify user's email address before upload or download any packages.

## Configuration
Open pyproject.toml to see the project metadata specification for details and other fields that can be defined in the project table. 
Other common fields are keywords to improve discoverability and the dependencies that are required to install the package.

## License
See License.txt file

