import datetime

__author__ = 'ife'

from jenkinsapi import jenkins
import sqlite3 as lite


jenkins_url = 'http://localhost:8080'
jenkins_username = 'username'
jenkins_password = 'password'

# Ideally you'd split the functions handling db work to a different file/class, btu then this is a quick script hack
def setup_db():
    db_connection = lite.connect(r'jenkins_db.db')
    db_connection.execute("CREATE TABLE IF NOT EXISTS jenkins_tasks (id INTEGER PRIMARY KEY, job_name TEXT, job_status TEXT, description TEXT, job_check_time TEXT)")
    return db_connection

def insert_into_db(db_connetion, name, status, timestamp):

    if db_connetion and name and status and timestamp:
        query = "insert into jenkins_tasks (job_name, job_status, job_check_time) values ('"+str(name)+"','"+str(status)+"','"+str(timestamp)+"')"
        try:
            db_connetion.execute(query)
        except Exception as e:
            # Ideally, this would be logged, and would not be a wildcard catchall
            print e.message

def connect_to_jenkins():
    server = None
    try:
        server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    except Exception as e:
        # Ideally, this would be logged, and would not be a wildcard catchall.
        print e.message
    return server

def process_jenkins_tasks():
    jenkins_server = connect_to_jenkins()
    if jenkins_server:

        try:
            for job_name, job_info in jenkins_server.get_jobs():
                job_status = 'Is Running: %s, Is Queued: %s, Is Enabled: %s',str(job_info.is_running()),str(job_info.is_queued()),str(job_info.is_enabled())
                job_checked =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_into_db(name=job_name, status=job_status, timestamp=job_checked)
        except Exception as e:
            print e.message



if __name__ == '__main__':
    db_connection = setup_db()
    # Ideally this would be a daemonised script, but its a quick hack, I not so worried about restarts, state traking... etc
    # so just create a loop with a time interrupt to pull jenkins server at intervals
    while(True):
        process_jenkins_tasks()
        # sleep script for 5 minutes
        datetime.time.sleep(300)
