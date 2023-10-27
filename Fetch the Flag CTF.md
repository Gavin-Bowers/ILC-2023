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

