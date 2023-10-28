![[Pasted image 20231027125746.png]]

Team:
Floppa Nation
*pGvYciyFWo*E3tut&rzuAsa

### Color Picker
In this problem, we have a color picker. Only the color value is being sent to the server so that's our attack surface. We do get the color back, so we can get info.

Assuming the server is storing users in an SQL database, the command to set color may look something like:

```SQL
UPDATE users
SET profilecolor = 'hexcolor'
WHERE username = 'johndoe'
```

We have control over hexcolor, so we can enter some kind of sql injection attack

I tested, and sending an invalid color works 
![[Pasted image 20231027131757.png]]

I tried some SQL attacks but nothing worked.

Then I remembered that I have the source code, which confirms that it isn't SQL based at all.

Now I have no Idea how to do the attack

### Read the rules

They actually hid the flag in the html. I downloaded it and used control-f in VSCode

### Nine One Sixteen

This is an Osint challenge to find the contact info for a ficticious company. We are provided a website with broken links and no information. The name RFC9116 leads to a security standard, which is interesting but doesn't help me find the flag.
Doing a copyright search (since the page has a copyright at the bottom) yielded no results. Looking at the page's html also didn't reveal anything. 

When I was reading about RFC 9116 on WIkipedia, I realized that what it mandates is for websites to have a security file accesible under the /security.txt or /.well-known/security.txt directories. Trying these directories on the website found me the flag.

### Finder's keepers

In this challenge, I connect to a server via ssh. There's a directory, which contains the flag, but I can't access it.

![[Pasted image 20231027142724.png]]

I learned that Patch's directory has group read permissions with ls -l, but trying to add myself to his group with newgrp requires a password I don't have

### Rusty

For this challenge, a rust program is provided along with an encoding of the flag it produced. The code takes the input string as bytes, and takes 6 bits of it at a time which are used to index into a charset to create the encoding. The following Python program does the opposite:

```Python
CHARSET = "QWlKoxp3mT9EeRb4YzgG6rNj1OLvZ5SDfMBaXtP8JyIFVH07uh2wicdnUAC#@q"
def decode(encoded):
	raw = [] 
	for char in encoded: 
		if char == '=': 
			continue
		raw.append(CHARSET.index(char))
	bits = ''.join(bin(r)[2:].zfill(6) for r in raw) 
	bytes_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8) if i+8 <= len(bits)]
	return ''.join(chr(b) for b in bytes_list)

flag = decode("OPhMOnVheP1hRaOa1Pmi1GrBbGm21PRaepxXOPxMeG1iOaYd1ji=") print(flag)
```

### Quick Maths

For this challenge, you connect to a server via netcat and must answer math questions. The catch is that you have to answer them very fast. Too fast to do by hand. So, I wrote a python script to do it. The math appears to work, but I wrangled with formatting for way too long before giving up. The issue is that I need to enter something, like newline, to get the next line from the server, but it considers that to be part of my answer, and so my answer is wrong. The math in my program works, but I can't get it to just read the answer. I don't have this issue in netcat, but using python I do. I tried writing a bash script but it had the same problem.

### YSON

This challenge features a website which turns yml into json. I tried escaping the input using a ' and got this error:

Error: while scanning a quoted scalar in "", line 12, column 1: ' ^ found unexpected end of stream in "", line 12, column 2: ' ^

Two quotes gets:

Error: while scanning a simple key in "", line 12, column 1: "" ^ could not find expected ':' in "", line 12, column 3: "" ^

This is a yml parser error apparently

### Beep64

This challenge provides an audio file, says that it uses base64, and asks us to find the flag. Listening to it, it sounds like a series of tones, so it must encode data with tones. After some analysis, it seems like it's DTFM, an old system used by touch-tone telephones. Which explains why it sounds like old phone noises. I found a Python program which can...



