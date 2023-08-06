# Parature Gmail Feed
## Description
The Parature Gmail Feed:
* Retrieves emails cc'd to a Gmail account originating from Parature
* Extracts Parature specific content from each email
* Creates a record from the extracted content
* Loads the record to a MongoDB database


## Installation
Install with pip
```
pip install paraturegmailfeed
```

**Project requires MongoDB**

[See MongoDB documentation for installation instructions](https://docs.mongodb.org/manual/installation/)

## Getting Started
### Setting up your config file

Create a new .py file. For example `my_config.py`
```
# Gmail API Variables
CLIENT_SECRET_FILE = 'Exported from your Google application account'
SCOPES = 'Scopes for your Google application'
APPLICATION_NAME = 'Name of your application'

USER_ID = 'YOUR EMAIL ACCOUNT USER ID'

TARGET_LABEL_QUERY = 'The label name '

# MongoDB Variables
MONGO_URI = 'YOUR DB URI'
DB_NAME = 'YOUR DB NAME'
```

### Example of usage:
```
from paraturegmailfeed import ParatureGmailFeed


def main():
    feed = ParatureGmailFeed('my_config.py')
    feed.run()

main()
```
### Running for the first time
Be sure to have `mongod` running.

You will be prompted to authorize the application to access your Gmail account.
After accepting, the application will run automatically.

[See official documentation for assistance](https://developers.google.com/gmail/api/quickstart/python)

## Design Decisions
### Why MongoDB?
* Flexible schema. As requirement grow/change the data schema can to!
* Native functionality. Simple upserts (unlike most SQL databses).

### How are duplicate records prevented?
* Gmail API message query is restricted to all messages that do NOT have the "Processed" label.
* The pymongo `update_one` method is used with the `upsert` option. This means that if a record already exists based on the composite key (ticket number and timestamp) the action will simply update the record (essentially do nothing).
