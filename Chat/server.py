#!/usr/bin/env python3

import socket
import threading
import json
import mysql.connector
from mysql.connector import Error
#import pandas as pd



hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

HOST = IPAddr
PORT = 5000
LISTENER_LIMIT = 10
active_clients = []

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

#connection = create_server_connection("localhost", "root", pw)

#use global to create global variables

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
def listen_for_messages(client, username):

    while 1:



        message = (client.recv(4096).decode('UTF-8'))
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"Kullanici olan {username}'den gelen mesaj bos.")


def send_message_to_client(client, message):

    client.sendall(message.encode())

def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

def client_handler(client):

    while 1:


        dosya1 = open(r"/home/kuzu/Desktop/Chat/Bilgiler/user.txt", "r")

        jsonPack = json.loads(client.recv(4096).decode())

        print(jsonPack)

        print(type(jsonPack))

        usernameclient = jsonPack["usernameclient"]

        print(usernameclient)
        print(type(usernameclient))

        passwordclient = jsonPack["passwordclient"]

        print(passwordclient)
        print(type(passwordclient))



        for line in dosya1:
            line = line.strip()
            if line:
                j = json.loads(line)
                print(j)
                print("user: " + j["username"])
                print("password: " + j["password"])
                if usernameclient == j["username"] and passwordclient == j["password"] or usernameclient == j["username1"] and passwordclient == j["password1"]:
                   active_clients.append((usernameclient, client))
                   prompt_message = "SERVER~" + f"{usernameclient} adli kullanici Pigeon'a katildi."
                   send_messages_to_all(prompt_message)
                   continue
                else:
                    while 1:
                      #active_clients.append((j["username"], client))
                      #prompt_message = "SERVER~" + f"Bilgiler yanlis, Server'a giris yapilamadi."
                      #send_messages_to_all("Giriş Yapılamadı.")
                      print("Giriş Yapılamadı.")
                      client_handler(client)
                      break

        break

    threading.Thread(target=listen_for_messages, args=(client, usernameclient,)).start()
def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Pigeon'in bagli olduğu ana makine: {HOST} {PORT}")
    except:
        print(f"Host'a {HOST} ve port'a {PORT} baglanilamadi.")

    server.listen(LISTENER_LIMIT)

    while 1:

        client, address = server.accept()
        print(f"Pigeon'a baglanan kullanicilar: {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()
