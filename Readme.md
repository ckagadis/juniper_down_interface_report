Author's Note:
--------------
BEFORE USING ANY CODE IN THESE SCRIPTS, READ THROUGH ALL FILES THOROUGHLY, UNDERSTAND WHAT THE SCRIPTS ARE DOING AND TEST THEIR BEHAVIOR IN AN ISOLATED ENVIRONMENT.  RESEARCH ANY POTENTIAL BUGS IN THE VERSION OF THE SOFTWARE YOU ARE USING THESE SCRIPTS WITH AND UNDERSTAND THAT FEATURE SETS OFTEN CHANGE FROM VERSION TO VERSION OF ANY PLATFORM WHICH MAY DEPRECATE CERTAIN PARTS OF THIS CODE.  ANY INDIVIDUAL CHARGED WITH RESPONSIBILITY IN THE MANAGEMENT OF A SYSTEM RUNS THE RISK OF CAUSING SERVICE DISRUPTIONS AND/OR DATA LOSS WHEN THEY MAKE ANY CHANGES AND SHOULD TAKE THIS DUTY SERIOUSLY AND ALWAYS USE CAUTION.  THIS CODE IS PROVIDED WITHOUT ANY WARRANTY WHATSOEVER AND IS INTENDED FOR EDUCATIONAL PURPOSES.  

Juniper Switch Down Interface Report
=======================================================
This script was written to assist in the retrieval of a list of network ports on Juniper network switches that have been in a "down" status for 12 weeks or more or have never been brought to an "up" status.  While it was originally written for a specific purpose, it can also be used as a general framework in other uses.  It was initially conceived as a way of pulling information from a Juniper network switch or list of switches (specifically the Juniper Ex 4200) by;

- Authenticating to a host via SSH
- Executing commands and receiving the output of said commands
- Parse through the output via regex
- Execute code against the parsed output

These four operations can be used in any case where a user uses SSH to connect to a machine to execute commands.  Because commands and the output of said commands can vary, the time.sleep() and remote_conn.recv() arguments in the program can be adjusted to fit each situation.  

Maintainer:
----------
Chris Kagadis
