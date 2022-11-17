# Simple data imputation on a table in MariaDB

Basic outlay:
- Connect to the instance
- Update the dob (Date of Birth) column of every record - we set a random date such that the age is between 15 and 75 years.
- Update the gender to Male or Female, if its anything else. Simple strategy used based on whether the primary key (id) is even or odd.
- Commit the changes

