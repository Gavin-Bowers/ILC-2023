### OSINT 1

part 1:
![[Pasted image 20231020102138.png]]
part 2:
![[Pasted image 20231020102545.png]]
I found the full key with this website, but not the email address. I though that using a somewhat complicated script which I would have to modify would be required to get the email (script here: https://github.com/catalyst256/MyJunk/blob/master/decode-pgpsig.py), but it turns out there' a better way. https://nixintel.info/osint-tools/using-pgp-keys-for-osint/ has a much simpler solution:

```bash
curl https://d.peegeepee.com/key_sig_here.asc | gpg
```

This didn't work because the website it refers to no longer exists, but I have the key from keys.openpgp.org so I can use that

![[Pasted image 20231020104025.png]]
Which tells is when it expires (the next question), but not the email address. Not sure why. I'm going to move on as this isn't worth the time it's taking

### Osint 2

The questions are all answered on various pages of https://www.submarinenetworks.com/ but googling is the best way to find them since the site isn't well organized

### Osint 3

I can find github.com's TLS certificate (Not to self: SSL is the outdated form of TLS, and is sometimes still used to refer to TLS) by clicking the lock next to the url in Vivaldi and clicking "connection is secure", bringing up this menu with info:
![[Pasted image 20231020110955.png]]

Entering the certificate fingerprint into https://crt.sh/ searches for the certificate logs. I found the info for that certificate, but not previous ones by github. Searching Github on the site finds all of the certificates related to github, and ordering them by expiry date allowed me to find the desired certificate:
![[Pasted image 20231020111639.png]]

And here's the serial number:
![[Pasted image 20231020111736.png]]

The following question is just the same but for cyberskyline.com. It's trivial now that I have the workflow

The last one requires finding a certificate with a specific serial number. This didn't work on crt.sh so I got worried, but it just requires using advanced search
![[Pasted image 20231020112309.png]]

### Osint 4

https://afdc.energy.gov/fuels/electricity_locations.html#/station/218666 can be used to search for charging stations by location. It gives a wealth of info, including the charging network and the plug types. The last questions asks about the plug type, and I couldn't get it to accept any answer. Not sure if it's a formatting issue, or if there's a sneaky charging station closer to the specified location

### Osint 5

I've got an image of a building, and I need to find info about the tree out front. Reverse image searching with google finds that the building is the Citicorp Center at 601 Lexington Avenue. Yeah, the one that was accidentally built structurally unsound and had to be reinforced in place so it didn't topple. That one.

I found the tree in street view to get a better look. A plant identification website identified the tree (from as street view screenshot) as a Willow Oak, which is correct.

I figured I could find the number of the tree in an architectural plan which includes it, but haven't been able to find one. I think it's not worth my time.

## Cryptography

### Crypto 1

cyberchef data type conversion

### Crypto 2

boxentriq cipher identifier and cipher solvers (with auto solve setting turned up to increase search space)

### Crypto 3

First one is a url with url encodeing. Cyberchef has a url decode option which reverses it. The second one is the same. The third one is url encoded twice.

### Crypto 4

I spent 20 points on the hint because I was pretty sure that the encoding scheme is element, word, letter from a NCL webpage but I tried FAQ as it had neatly ordered elements, and it didn't work, so I was stumped. The hint pretty much says outright that it's the FAQ. Looking at the title 'rulebreaker' It's so obvious, but I didn't think the title would have relevant info. Dang. I can still get 40 points though. The code is actually section, element, word.

```
[1, 4, 1] I
[11, 4, 2] follow
[2, 2, 5] the
[4, 1, 48] rules
[1, 14, 42] 365
[1, 14, 43] days
[2, 1, 12] a
[1, 9, 15] year. 
[2, 4, 11] You
[6, 3, 8] will
[5, 1, 54] also
[11, 4, 2] follow
[2, 2, 5] the
[4, 1, 48] rules.
```

1 doesn't have a section 9 or 14, so I'm confused. It appears that counting all of the bullet points and not the numbered items works for section 1. I got the answer wrong at first because I entered 356 instead of 365, but it was still wrong after fixing that. I realize that I'm using "to" instead of I for the first entry, which was based on my incorrect understanding of section 1.

### Crypto 5

This challenge provides a png which apparently has half of it encrypted. The info for decyption is also in the image. Running Aperisolve on it finds the txtKey: The_Vault's_Open,IV: taylor's_version in the metadata via Exiftool (originally they were encoded as html objects so I used Cyberchef). I also noticed that there's a formatting pattern for pngs which ends halfway through the file. I think I need to copy out the encrypted half, decrypt it, and add it back.

I copied out what I thought is the correct bytes and tried to decrypt it but had no success. I'm not sure if the decryption or the bytes selected are wrong

### Crypto 6

The emojis provided correspond to the following numbers

```
[649,
 633,
 622,
 627,
 559,
 629,
 648,
 648,
 575,
 628,
 580,
 636,
 560,
 616,
 629,
 628,
 629,
 580,
 639,
 605,
 640,
 580,
 639,
 638,
 620,
 601,
 619,
 601,
 634,
 605,
 636,
 650,
 656]
```

🦎A
🦅B
🦡C
🐣D
🐒 E
🐥F
🐢G
🐢G
🐅 H
🐤I
🐎J
🦉 K
🦍L
🐨 M
🐥F
🐤 I
🐥F
🐎J
🦩N
🐁O
🦚P
🐎J
🦩N
🪶 Q
🦨R
🦣S
🦦T
🦣S
🦆U
🐁O
🦉K
🐍V
🐋W
A BCDE FGGH IJK LM FI FJNO PJNQ RSTS UOKVW
🦎 🦅🦡🐣🐒 🐥🐢🐢🐅 🐤🐎🦉 🦍🐨 🐥🐤 🐥🐎🦩🐁 🦚🐎🦩🪶 🦨🦣🦦🦣 🦆🐁🦉🐍🐋

This looks like an alphanumeric substitution cipher, but with the wide range of letters used and the limited amount of text, I haven't been able to crack it. It may be another cipher or encoding scheme entirely, but I don't know what the numbers could correspond to.

## Cracking

### Cracking 1

I used the syntax `echo -n XR6497KV\"\@\/ | sha512sum` with each password and corresponding hashing algorithm. (md5sum, sha1sum, etc.). For the last one (included above) I had to escape some characters with \

### Cracking 2

This challenge has hashes to crack with rockyou.txt as the dictionary. This is done easily with Hashcat. `hashcat -m 0 hashes rockyou.txt -O`

### Cracking 3

This problem has Windows keys dumps, which can be cracked with `hashcat -m 1000 hashes dictionary_here -O`. I tried rockyou to no success, then tried a large dictionary. If that fails, I will try Windows key rainbow tables, which can be downloaded online. Although I'm surprised that an easy problem would require that.

### Cracking 4

These hashes are outputted from the Unix `crypt()` function. The following command uses hashcat to crack them: `hashcat hashes2 -m 500 -a 3 SKY-hash_goes_here-?d?d?d?d -O` 

### Cracking 5

I found a list of all city names from Geonames. Searching "database" can be more helpful than "list" when searching for extensive lists of things. It was in json format with other data, so I used JQ to extract the names of cities only and put them in a text file: `jq -r '.[].name' cities.json > city_names.txt`

The following command performs the attack `./hashcat.exe -m 500 -a 6 ../hashes3 ../city_names.txt ?d?d -O`
(I use Windows and Linux Hashcat for performance and convenience respectively)
-m 500 refers to the crypt() format which the hashes are in. -a 6 specifies a hybrid dictionary and mask attack, which then uses city_names as the dictionary and ?d?d as the mask

This didn't yield all of the passwords, indicating that I need more cities, or that some cities are lower case. I looked at the first question and noticed that the hash was NY. I added variations to the file so New York City was also represented as NewYork among others. This worked and I got one more password. 

Next I tried removing all spaces which worked and gave me the last two. I probably should have done that in the first place

### Cracking 6

I wrote the following script to get lists of actors and actresses from Wikipedia and copied the list of Canadian actors and actresses manually as it was only one page.

```Python
import requests
def get_actor_names_from_category(cm_title):
    base_url = "https://en.wikipedia.org/w/api.php"
    # Get list of pages in the category
    params = {
        "action": "query",
        "cmtitle": cm_title,
        "cmlimit": "500",  # Max limit allowed
        "list": "categorymembers",
        "format": "json"
    }
    actor_names = []
    while True:
        req = requests.get(url=base_url, params=params)
        data = req.json()
        # Add page titles (actress names) to the list
        pages = data['query']['categorymembers']
        actor_names.extend([page['title'] for page in pages])
        # Check for the 'continue' field in the response to get the next batch
        if 'continue' in data:
            params['cmcontinue'] = data['continue']['cmcontinue']
        else:
            break

if __name__ == "__main__":

    get_actor_names_from_category("Category:21st-century American male actors")
    get_actor_names_from_category("Category:20th-century American male actors")
    get_actor_names_from_category("Category:19th-century American male actors")
    get_actor_names_from_category("Category:18th-century American male actors")
    get_actor_names_from_category("Category:21st-century American actresses")
    get_actor_names_from_category("Category:20th-century American actresses")
    get_actor_names_from_category("Category:19th-century American actresses")
    get_actor_names_from_category("Category:18th-century American actresses")
```

I used a script I wrote to remove things in parenthesis with regex. I modified it to use command line arguments and had a hilarious error where I used `arg[0]` instead of `arg[1]`so it outputed a version of itself with anything between parenthesis removed.

I also used scripts to remove spaces and give me the first and last names without redundancy. I then ran the following command, using a ruleset to make various substitutions and additions:    
`./hashcat.exe -m 500 -a 0 -r ..\rules\clem9669_medium.rule ../hashes4 ../ns_np_all_actors_plus.txt -O`

I got one after trying various rulesets: G1ll1@nJ@cobs
It seems that my list of full names with no spaces is good, but is probably running up against the limits of the rulesets. The rulesets have limits on how far into the words substitutions are, which means that long password like these are not being covered. I'll need an even more comprehensive ruleset and perhaps run overnight to crack these

### Forensics 1

Binwalk -e extracts the images in the file. One of them contains the flag


### Enumeration and Exploitation 1

I used a python script to decrypt the flag. Notably, the AES encryption used the password and IV directly and not through a key algorithm, which through me off.

### E & E 2

I wrote a script to make the UDP request but it doesn't work and I'm not sure why

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 0))
byte_string = "0005cb7fe918aa4f5b9fc702651b335a"
server_address = ("udp-hijack.services.cityinthe.cloud", 7004)
sock.sendto(byte_string.encode() + b'c372b225b499e392', server_address)
sock.settimeout(2)
data, addr = sock.recvfrom(1024)
print("Received:", data.decode())
sock.close()
```

