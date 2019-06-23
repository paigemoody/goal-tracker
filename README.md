# goal-tracker

A goal tracking app that allows users to view, save, and edit their personal goals.

![goal-tracker](https://user-images.githubusercontent.com/25571355/59982178-0796de80-95c3-11e9-8831-00431b30cab1.gif)


## Tech Stack
Python, PostgreSQL, SQLAlchemy, Flask, JavaScript, JQuery, Jinja, CSS

## Getting Started

These instructions will get you a copy of the project up and running on your local machine with a sample database.

### Prerequisites

```
python3.7
postgresql
```

### Install dependencies 

`$ pip3 install -r requirements.txt`


### Run locally


**1.** Create postgres database.
	`$ createdb goal_tracker`
	
**2.** (optional) Seed database with sample data.

	$ python3 seed.py

**3.** Create `sercrets.sh` file in root directory. 

**4.** Add `export flask_session_key="<some secret key>"` to `secrets.sh` *Note: this is required to run the Flask server.*

**5.** Connect `secrets.sh`. 

	$ source secrets.sh

**6.** Run server.

	$ python3 server.py