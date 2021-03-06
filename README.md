# ChatterBox
Python based chat client using SleekXMPP.

##Prerequistes
There are lot of XMPP servers out there, but I would prefer Openfire. The below are the commands required to setup Openfire on your localsystem to test ChatterBox. For flexibility purpose I have used MySQL as the database for storing configuration details of the Openfire server.

```
1.) Download the latest JRE:
  $sudo apt-add-repository ppa:webupd8team/java 

if the command throws an exception run the below command first:
  $sudo apt-get install software-properties-common python-software-properties

Then execute 
  $sudo apt-add-repository ppa:webupd8team/java
  $sudo apt-get update
  $sudo apt-get install oracle-java8-installer

2.) Download the latest Openfire executable from http://www.igniterealtime.org/downloads/.
(http://download.igniterealtime.org/openfire/openfire_4.0.2_all.deb)
  $sudo dpkg -i openfire_4.0.2_all.deb
				or
  Execute the command 
  $sudo apt-get install openfire


3.) Download MYSQL server instance
  $sudo apt-get install mysql-server

4.) Create a table with database name "openfire" using the below command:
  $mysql -u <username> -p<password> -e "CREATE DATABASE openfire;"
  
5.) Download and Install SleekXMPP from here --> https://github.com/fritzy/SleekXMPP

```

## Get the code
```
    $git clone "https://github.com/vyassu/ChatterBox"
    $cd ChatterBox
```

## Test
Currently ChatterBox supports two modes of operation encrypted and unencrypted mode. For encrypted mode it is necessary to install Public-Private keys both on your local system and as well as on the XMPP server. The below steps are for Encrypted mode of operation.
```
   $cd ChatterBox
   $python XMPPSSLConn_Openfire.py -u <JID> -p password
```
After executing the above mentioned commands a command line interface appears follow the instructions to get connected to the XMPP chat server and to start sending messages.

