# DishFinder

Telegram bot that helps you to find idea for dish - just enter ingredients and choose your favorite dish.
## Features

- Output of detailed information
	- image
	- ingredients
	- step-by-step instruction
- Saving dishes in 'history'
- Display up to 5 options at once
- Convinient user interface with pagination 
## Dependencies

- sqlalchemy 
- aiogram
- pygame
- requests
## Codestyle linters and tests 

The project has been checked and tested with the following tools:
- flake8
- pydocstyle
- pytest

## TODO

- [ ] Translation in russian and english
- [ ] Asynchronous API Calls
- [ ] Change DB on Postgres
- [ ] Ability to view the full recipe through history

## How to start

### For developers
- set spoonacular, telegram bot api keys to env
- run entrance point - main.py
### For users
- https://t.me/DishFinderBot - just write
## Design

### State diagram 
![image](https://user-images.githubusercontent.com/114457052/234188089-2513addb-dfef-42d9-9e76-05d82365b096.png)
### Sequence diagram 
![image](https://user-images.githubusercontent.com/114457052/234188130-1be8a3c9-6520-47f7-941c-8012c794d22e.png)

### Secret
Tome AI creates an image of happy customers who have discovered the right dish.
![image](https://user-images.githubusercontent.com/114457052/234189745-d808c5be-43c3-4af1-a2ab-e9fb015bdd34.png)



