# jooble-test-task
Link shortening service written with Flask

## Algorithm:
In order to keep links as short as possible, the original links are numbered using 32-base values, which are formed from '0123456789' + english lowercase alphabet.
In this case, ID is the short link. 
<br>
The expired dates once a day will checked and deleted by background scheduled task. 
<br>
Database will be created at script folder.
<p> 
The ID field in the database looks like this: 

![db_example](https://user-images.githubusercontent.com/46729793/107218980-142aad80-6a19-11eb-9dea-f4bb236da489.png)

Database scheme looks like:
<p>
  
![database](https://user-images.githubusercontent.com/46729793/107218975-11c85380-6a19-11eb-8161-f79b415bc634.png)


To get the original link, just select row by ID.

![algorithm](https://user-images.githubusercontent.com/46729793/107218965-0e34cc80-6a19-11eb-84d1-572741b84df4.png)

## Installation:

  1. Create virtual enviroment <p> `python3 -m venv directory`
  2. Activate it <p> `source directory/bin/active`
  3. Install requirements <p> `pip3 install -r requirements.txt`
  4. Run server by <p> `python3 main.py`
  5. Enjoy!
    
## Usage:
If not deployed, then you can test in your local network:
<p>
  
**To short:** `localhost:5000/shorten?url=[url_to_shorten]&days_to_expire=[number_of_days_to_expire]` (90 by default)
<p>
  
**To original:** `localhost:5000/[short_link]`

## TODO:
Replace deleted records by reused free IDs 
