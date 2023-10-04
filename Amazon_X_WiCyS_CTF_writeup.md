Amazon X WiCyS CTF writeup

I completed 3 challenges: recon 1 and 2, and web 1. I worked on but did not complete reverse engineering 1, web 2, cryptography 1 & 2, and stenography 1.
I felt fairly rusty after not doing anything computer related over the summer. I was also distracted by working on getting registered for DSA during the event.

Recon 1
This task involved finding a bad actor by their username somewhere on the internet. At first I tried googling the username but it didn’t work. Then I used a person search tool, since the username seemed like a regular name. It also didn’t work. Finally, I used a tool to search for usernames on various websites, and it found a number of hits. The first one I checked was on Twitter, which was indeed the bad actor.

Recon 2
For the second recon task, I was to find the hidden Discord server where the bad actor was recruiting hackers. I looked at the posts and followed accounts’ recent posts but didn’t find anything.
Then I noticed that the description had another username which was their “coding name’. I checked github and sure enough there was an account. It had only a hello world program in a few languages.
I checked the code but didn’t find anything. Finally, I (actually a teammate) checked the version history and found the Discord server link in an earlier version of the code.

Web 1
This task featured a website which could ping servers on the network, if given an ip. It was “secured” by filtering responses including “python” and “curl”.
I tried to run an additional command to the ping by using && and nmap to scout the network. However, I used nmap incorrectly and got an error. I eventually tried ls and found that the flag was in a file, which I used cat to read.

Reverse Engineering
The file which was given for this challenge was a zip file containing a zip file containing a couple of files with no file type.
I checked the binaries with 010 editor and found that one contained something code-like, one contained text, and others contained data with no obvious significance.
I gave a snippet of the code-like text to ChatGPT, which identified it as C++ compiler artifacts. Thinking the code was compiled C++, I tried to decompile it with Ghidra, but had no luck.
It wasn’t interpretable as assembly it seemed. There seemed to be some way of running the files, based on comments on the CTF Discord, but I couldn’t figure out how.
I did infer from the text that the program does something cryptographic, so I would have to figure out the algorithm in order to find the key.

Cryptography 1
This task gave me a large text file. It looked to be base 64 encoded. I tried decoding it with a python script but it was still encoded. I thought I was doing something wrong. 
Later I learned from a writeup that it was encoded multiple times. In retrospect it seems pretty obvious.

Cryptography 2
This challenge featured a Python script which used an insecure form of RSA to encrypt the key. I tried writing my own script to crack it, but it was more complex of a task than I thought and I had difficulty with dependencies in Python.
I considered using an existing cracking tool like Hashcat, but ended up moving on to other challenges.

Stenography
I ran the image through a number of automatic stenography websites, but didn’t get any results. Looking at the binary with 010 editor didn’t yield any results.
I’m not sure what I was doing wrong since I don’t think this one was meant to be very hard
