import subprocess
from subprocess import Popen, PIPE
import sys
import psycopg2
from psycopg2 import OperationalError
from psycopg2 import Error
import time
from datetime import date
import os
import logging
import variable

def get_day():
        today = date.today()
        today = today.strftime("%Y/%m/%d")
        return today

def get_data():
        data = dict()
        data['email'] = str(sys.argv[1])
        data['username'] = str(sys.argv[2])
        data['uid'] = str(sys.argv[3])
        data['DB_USER'] = str(sys.argv[4])
        data['DB_PWD'] = str(sys.argv[5])
        data['env'] = str(sys.argv[6])
        data['ticket'] = str(sys.argv[7])
        data['buildNumber'] = str(sys.argv[8])
        data['jobname'] = str(sys.argv[9])
        data['jenkinsUser'] = str(sys.argv[10])
        data['country'] = str(sys.argv[11])
        return data

def create_user():
        all_data = get_data()
        group = variable.group
        groupjenkins = variable.groupjenkins
        email = all_data['email']
        username = all_data['username']
        userid = all_data['uid']
        try:
                luseradd = subprocess.Popen([ "luseradd", "-d", "/home/%s" %username, "%s"%userid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = luseradd.communicate()
                logging.debug("luseradd -d /home/$username $username => %s ", out)
                if not err:
                    print("erreur with => useradd -d /home/$username $username  : ", err)
                    logging.error("erreur with => useradd -d /home/$username $username  : %s", err)
                else:
                    print("luseradd -d /home/$username $username is ok")
                    logging.debug("luseradd -d /home/$username $username => %s ", out)
        except OSError as e:
                logging.error("erreur with => luseradd -d /home/$username $username : %s", e)
                print("erreur with => luseradd -d /home/$username $username : ", e)
        try:
                usermod = subprocess.Popen(["usermod", "-aG", "%s"%group, "%s"%username], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = usermod.communicate()
                if not err:
                    print("erreur with => usermod -aG $group $username : ", err)
                    logging.error("erreur with => usermod -aG $group $username : %s", err)
                else:
                    print("usermod -aG $group $username => is ok")
                    logging.debug("usermod -aG $group $username => %s ",out)
        except OSError as e:
                logging.error("erreur with => usermod -aG $group $username : %s", e)
                print("erreur with => usermod -aG $group $username : ", e)
        try:
                usermod2 = subprocess.Popen(["usermod", "-aG", "%s"%username, "%s"%groupjenkins], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = usermod2.communicate()
                if not err:
                    print("erreur with => usermod -aG $username $groiupjenkins : ", err)
                    logging.error("erreur with => usermod -aG $username $groupjenkins : %s", err)
                else:
                    print("usermod -aG $username jenkins => is ok")
                    logging.debug("usermod -aG $username jenkins => %s ",out)
                
        except OSError as e:
                logging.error("erreur with => usermod -aG $username $groupjenkins : %s", e)
                print("erreur with => usermod -aG $username $groupjenkins : ", e)
        try:
                ln = subprocess.Popen(["ln", "-s", "/home/share", "/home/%s/share"%(username)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = ln.communicate()
                if not err:
                    print("erreur with => ln -s /home/share /home/$username/share : ", err)
                    logging.error("erreur with => ln -s /home/share /home/$username/share : %s", err)
                else:
                    print("ln -s /home/share /home/$username/share => is ok")
                    logging.info("ln -s /home/share /home/$username/share => %s ", out)
        except OSError as e:
                logging.error("erreur with => ln -s /home/share /home/$username/share : %s", e)
                print("erreur with => ln -s /home/share /home/$username/share : ", e)
        try:        
                password="date +%s | sha256sum | base64 | head -c 10 ; echo"
                thepassword = (subprocess.check_output(password,shell=True).decode("utf-8"))
                logging.debug("$(date +%s | sha256sum | base64 | head -c 10 ; echo)")
        except OSError as e:
                logging.error("erreur with => password=$(date +%s | sha256sum | base64 | head -c 10 ; echo)", e)
                print("erreur with => password=$(date +%s | sha256sum | base64 | head -c 10 ; echo)", e)
        try:
                print("the password is from try : ", thepassword)
                print("le nom d'utilisateur est : ", username)
                theecho = subprocess.Popen(["echo", "%s"%(thepassword), "|", "passwd", "--stdin", "%s"%(username)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = theecho.communicate()
                if not err:
                    print("erreur with => echo $password | passwd --stdin $username : ", err)
                    logging.error("erreur with => echo $password | passwd --stdin $username : %s", err)
                else:
                    print("echo $password | passwd --stdin $username => is ok")
                    logging.debug("echo $password | passwd --stdin $username : %s ", out)
                
        except OSError as e:
                logging.error("erreur with => echo $password | passwd --stdin $username : %s", e)
                print("erreur with => echo $password | passwd --stdin $username : ", e)
        try:
                theecho2 = subprocess.Popen(["echo", "%s"%(userid), "|", "tr", "[:lower:]", "[:upper:]", ">", "/home/%s/.uid"%(username)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = theecho2.communicate()
                if not err:
                    print("erreur with => echo $3 | tr [:lower:] [:upper:] > /home/$username/.uid : ", err)
                    logging.error("erreur with => echo $3 | tr [:lower:] [:upper:] > /home/$username/.uid : %s", err)
                else:
                    print("echo $3 | tr [:lower:] [:upper:] > /home/$username/.uid => is ok ")
                    logging.debug("echo $3 | tr [:lower:] [:upper:] > /home/$username/.uid : %s", out)
                
        except OSError as e:
                logging.error("erreur with => echo $3 | tr [:lower:] [:upper:] > /home/$username/.uid %s", e)
                print("erreur with => echo $3 | tr [:lower:] [:upper:] > /home/$username/.uid : ", e)
        try:
                opt = subprocess.Popen(["/opt/admin/configure-SparkMagic-for-user.sh", "%s"%(username), "%s"%(userid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = opt.communicate()
                if not err:
                    print("erreur with => /opt/admin/configure-SparkMagic-for-user.sh $username $userid: ", err)
                    logging.error("erreur with => /opt/admin/configure-SparkMagic-for-user.sh $username $userid: %s", err)
                else:
                    print("/opt/admin/configure-SparkMagic-for-user.sh $username $userid => is ok ")
                    logging.debug("/opt/admin/configure-SparkMagic-for-user.sh $username $userid : %s", out)
                
        except OSError as e:
                logging.error("erreur with => /opt/admin/configure-SparkMagic-for-user.sh $username $userid %s",e)
                print("erreur with => /opt/admin/configure-SparkMagic-for-user.sh $username $userid: ", e)
        try:
                sendmail = subprocess.Popen(["/opt/admin/sendMailCreateUser.py", "%s"%(username), "%s"%(thepassword), "%s"%(email)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = sendmail.communicate()
                if not err:
                    print("erreur with => /opt/admin/sendMailCreateUser.py $username $password $email : ", err)
                    logging.error("erreur with => /opt/admin/sendMailCreateUser.py $username $password $email : %s", err)
                else:
                    print("/opt/admin/sendMailCreateUser.py $username $password $email : ", out)
                    logging.debug("/opt/admin/sendMailCreateUser.py $username $password $email : %s", out)
                
        except OSError as e:
                logging.error("erreur with => /opt/admin/sendMailCreateUser.py $username $password $email %s",e)
                print("erreur with => /opt/admin/sendMailCreateUser.py $username $password $email : ",e)


def connect_to_data_bases():
        all_data = get_data()
        logging.info("get all values from command line")
        day = get_day()
        logging.info("get value from get_day function")
        logging.info("get status value from variable file's")
        newstatus = variable.newstatus
        logging.info("get newstatus value from variable file's")
        try:
                connection = psycopg2.connect(host=variable.host,database=variable.database,user=all_data['DB_USER'],password=all_data['DB_PWD'])
                logging.debug("start connection to data base %s", connection)
                cursor = connection.cursor()
                logging.debug("start connection : %s", cursor)
                postgres_insert_query = """SELECT userexist (%s);"""
                logging.info("call function userexist in data base to tcheck if user exist or not")
                record_to_insert = (all_data['email'],)
                print(record_to_insert)
                ex = cursor.execute(postgres_insert_query, record_to_insert)
                logging.debug("start check the existence of user : %s", ex)
                result_of_cursor = cursor.fetchall()
                num = len(result_of_cursor)
                if not num:
                        print("add num if not num")
                        date_of_desactivation = "---------"
                        date_of_delete = "---------"
                        status = "Creation"
                        cursor.execute("CALL newusers(%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],status,day,date_of_desactivation,date_of_delete,all_data['country'],all_data['env']))
                        logging.debug("According to the insertions it is a new user")
                        cursor.execute("CALL newhistory(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],day,all_data['ticket'],all_data['buildNumber'],all_data['jobname'],all_data['jenkinsUser'],status,all_data['env']))
                        logging.debug("Add to history databases")
                        logging.debug("End insertion in database")   
                elif num > 0 and num<2:
                        for ro in result_of_cursor:
                                result = ro[0]
                                if result != all_data['env']:
                                        date_of_desactivation = "---------"
                                        date_of_delete = "---------"
                                        status = "Creation"
                                        cursor.execute("CALL newusers(%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],status,day,date_of_desactivation,date_of_delete,all_data['country'],all_data['env']))
                                        logging.debug("According to the insertions it is a new user")
                                        cursor.execute("CALL newhistory(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],day,all_data['ticket'],all_data['buildNumber'],all_data['jobname'],all_data['jenkinsUser'],status,all_data['env']))
                                        logging.debug("Add to history databases")
                                        logging.debug("End insertion in database")
                                else: 
                                        action = "Updated"
                                        cursor.execute("CALL newhistory(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],day,all_data['ticket'],all_data['buildNumber'],all_data['jobname'],all_data['jenkinsUser'],action,all_data['env']))
                                        logging.debug("User was updated")
                                        logging.debug("End insertion in database")
                elif num >=2: 
                        val1 = result_of_cursor[0]
                        val2 = result_of_cursor[1]
                        if val1 != all_data['env'] and val2 != all_data['env']:
                                date_of_desactivation = "---------"
                                date_of_delete = "---------"
                                status = "Updated"
                                cursor.execute("CALL newhistory(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],day,all_data['ticket'],all_data['buildNumber'],all_data['jobname'],all_data['jenkinsUser'],status,all_data['env']))
                                logging.debug("User was updated")
                                logging.debug("End insertion in database")
                        else: 
                                action = "Updated"
                                cursor.execute("CALL newhistory(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],day,all_data['ticket'],all_data['buildNumber'],all_data['jobname'],all_data['jenkinsUser'],action,all_data['env']))
                                logging.debug("User was updated")
                                logging.debug("End insertion in database")

                else:
                        action = "Updated"
                        cursor.execute("CALL newhistory(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (all_data['uid'],all_data['username'],all_data['email'],day,all_data['ticket'],all_data['buildNumber'],all_data['jobname'],all_data['jenkinsUser'],action,all_data['env']))
                        logging.debug("User was updated")
                        logging.debug("End insertion in database")
                connection.commit()
                count = cursor.rowcount
        except (Exception, psycopg2.Error) as error:
                logging.error("Failed to insert record into newUsers table => %s", error)
                raise
        finally:
                if connection:
                        cursor.close()
                        connection.close()
                        logging.debug("PostgreSQL connection is closed")

if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')
        logging.info("################# SATR OF SCRPT #######################")
        create_user()
        connect_to_data_bases()
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.ERROR)
        logging.info("################# END OF SCRPT #######################")
                    
