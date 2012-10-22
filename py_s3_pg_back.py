#!/usr/bin/python2.6
#Coded by Anto !!
# This script Uploades Database dump to s3 
import os
import datetime
import time
import string
import smtplib
def s3upload(filename):
                try:
                        from boto.s3.connection import S3Connection
                        conn = S3Connection('access key', 'acces token')
                        from boto.s3.key import Key
                        b=conn.get_bucket('bucket name')
                        k=b.new_key(filename)
                        k.set_contents_from_filename(filename)
                        #clear the pg dump in local
                        syscommand='rm '+filename
                        os.system(syscommand)
                        print "Uploaded to s3 and deleted from local !"
                except IOError as e:
                        panic(e)
                        print e
# function to mail me when smthing goes wrong !
def panic(stacktrace):
                        print "error!"
                        SUBJECT = " Backup Failed !!"
                        TO = "anto@urdomain.com"
                        FROM = "postgres@urdomain.com"
                        text = "Backup Failed"+stacktrace
                        BODY = string.join((
                        "From: %s" % FROM,
                        "To: %s" % TO,
                        "Subject: %s" % SUBJECT ,
                        "",
                        text
                        ), "\r\n")
                        server = smtplib.SMTP('localhost')
                        server.sendmail(FROM, [TO], BODY)
                        server.quit()



#get current date n time in a manner i can stamp it on to a filename ;)
now = datetime.datetime.now()
cur= now.strftime("%Y_%m_%d_%H_%M")

#the postgres command to dump all db stuff
shellcommand='pg_dumpall >'
filename ='talentcall_back'+cur
command =shellcommand+filename
try :
        os.system(command)
        time.sleep(5)
        s3upload(filename)
except IOError as e:
        panic(e)
                                                                                                                                              1,1           Top
