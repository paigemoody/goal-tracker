# goal-tracker

A goal tracking app that allows users to view, save, and edit their personal goals.

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