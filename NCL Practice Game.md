
## Cryptography

### Decoding 2

I was given 2 flags to decipher. Because the cyphered flags were short I knew that the cipher must take a key as input (alphabetic substitution is right out) and be fairly simple due to the limited size. One such cipher is the Vigenère cipher which I tried with each letter of the alphabet as a key. Each flag was decoded with a different letter. I used CyberChef for deciphering

![[Pasted image 20231010180428.png]]
### Decoding 4

An image was given to decode:
![[Pasted image 20231009115419.png]]

Which I was able to transcribe to the text below. using that tool, I was able to decrypt it. I had to increase the dictionary weight and increase the iteration count a lot in order to solve it.

![[Pasted image 20231009115245.png]]

### Decoding 5

![[Pasted image 20231009120803.png]]

The following text is given:

TAQBEJPGXSYTVKAJLRIENVO
HATEFBOTGOUSGHHDFDGPHEL
EGIROWWMPRJDGNEASWHVFEU
FXSTLSITEMXRACESHZTESKF
LVGHLANETKDYSDAREQSEIFR

I tried decoding it but had no luck. Then I realized that both the nonogram and the text is 5 by 23. Which indicates that perhaps if I take each char which is black on the nonogram I will get the flag.

```
T   E  GXSY   A   IENVO
HA  F OT     H D  G
EGIRO W      N A  HVFEU
F STL I     ACESH T
L  HL NETKD S   E SEIFR
```

Which is:

TEGXSYAIENVO
HAFOTHDG
EGIROWNAHVFEU
FSTLIACESHT
LHLNETKDSESEIFR

without spaces. Still gibberish, but I will try to decode it. Decoding attempts failed.
Wait... reading it vertically says "theflagisrthefollowingtextskydashncaedasheightsevenfivefour" which reads: the flag is the following text sky dash ncae dash eight seven five four
So the flag is `sky-ncae-8754`

### Steganography (medium)

I was given the image harddrive.txt. I tried using binwalk and strings to no success. I then used stegOnline and checked bit planes but had no luck. I also looked at the binary with 010 editor. I considered the possibility that the AR codes in the image were a lead, but the resolution was surely too low for them to be readable. I finally used Aperisolve, a great stegsolving tool, and steghide found a txt file which contained the answer.

## Cracking

### Cracking 4 (hard)

I was tasked with cracking 5 hashes. The passwords are based off of American tv shows. I found a list of 800 TV shows and a ruleset for permutations and tried cracking the shows with and without spaces. However, I was not successful. I then found a more extensive list of 6000 shows (Alphabetically indexed lists of television programs from Wikipedia). Many titles had the year of production in parentheses after the title, so I asked chatGPT to write a Python script to remove them. It did, using regex, and I ran the script. Using the larger list and the medium intensity ruleset resulted in 2 of the passwords being cracked. The passwords seemed to be unaltered names of shows, without spaces.

![[Pasted image 20231009155557.png]]

I tried cracking on the large ruleset and found another password (below). It also had no modifications other than spaces, which indicates that the medium ruleset doesn't try removing all spaces. Maybe it removes a certain number of them. 2 passwords are still unaccounted for.

93abd6297eb91aa8efa153484ec580ab:TheSuiteLifeonDeck 

For the final 2, I made the list more extensive by adding currently airing shows, which may not have been on the list. I then used a Python script to remove the spaces.

![[Pasted image 20231009161039.png]]

I also added back in the shows with years included, with spaces removed. Now the file is 14,818 lines long.

The final attempt was unable to uncover more passwords. They may feature incomplete show names, are only related to the shows (i.e. character names rather than show names)  or feature more extensive changes. I'm going to give up on these for now.

In the end, I checked 52,602,462,654 passwords.

### PDF (Medium)

