import socket
import sqlite3
import json
import sys
import re
server_address = ('localhost', 5001)
menu = ["(L)og_in  (S)ign_up  (Q)uery  Schedule_(P)rint  (M)odify  Shut_(D)own"]
valid = frozenset("lsqpmd")
date = "January February March April May June July August September October November December"
def main(data):
    oper = data[0]
    if oper in valid:
        if oper == "s":
            id = data[1]
            pwd = data[2]
            user_sign_up(id, pwd)
        elif oper == "l":
            id = data[1]
            pwd = data[2]
            user_log_in(id, pwd)
        elif oper == "q":
            tournament_query(data[1:])
        elif oper == "p":
            load_tournamentdb_data()
        elif oper == "m":
            tournament_modify(data[1:])
        elif oper == "d":
            shutdown()
        else:
            pass
    else:
        connection.send(json.dumps(["false", "Invalid operation."]).encode())
def load_userdb_data():
    conn_db = sqlite3.connect('System_users.db')
    cur = conn_db.cursor()
    sql_text = "CREATE TABLE IF NOT EXISTS user_info (id varchar(25) UNIQUE NOT NULL, password varchar(255) NOT NULL , is_admin boolean NOT NULL);"
    sql_text2 = "select * from user_info "
    cur.execute(sql_text)
    conn_db.commit()
    insert_admin = "INSERT INTO user_info VALUES (?,?,?)"
    cur.execute(sql_text2)
    res = cur.fetchall()
    if len(res) > 0:
        pass
    else:
        cur.execute(insert_admin, ("admin", "admin123", 1))
        conn_db.commit()
    conn_db.close()
def load_tournamentdb_data():
    conn_db = sqlite3.connect('2022_FIFA_WorldCup.db')
    cur = conn_db.cursor()
    cur.execute("select * from Tournaments")
    res = cur.fetchall()
    schedule_display(res)
    conn_db.commit()
    conn_db.close()
def user_log_in(id, pwd):
    conn_db = sqlite3.connect('System_users.db')
    cur = conn_db.cursor()
    sql_text = "select password,is_admin from user_info where id = (?)"
    cur.execute(sql_text, (id,))
    res = cur.fetchall()
    if len(res) == 0:
        connection.send(json.dumps(["null", "This user does not exist, please register."]).encode())
    else:
        if pwd == res[0][0]:
            connection.send(json.dumps(["true", res[0][1]]).encode())
        else:
            connection.send(json.dumps(["false"]).encode())
    conn_db.commit()
    conn_db.close()
def user_sign_up(id, pwd):
    conn_db = sqlite3.connect('System_users.db')
    cur = conn_db.cursor()
    sql_text = "INSERT INTO user_info VALUES (?,?,?);"
    cur.execute(sql_text, (id, pwd, 0))
    conn_db.commit()
    connection.send(json.dumps(["true"]).encode())
    conn_db.close()
def tournament_query(info):
    if info[0] == 1:
        load_tournamentdb_data()
    else:
        conn_db = sqlite3.connect('2022_FIFA_WorldCup.db')
        cur = conn_db.cursor()
        pat1 = "[0-9]+:[0-9]+"
        pat2 = "\D"
        temp = info[1]
        relevant_info = temp.strip()
        if re.search(pat1, relevant_info): # 按比分进行查询
            sql_text = "select * from Tournaments where score1 = ? and score2 = ?"
            cur.execute(sql_text, (int(relevant_info[0]), int(relevant_info[-1])))
            res = cur.fetchall()
            schedule_display(res)
            cur.close()
        elif re.search(pat2, relevant_info):
            if re.search(relevant_info.title(), date): # 按月份进行查询
                sql_text = "select * from Tournaments where month like ?"
                cur.execute(sql_text, (relevant_info + "%",))
                res = cur.fetchall()
                schedule_display(res)
                cur.close()
            else: # 按队名（国家名）进行查询
                sql_text = "select * from Tournaments where team1 like ? or team2 like ? "
                cur.execute(sql_text, (relevant_info + "%", relevant_info + "%"))
                res = cur.fetchall()
                schedule_display(res)
                cur.close()
        elif relevant_info.isdigit(): # 按日期进行查询
            sql_text = "select * from Tournaments where day = ?"
            cur.execute(sql_text, (int(relevant_info),))
            res = cur.fetchall()
            schedule_display(res)
            cur.close()
        else:
            connection.send(json.dumps(["false", "Error,please restart."]).encode())
def tournament_modify(info):
    conn_db = sqlite3.connect('2022_FIFA_WorldCup.db')
    cur = conn_db.cursor()
    if info[0] == "m":
        try:
            m_data = info[1]
            sql_text = "delete from Tournaments where id = ? "
            cur.execute(sql_text, (int(m_data[0]),))
            sql_text2 = "insert into Tournaments values (?,?,?,?,?,?,?,?,?,?)"
            cur.execute(sql_text2, tuple(m_data))
            conn_db.commit()
            conn_db.close()
            connection.send(json.dumps(["true"]).encode())
            conn_db.close()
        except Exception:
            connection.send(json.dumps(["false"]).encode())
        finally:
            conn_db.close()
    elif info[0] == "a":
        try:
            a_data = info[1]
            sql_text = "select max(id) from Tournaments "
            cur.execute(sql_text)
            max_id = cur.fetchall()
            sql_text2 = "insert into Tournaments values (?,?,?,?,?,?,?,?,?,?)"
            lst = [max_id[0][0] + 1, ]
            for i in a_data:
                lst.append(i)
            cur.execute(sql_text2, tuple(lst))
            conn_db.commit()
            conn_db.close()
            connection.send(json.dumps(["true", "1"]).encode())
        except Exception:
            connection.send(json.dumps(["false"]).encode())
        finally:
            conn_db.close()
    elif info[0] == "d":
        try:
            d_data = info[1]
            sql_text = "delete from Tournaments where id = ? "
            cur.execute(sql_text, (int(d_data),))
            conn_db.commit()
            conn_db.close()
            data1 = json.dumps(["true"])
            connection.send(data1.encode())
        except Exception:
            connection.send(json.dumps(["false"]).encode())
        finally:
            conn_db.close()
    else:
        pass
def schedule_display(info):
    schedule = []
    if bool(info):
        for i in info:
            schedule_set = (
                str(i[0]), i[1] + " " + str(i[2]), i[3], i[4], str(i[5]) + ":" + str(i[6]), i[7], i[8], i[9])
            schedule.append(schedule_set)
        connection.send(json.dumps(schedule).encode())
    else:
        connection.send(json.dumps(["false"]).encode())
def shutdown():
    connection.close()
    server_socket.close()
    sys.exit()
if __name__ == "__main__":
    try:
        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the address and port
        server_socket.bind(server_address)
        server_socket.listen(5)
        connection, client_address = server_socket.accept()
        # Display the connection address
        print("Connection from: " + str(client_address))
        # Send a response back to the client
        response = "ACK: {}".format("System is ready!")
        connection.send(response.encode())
        # Load the data in the user database
        load_userdb_data()
        # Continuous communication with the client
        while True:
            recv = connection.recv(1024)
            data = json.loads(recv)
            if not data:
                continue
            else:
                main(data)
                print(data)
    except ConnectionResetError:
        print("The client side has closed.")
        sys.exit()
    except sqlite3.IntegrityError as err:
        connection.send(json.dumps(["false", str(err)]).encode())
        pass
    except EOFError as err:
        connection.send(json.dumps(["false", str(err)]).encode())
        pass
    except json.decoder.JSONDecodeError:
        print("The client side has closed.")
        sys.exit()
