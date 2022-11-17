import mariadb
import sys
import random
import time

# Below two functions were leveraged from stackoverflow
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y/%m/%d', prop)
    
# Connect to the MariaDB instance
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="ec2-3-145-100-54.us-east-2.compute.amazonaws.com",
        port=4306,
        database="medical_analysis"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}") 
    sys.exit(1)

cur = conn.cursor()

# Update the DoB column for every record, we will set a date between 01/01/1947 and 01/01/2007
cur.execute(
    "SELECT id FROM patient_info"
)
table = cur.fetchall()
for (id,) in table:
    cur.execute(
        "UPDATE patient_info SET dob = ? WHERE id = ?",(random_date("1947/01/01", "2007/01/01", random.random()),id)
    )

# Fetch records with gender not set to Male/Female
cur.execute(
    "SELECT id FROM patient_info WHERE gender<>? AND gender<>?",("Male","Female")
)
table = cur.fetchall()
for (id,) in table:
    # All even IDs mark them as Male, the rest Female
    if id % 2 == 0:
        cur.execute(
            "UPDATE patient_info SET gender = ? WHERE id = ?",("Male",id)
        )
    else:
        cur.execute(
            "UPDATE patient_info SET gender = ? WHERE id = ?",("Female",id)
        )

# Commit and close
conn.commit()
conn.close()

