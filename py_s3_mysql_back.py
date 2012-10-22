#!/usr/bin/python
import time
import MySQLdb
import os
import smtplib
filestamp = time.strftime('%Y-%m-%d')


def panic(stacktrace):
		print stacktrace
		print "Error !!"
		sender = 'database_backupmanager@urdomain.com'
                receivers = ['team@somthing.com']
                message = """From: From Database Manager <database_backupmanager@urdomain.com>
                To: To Person <anto@domain.com>
                MIME-Version: 1.0
                Content-type: text/html
                Subject:Database Backup Manager

                Scheduled DB backup failed !!!.
                """
                smtpObj = smtplib.SMTP('localhost')
                smtpObj.sendmail(sender, receivers, message)
                print "Successfully sent email"



def s3upload(backupfile):
		try:
                        from boto.s3.connection import S3Connection
                        conn = S3Connection('acces key', 'access token')
                        from boto.s3.key import Key
                        b=conn.get_bucket('bucket name')
                        k=b.new_key(backupfile+filestamp)
                        k.set_contents_from_filename(backupfile+filestamp)
                        #clear the pg dump in local
                        syscommand='rm '+backupfile+filestamp
                        os.system(syscommand)
                        print "Uploaded to s3 and deleted from local !"
		except IOError as e:
                        panic(e)
                        print e




user='username'
passwd='password'
host='localhost'

try:
	conn = MySQLdb.connect (host, user, passwd)

	cursor = conn.cursor()

	cursor.execute("SHOW DATABASES")

	results = cursor.fetchall()
	cursor.close()
	conn.close()

	for result in results:
    		backupfile=result[0]+".sql.gz"
    		cmd="echo 'Back up "+result[0]+" database to yourLocation/"+backupfile+"'"
    		os.system(cmd)
                cmd="mysqldump -u "+user+" -h "+host+" -p"+passwd+" --opt --routines --flush-privileges --single-transaction --database "+result[0]+" | gzip -9 --rsyncable > /home/bitnami/database_back/"+backupfile+filestamp
    		os.system(cmd)
		s3upload(backupfile)
                  
except IOError as e:
		panic(e)
