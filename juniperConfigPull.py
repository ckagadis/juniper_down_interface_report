from hosts import hostname
from defs import superCopy
import re
import sys
import os
import paramiko
import time
import getpass

"""
This script was written to assist in the retrieval of a list of network ports on Juniper network switches that have been in a "down" status for 12 weeks or more or have never been brought to an "up" status.

Resources:
https://regex101.com/

"""
os.system('clear')

try:
    userName = str(input("Please enter username: "))
    passWord = getpass.getpass("Please enter password: ")
except:
    e = sys.exc_info()[0]
    print("Unexpected error:", sys.exc_info()[0])
    raise

i = 0 # Counts the number of times our while loop will run.

print("********* DOWN NETWORK INTERFACE REPORT *********")

while i < len(hostname): # While loop will run so long as the value of the "i" variable is less than the total number of hosts is the "host" list.
    try:
        hostNameCommandOutput = os.popen("nslookup " +  hostname[i]).read() # Retrieve the hostname of the network switch and store it as 'hostNameString' silently.
        remote_conn_pre=paramiko.SSHClient()
        remote_conn_pre
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(hostname[i], username=userName, password=passWord, look_for_keys=False, allow_agent=False, timeout=2)

        hostnameString = re.findall(r'\bname = \S+', hostNameCommandOutput)[0]
        hostnameString = hostnameString.replace('name = ', '') # Get rid of the string "name = " from the output of hostnameString

        sys.stdout = open('./output/' + hostnameString + 'txt', 'wt')
        hostnameString = hostnameString.replace('.com.', '.com') # Get rid of the string "name = " from the output of hostnameString

        print("SSH connection established to " + hostname[i] + " (" + hostnameString + ").\n")

        remote_conn = remote_conn_pre.invoke_shell()
        time.sleep(1)
    except:
        #print(EnvironmentError) # For debugging
        print("Could not connect to " + hostname[i] + ".  Please verify that the hostname is spelled correctly and that the authentication has been set properly.")

        hostnameString = re.findall(r'\bname = \S+', hostNameCommandOutput)[0]
        hostnameString = hostnameString.replace('name = ', '') # Get rid of the string "name = " from the output of hostnameString

        sys.stdout = open('./output/' + hostnameString + 'txt', 'wt')
        hostnameString = hostnameString.replace('name = ', '') # Get rid of the string "name = " from the output of hostnameString
        hostnameString = hostnameString.replace('.com.', '.com') # Get rid of the string "name = " from the output of hostnameString

        print("Could not connect to " + hostname[i]+ " (" + hostnameString + ").  Please verify that the hostname is spelled correctly and that the authentication has been set properly.")
        sys.exit()
    else:
        remote_conn.send('set cli screen-length 10000\n')
        time.sleep(2)
        remote_conn.send('edit\n')
        time.sleep(2)
        remote_conn.send('run show interfaces | match "Physical interface: ge" | match "Down"\n')
        time.sleep(25)
        output = remote_conn.recv(500000)
        #print(output.decode()) # For debugging
        interfaceOutput = output.decode()

        #print(interfaceOutput) # For debugging
        interfaceOutputList = re.findall(r'\bge-[0-9]/[0-9]/[0-9]\S', interfaceOutput) # retrieve interface names interfaceOutput that are in the 'down' state

        j = 0

        while j < len(interfaceOutputList):
            interfaceOutputList[j] = interfaceOutputList[j].replace(',', '')
            #print(interfaceOutputList[j]) # For debugging
            remote_conn.send('run show interfaces ' + interfaceOutputList[j] +  '| match "ge|flap"\n')
            time.sleep(1)
            output = remote_conn.recv(500)
            try:
                if str("Never") in output.decode(): #Evaluate if the interface has never flapped.
                    remote_conn.send('show interfaces ' + interfaceOutputList[j] + ' unit 0 family ethernet-switching vlan\n')
                    time.sleep(1)
                    output = remote_conn.recv(500)
                    vlanOutput = output.decode()
                    if not (re.findall(r'\bmembers (\S+|\s+|\D+|\d+|\D+\d+\W+]);', vlanOutput)): # Evaluate if the never flapped interface is a member of a vlan.
                        print(interfaceOutputList[j] + "    Last flapped   : Never.  Member: NONE")
                    else:
                        print(interfaceOutputList[j] + "    Last flapped   : Never.  Member: " + re.findall(r'\bmembers (\S+|\s+|\D+|\d+|\D+\d+\W+]);', vlanOutput)[0]) # Regex pattern to retrieve vlan name
                    time.sleep(1)
                else: # The interface has flapped.  Evaluate if it has flapped over 12 weeks ago.
                    weeksDown = re.findall(r'\b\d+\w?w', output.decode())[0]
                    weeksDown = weeksDown.replace('w', '')
                    weeksDown = int(weeksDown)
                    if weeksDown >= 12: # Evaluate if the interface has flapped 12 or more weeks ago.
                        #print(weeksDown) # For debugging
                        remote_conn.send('show interfaces ' + interfaceOutputList[j] + ' unit 0 family ethernet-switching vlan\n')
                        time.sleep(1)
                        output = remote_conn.recv(500)
                        vlanOutput = output.decode()
                        if not (re.findall(r'\bmembers (\S+|\s+|\D+|\d+|\D+\d+\W+]);', vlanOutput)): # Regex pattern to retrieve vlan name
                            print(interfaceOutputList[j] + "    Last flapped   : " + str(weeksDown) + " weeks ago.  Member: NONE")
                        else:
                            print(interfaceOutputList[j] + "    Last flapped   : " + str(weeksDown) + " weeks ago.  Member: " + re.findall(r'\bmembers (\S+|\s+|\D+|\d+|\D+\d+\W+]);', vlanOutput)[0]) # Regex pattern to retrieve vlan name
                        time.sleep(2)
                        #print(re.findall(r'\b\d+\w?w', output.decode())[0])
                    else: # The interface has flapped within 12 weeks.
                        #print(interfaceOutputList[j] + "    Down less than 12 weeks.") # For debugging.
                        pass
            except IndexError: # The interface has flapped less than a week ago.
                    #print(interfaceOutputList[j] + "    Down less than a week.") # For debugging.
                    pass

            j += 1

        remote_conn_pre.close()

    print('\n')

    i += 1

superCopy()
