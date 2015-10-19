## Who To Follow?
This app was designed to help people find Twitter accounts relevant to their own interests. When seach keywords
are entered into the input bar Twitter is queried and the top 10 accounts (based upon followers, verification and number of tweets) are rendered with their picture, name and username as well as a link to follow that account.

#### Dependencies
This app depends on Python, Flask, gunicorn, Jinja, oauth, and TwitterAPI.

To install and develop:

```
# Install dependencies to a new virtual environment
virtualenv venv
source venv/bin/activate # (or . venv/bin/activate, depending on your shell)

# Set up twitter credentials
export ACCESS_TOKEN=...
export ACCESS_SECRET=...
export CONSUMER_TOKEN=...
export CONSUMER_SECRET=...

# Install deps and run
pip install -r requirements.txt
python who_to_follow.py
```

#### Contribution Policy
All contributions are greatly encouraged, submit a PR to be considered!
