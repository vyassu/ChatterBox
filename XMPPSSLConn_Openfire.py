import sys, ssl
import logging
import sleekxmpp
import xml.etree.ElementTree as ET
from optparse import OptionParser

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

class XMPPConnMgr(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password,encryption=True):
        sleekxmpp.ClientXMPP.__init__(self, jid, password,sasl_mech="PLAIN")
        # Plugins that needs to be registered
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.response_timeout = 10000

        # SSL Configuration
        #   Ca certs points to the system trustore located at /etc/ssl/certs
        #   certfile points to the certificate file of the client
        #   keyfile points to the key file of the client

        if encryption:
            self.ca_certs = "/etc/ssl/certs/ca-certificates.crt"
            self.certfile = "/home/vyassu/cert/Openfire/node0@localhost.crt"
            self.keyfile = "/home/vyassu/cert/Openfire/node0@localhost.key"
        else:
            self['feature_mechanisms'].unencrypted_plain = True
        self.roaster = {}                                                   # Variable to store all friends/peer
        self.add_event_handler("session_start", self.start)                 # Registering event handler

    # Method to create connection to XMPP server
    def conn(self,useTLS=True):
        if conn.connect(("localhost", "6222"), use_tls=useTLS):
            conn.process(block=False)
            print("Connection established....")
            print ("JID after connection:: ", conn.jid)
            return True
        else:
            print("Unable to connect.")
        return False

    # Method to receieve messages from Peer/Friends
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
           if msg['subject']!="":
             msg.reply("Got it !!\n%(body)s" % msg).send()
        print str(msg['body'])

    # Method to update the status of all the peers online
    def online_friends(self,presence):
        friend = str(presence['from']).split("/")[0]
        self.roaster[friend] ="Online"
        print self.roaster

    # Method to send initial presence messages
    def start(self, event):
        self.send_presence(pstatus="Online")
        self.get_roster()
        root = ET.fromstring(str(self.get_roster()))
        namespace = {"ns":"jabber:iq:roster"}

        for element in root.findall(".//ns:query/ns:item",namespace):
            self.roaster.update({str(element.attrib['jid']):"offline"})
        print self.roaster
        self.add_event_handler("presence_available", self.online_friends)
        self.add_event_handler("message", self.message)

    # Method to send messages to Friends
    def SendMessage(self,msg,recepient):
        try:
            if len(self.roaster)==0:
                print "No friends in the Roster!!"
                return
            if self.roaster[recepient]!="Online":
                print "Friend offline.."

            message = self.Message()
            message['to'] = recepient
            message['type'] = 'chat'
            message['body'] = msg
            message['subject']= msg
            message.send()

        except KeyError:
            print "Invalid Destination/ FriendName"
        except:
            print "Unhandled exception"



if __name__ == '__main__':
    optp = OptionParser()
    optp.add_option('-u', '--username', help='your username', dest='username')
    optp.add_option('-p', '--password', help='your password', dest='password')
    opts, args = optp.parse_args()

    logging.basicConfig(level=logging.DEBUG,format='%(levelname)-8s %(message)s')

    if opts.username is None or opts.password is None:
        raise RuntimeError("No username/password provided!!!")

    print "Do you want encryption ON/OFF:"
    useTLS=True
    encryption= raw_input()
    if encryption=="OFF":
        useTLS=False

    conn = XMPPConnMgr(opts.username, opts.password,useTLS)        ## Connection manager

    # Start sending messages only after successful connection with XMPP server
    if conn.conn(useTLS):
        print "Ready to send message!!!"
        print "Enter friend/target system name/JID"
        recepient = raw_input()
        exit = "Y"
        while(exit !="N"):
            print "Enter your message::"
            message = raw_input()
            conn.SendMessage(message,recepient)
            print "Do you to continue(Y/N):"
            exit = raw_input()
    conn.disconnect(wait=True)
    #conn.keyfile="/home/vyassu/cert/Openfire/vyassu@nm.vyassu-qv15971.ufl-eel6892-sp16-pg0.wisc.cloudlab.us_in.key"
    #conn.certfile="/home/vyassu/cert/Openfire/vyassu@nm.vyassu-qv15971.ufl-eel6892-sp16-pg0.wisc.cloudlab.us.crt"

