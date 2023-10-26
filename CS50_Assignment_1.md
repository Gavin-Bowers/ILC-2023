### As we learned in lecture, many of the most popular algorithms used today for encrypting data are public and thoroughly described in literature.

### If we are trying to protect our data from being intercepted, and potential malicious actors have access to this same literature, why is our data not necessarily at risk?

The details of encryption algorithms being available to bad actors doesn't compromise the effectiveness of the algorithms because the algorithms are designed to be resistant to attack even if the attackers have full knowledge of the algorithms. Sometimes, more efficient ways of cracking encryption algorithms are discovered, and new algorithms must be adopted. Algorithms being public increases the risk of this happening, but also ensures that good actors can verify the security of the algorithms and look for such vulnerabilities.
### In what sense might files not actually be deleted even if you empty the recycle bin on Windows or empty the trash on macOS?

When the operating system deletes files, it marks their space on the drive as being free for overwriting, but doesn't overwrite the data immediately. This can allow digital forensics to potentially recover the data.
### How do quantum computers differ from traditional (non-quantum) computers?

Quantum computers use particles in superpositions of states and which are entangled with each other. These are called Qubits, because they encode a value which is a superposition of 1 and 0. The components of a quantum computer cause Qubits to become entangled in certain ways which create quantum logic operations. By setting the state of input Qubits, the entanglement results in superpositions of states to propagate through the quantum logic components, and create a superposition in the output Qubits. When the output qubits are measured, the superposition collapses into a 0 or 1 at random, based on the probability distribution encoded by the superposition. Quantum computers give multiple results for the same input, unlike classical computers which always give the same result. By repeatedly performing a quantum computation, the probability distribution for each output Qubit can be determined. This probability distribution is the actual result of the quantum algorithm. Because of their fundamentally different approach to computation, quantum computers can perform certain algorithms many orders of magnitude better than classical computers. However, it's unknown if all classical algorithms can be converted into quantum ones. Quantum computers are currently very limited in their uses due to the small number of Qubits (<100 for most) they have. However, a specific kind of quantum computer called quantum annealers are already being used for certain real world applications, working in concert with classical computers. One day, quantum computers may become powerful enough to be a threat to encryption algorithms, requiring a switch to algorithms which are quantum resistant. Some quantum resistant protocols are already in use today, such as Mulvad VPN's quantum resistant VPN encryption.
### How does public-key (i.e., asymmetric) cryptography enable two parties to establish a shared secret, even over an insecure (i.e., unencrypted) channel?

Public key encryption allows two parties to establish a shared secret over an insecure channel because each party can use the public key of the other party to encrypt a secret, which can then be sent and only decrypted by the receiving party using their own private key. If each party sends a value, then combines it's own value with the value from the other party, they can securely establish a shared secret.
### What is a salt, in the context of this lecture?

A salt is a value which is added to another value before the latter is hashed so that hashes resulting from the same value (minus the salt) aren't identical. Commonly, passwords are hashed for secure storage, and if the hash isn't salted, (typically using the username or id) users with the same password will have the same hash. In the case of a data breach, unsalted hashes can be processed to find the hashes corresponding to the most common passwords, and those passwords can be found using a dictionary attack or another attack method.
### Suppose that Alice and Bob need to coordinate a meeting, as by exchanging emails using Microsoft Outlook, a popular client for email.

### If their emails are encrypted in-transit, who (besides Alice and Bob) might nonetheless be able to read the emails, and why?

Encryption in transit means that the messages are encrypted when being sent from Alice to Bob. Specifically, they are encrypted as they are sent between an Outlook email server Alice is connected to and one Bob is connected to. The messages are not encrypted when Bob sends the content of the email to the email server, so Microsoft can read it. Only end to end encryption, where the message leaves Bob's computer already encrypted and gets decrypted by Alice, ensures that no-one other than Alice and Bob can read it.
### Suppose that you have been hired to perform some work for Charlie. After agreeing to terms, you send the contract to Charlie via email, and, later that day, you receive a digitally signed copy from an email address that appears to belong to Charlie but isn't the one to which you sent the contract originally.

### How can you be certain (as certain as possible, anyway) that Charlie was the one who digitally signed the contract?

To verify the authenticity and integrity of a digital signature, you use Charlie's public key to decrypt the signature. The result should be a hash of the message. If you hash the message yourself and the hashes are the same, it means the message is unchanged and was sent by someone with access to Charlie's private key (hopefully Charlie).
### MD5 is an example of a still popular hashing algorithm that has been in use since the early 1990s. Read this article about MD5 before continuing on.

### Note that MD5 is a 128-bit algorithm, meaning its digests (i.e. hash values) are always 128 bits in length, and therefore there are 2^128 unique digests available. Thus, understand that the article's critique that there is a "high potential for collisions," while not invalid or indeed even incorrect, is perhaps something that should be understood with a bit of context.

### Suppose that a company has made a large file available for download via its website. Why might they also make available the MD5 hash of that file (as is indeed a common practice)?

You can hash the file yourself using MD5 and if the MD5 hash you get is the same as the one from a trusted source, you can conclude that the file hasn't been altered.
### What's the difference between a code and a cipher?

Codes generally substitute values on a semantic level, like words or phrases, while ciphers make substitutions character by character. Codes are used to communicate information more compactly, and are encoded and decoded with codebooks. Ciphers are used to communicate information securely, and use algorithms to encode and decode.
### Otkz D zvmizy v amzz kjdio! di ocz wjs wzgjr.
### No, the above isn't random typing! :)

i earned a free point
