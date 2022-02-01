# DDOSER

This service is used to simulate the behaviour of a DDOS yoyo attack.

###How? 
Sending multiple requests to a server from different processes.
Each process simulates a user.

###Classes
####Runner
This class initialize and control the attacker processes.


####Attacker
Each attacker is a process. 
Each process wait for a signal from the Runner, and only when all attackers are ready, start running the yoyo attack.