I tried using a pdf password protection removing website first, but it seems like it only removes passwords from protected but not encrypted documents. Makes sense. Next, I found that there's a utility on Linux called pdfcrack which I tried. However, it was terribly slow, so brute forcing the password was not viable. I decided that a faster method must be possible and indeed it is. I found a Python script called pdf2john which extracts the password hash from the pdf, for use in John the ripper. with some formatting changes, I readied it to use with Hashcat. Hashcat was much faster than pdfcrack, but still didn't get anywhere with brute forcing. I tried a dictionary attack using the rockyou file I had from previous challenges, and that worked. 

![[Pasted image 20231009175600.png]]

### Cracking 5 (hard)

I got Hashcat to run on my GPU so it runs faster. I did the first cracking attempt using the rockyou password list for a dictionary attack and got the first 3 passwords immediately. 

For the 4th password, I used a hybrid attack of the rockyou dictionary plus the medium rule set.

I got a weird graphical error possibly caused by nano for windows:
![[Pasted image 20231009194828.png]]

I tried the rockyou dictionary plus the large rule set and it took 5 hours, but didn't crack the password. I think I'll try word combinations or brute force next. I checked 50,921,171,794,752 passwords. 50 trillion.
## Log Analysis

### Database Dump (medium)

![[Pasted image 20231010154717.png]]
### Intrusion Detection

I used JQ and a command from ChatGPT to find all of the unique IP addresses
![[Pasted image 20231010120612.png]]

Took a few tries to get the next one. It's more complex as the signature is inside of the alert object in the json, but not all entries in the json have alert. Giving chatgpt a larger snippet of the file helped it to figure it out.

![[Pasted image 20231010132235.png]]

For counting up the instances of categories of attack, -n can be used after uniq

![[Pasted image 20231010133404.png]]

Adding another sort can sort the output (this is for signature rather than category, for the following challenge)

![[Pasted image 20231010141311.png]]

## Forensics

### Blocked (Easy)

I'm kind of pissed at this one. The pdf features an image of a Snorlax, implying along with the title that the flag is covered by the Snorlax image. I suspected that Adobe Acrobat could edit it to get the flag, but I didn't want to use it. I tried a bunch of pdf editor websites but all of them had terrible features and didn't let me move the images. Then I tried using binwalk, which Identified that there were 3 images in the pdf but didn't extract them. Trying different flags didn't work, although it might have been possible with the right flags. In the end I caved and used a free trial for Adobe Acrobat to solve it. I can't believe they charge $20 a month to edit pdfs. Mental

![[Pasted image 20231012112553.png]]
### Docter (Medium)

I used `binwalk -Me` and it instantly solved the challenge. It extracted a whole hierarchy of files, which included the image with the answer. Did not feel like medium difficulty. I had a much harder time on the first one because I really didn't want to use Acrobat. Fuck Adobe

![[Pasted image 20231012111856.png]]
![[Pasted image 20231012111922.png]]
![[Pasted image 20231012111948.png]]

## Recon

### Port Scan (Easy)

```bash
root@kali:~$ nmap -p1-65535 target
Starting Nmap 7.92 ( https://nmap.org ) at 2023-10-12 21:02 UTC
Nmap scan report for target (10.7.71.68)
Host is up (0.0000090s latency).
rDNS record for 10.7.71.68: 65258992c912c56875c0ae59.c-616f1ba2881ec8a643b6b84e-t-651ef8258c0399153e84f44b-port
Not shown: 65531 closed tcp ports (reset)
PORT     STATE SERVICE
28/tcp   open  unknown
487/tcp  open  saft
1500/tcp open  vlsi-lm
3201/tcp open  cpq-tasksmart
MAC Address: 02:42:0A:07:47:44 (Unknown)
```

Using ssh and ftp (assuming a file called flag.txt) on the first port was unsuccessful. I tried using nmap -A to learn more about the ports but it stalled out. I succeeded when I used netcat on the port, which returned a banner containing the flag.

I used nc again on the second port trying to get more data, but it just gave me the flag. Okay...

Same for the third flag

And the fourth!? Why does this one have a different point value if they're all solved the same way?

### Net Track (Medium)

### Who's There? (Hard)

nmap -Pn --host-timeout 201 --max-retries 0 -p 5555 127.0.0.1