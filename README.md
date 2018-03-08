# Madras

[![Build Status](https://travis-ci.org/TotalityHacks/madras.svg?branch=master)](https://travis-ci.org/TotalityHacks/madras)

Madras is the backend for a cloud-based hackathon management system that aims to bring together the many different hackathon organizing systems into one centralized service to minimize the need to migrate data between hacker applications, registration, check-in, announcements, reimbursement, judging, and prizes.  Created with the goal of making organizing hackathons easier for everyone.

## Setup

```bash
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```
