from unittest import result
import mariadb
import dbcreds

def conect_db():
    conn = None
    cursor = None
    
    try:
        conn = mariadb.connect(
                        user = dbcreds.user,
                        password = dbcreds.password,
                        host = dbcreds.host,
                        port = dbcreds.port,
                        database = dbcreds.database
    )
        cursor = conn.cursor()
        return (conn,cursor)

    except mariadb.OperationalError as e:
        print("got an operational error")
        if ("access denied" in e.msg):
            print("failed to log in")
        disconnect_db(conn, cursor)



def disconnect_db(conn, cursor):
    if(cursor != None):
        cursor.close()
    if(conn != None):
        conn.rollback()
        conn.close()



def run_query(statement, args=None):
    
    try:
        (conn, cursor) = conect_db()
        if statement.startswith("SELECT"):
            cursor.execute(statement,args)
            result = cursor.fetchall()
            print("todtal of {} users" .format(cursor.rowcount))
            return result
            
        else:
            cursor.execute(statement, args)
            if cursor.rowcount == 1:
                conn.commit()
                print("insert sucessful")
            else:
                print("failed to instert")
    
    except mariadb.OperationalError as e:
        print("got an operational error")
        if ("access denied" in e.msg):
            print("failed to log in")

    except mariadb.IntegrityError as e:
        if("CONSTRAINT `user_CHECK_username`" in e.msg):
            print("error, all usernames must start with the letter J")
        if ("CONSTRAINT `user_CHECK_age`" in e.msg):
            print("error user is outside of acceptable range")
    
            print("intergity error")
            print(e.msg)

    except mariadb.ProgrammingError as e:
        if("SQL syntax" in e.msg):
            print("Apparently you do not know how to program")
        else:
            print("got a different programing error")
            print(e.msg)

    except RuntimeError as e:
        print("caught a run time error")
        e.with_traceback

    except Exception as e :
        print(e.with_traceback)
    
