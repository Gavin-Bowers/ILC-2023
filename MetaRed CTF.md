
## Crypto

### Alien Message

Using Google's find Image source found that this is the font from futurama, which makes sense given the omicron reference and explains why it looked familiar. I found an online font for it which indicates that the text says: "you have saved your planet"

![[Pasted image 20231121080046.png]]

I failed to submit the flag the first few times because it turns out it is in all caps. The letters look the same when capitalized so I couldn't tell.

## Misc

### ARP spoofing

This challenge provides a package capture file for an ARP spoofing attack and the flag is the mac address of the attacker. I'm not sure how to identify the attack but I knew the perp would be one of the 4 sources sending ARP packets, so I just tried all of them.

![[Pasted image 20231121094212.png]]

## Cryptography (why is this a different section than crypto?)

### Personal Encryption

This challenge literally tells you that the encryption is ceaser with a different value for each word. It provides a date and time which are somehow encoding the ceaser keys but they aren't necessary because ceaser is trivial to brute force