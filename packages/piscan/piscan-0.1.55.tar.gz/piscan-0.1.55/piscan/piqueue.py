#!/usr/bin/env python
from __future__ import division
import pika
import sys
import json
import os
import subprocess
import boto
import time
from boto.s3.key import Key
from boto.sqs.message import Message
import logging
import logging.handlers
import argparse
import ConfigParser
import string

config = ConfigParser.ConfigParser()
config.read("/etc/piscan/piscan.ini")

#time.sleep(5)

#LOG_FILENAME = config.get("system", "logloc") + "/piqueue.log"
LOG_FILENAME = "/var/log/piqueue.log"
LOG_LEVEL = logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

#sys.stdout = MyLogger(logger, logging.INFO)
#sys.stderr = MyLogger(logger, logging.ERROR)

logger.info("*** Starting PiQueue.Py ***")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

z = "~"

#def SendQueue(message):
#        try:
#            logger.debug("Connecting to CutQ")
#    	    connection1 = pika.BlockingConnection(pika.ConnectionParameters(host='rxwave.com', port=5672, virtual_host='/', credentials=pika.credentials.PlainCredentials('piscan', 'magic4update')))
#	    channel = connection1.channel()
#	    channel.queue_declare(queue='CutQ', durable=True)
#	    channel.basic_publish(exchange='', routing_key='CutQ', body=message, properties=pika.BasicProperties(delivery_mode = 2,))
#            logger.info("send message to CutQ - " + message)
#	    connection1.close()
#        except:
#            logger.error("Unable to send message to CutQ")

def digits(x):
    return int(100*x)/100.0

def callback(ch, method, properties, body):
    logger.debug("*** Message Recevied (" + body +") ***")

    try:
        a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w = body.split("~")
        RID,hash,filename,CutLen,freq,SysSite,Group,Channel,SysType,Modulation,PL,CuDT,RSSI,SqNm,o,p,q,r,s,t,u,v,w = body.split("~")
        aa = "0"
        try:
            path="/etc/piscan/" + str(n) + ".wav"
            fl=open(path,"rb")
            logger.info("WAV Open : " + str(n) + ".wav" )
            fl.seek(28)
            aa = fl.read(4)
            fl.close()
            byteRate = 0
            for ii in range(4):
                byteRate=byteRate + ord(aa[ii])*pow(256,ii)
            fileSize = os.path.getsize(path)  
            ms = ((fileSize - 44) * 1000) / byteRate
            ctln =  digits(ms/1000)
            aa = str(ctln)
            CutLen = aa
        except:
            logger.error("Unable to determine WAV size")


        logger.debug("Converting WAV")
        subprocess.call(["sudo", "/usr/bin/lame", "-b 32", "-f", "/etc/piscan/" + str(n) + ".wav", "/etc/piscan/" + str(n) + ".mp3"])

        fls = 0
        bb = os.path.getsize("/etc/piscan/" + str(n) + ".mp3")
        logger.debug("MP3 File Size: " + str(fls))

        message='{'
        message = message + '"RID": ' + RID + ','
        message = message + '"Hash": "' + Hash + '",'
        message = message + '"FileName": "' +  filename  + '",'
        message = message + '"Freq": ' + freq + ','
        message = message + '"CutLen": ' + CutLen + ','
        message = message + '"SysSite": "' + SysSite + '",'
        message = message + '"Group": "' + Group + '",'
        message = message + '"Channel": "' + Channel + '",'
        message = message + '"SysType": "' + SysType + '",'
        message = message + '"Modulation": "' + Modulation + '",'
        message = message + '"PL": "' + PL + '",'
        message = message + '"TGID": "' + TGID + '",'
        message = message + '"RSSI": ' + RSSI + ','
        message = message + '"Modulation": "' + Modulation + '",'
        message = message + '"CutDt": "' + CutDt + '",'
        message = message + '"SeqNum": "' + SqNm + '",'
        message = message + '}'

        logger.debug("Sending MP3")
        s3_connection = boto.connect_s3(anon=True)
        bucket = s3_connection.get_bucket("cuts",validate=False)
        # try
        key = bucket.new_key('audio/' + str(a) + "_" + str(n) + '.mp3')
        # EXCEPTION HERE
        #     LOGGING HERE
        key.set_contents_from_filename('/etc/piscan/' + str(n) + '.mp3', reduced_redundancy=True)
        #key.set_acl('public-read')
        logger.debug("Send MP3 Successful")

        logger.debug("Sending CutQ message")

        cutqstr = str(a)+z+str(b)+z+str(c)+z+str(d)+z+str(e)+z+str(f)+z+str(g)+z+str(h)+z+str(i)+z+str(j)+z+str(k)+z+str(l)+z+str(m)+z+str(n)+z+str(o)+z+str(p)+z+str(q)+z+str(r)+z+z+z+z+z+z+z+z+z+str(aa)+z+str(bb)
        cutqstr = message
	#SendQueue(cutqstr)


        aws_access_key_id='AKIAIRB443KH6BYRQTWA'
        aws_secret_access_key='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'
        conn = boto.sqs.connect_to_region("us-east-1", aws_access_key_id='AKIAIRB443KH6BYRQTWA', aws_secret_access_key='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')
        logger.debug("Connecting to SQS")
        my_queue = conn.get_queue('inbound')
        logger.debug("Connecting to inbound")
        m = Message()
        m.set_body(cutqstr)
        logger.debug("Sending message")
        my_queue.write(m)
        logger.debug("Message Sent")

        logger.info("Sent: " + cutqstr)

        logger.debug("Deleting MP3")
        os.remove("/etc/piscan/" + str(n) + ".mp3")

    except:
        logger.debug("*** Message from LameQ incorrect size - skipping (" + body +") ***", exc_info=True)

    logger.debug("Deleting WAV")
    try:
        os.remove("/etc/piscan/" + str(n) + ".wav")
    except:
        logger.error("Unable to delete WAV")


    ch.basic_ack(delivery_tag = method.delivery_tag)


logger.debug("Connecting to  queue")
channel.queue_declare(queue='LameQ', durable=True)

logger.debug("Starting Consumption")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='LameQ')
logger.debug("Starting Consumption - 2")
channel.start_consuming()




