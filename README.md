# borgprune

A script to delete outdated [borg](https://www.borgbackup.org/) archives. I never really understood borg's "prune" configuration so in the end I just wrote this code.

**PLEASE NOTE:** This command will delete all "outdated" archives without further confirmation!

    $ borgprune ARCHIVE

### What is "outdated"?
The borgprune cli script will *keep* the following archives:
- one per month for the last year
- one per week for the last 5 months
- one per day for the last two months
- all backups for the last seven days

In addition the latest backup is always preserved. All other archives will be deleted. 

### Requirements and Installation
The code is written in Python 3 and relies on [python-dateutil](https://pypi.python.org/pypi/python-dateutil).

    pip install -r requirements.txt
    python setup.py install


### Limitations
Currently the code is arguably more "libborgprune" as CLI users can not specify custom rules for deleting archives. I'll add some kind of configuration file support (and more CLI flags) but this code satifies my immediate needs so I just published it.

