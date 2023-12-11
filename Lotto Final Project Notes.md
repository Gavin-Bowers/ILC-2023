The application I'm trying to reverse engineer is lotto.exe. This application opens a window which asks you to enter a lottery ticket. The goal is to enter the winning ticket. This challenge is quite hard. The lotto.exe file is a very large x86 assembly file with considerable complexity. My former teacher said that it took them the better part of a week. So, I think this is a reasonable conclusion to the hacking I've been doing this quarter.

### Setup

I first installed a C toolchain with MinGW so that I could play around with C compilation. This will help me reason about the relationship between C and assembly.

![[Pasted image 20231209153440.png]]

I got a little confused by the proliferation of different toolchains for C compilation on Windows, but I followed the recommendation of the C/C++ extension for VSCode and used MinGW. I continue to be baffled that many applications on Windows require you to add them to the PATH manually.

I also updated my installation of Ghidra. The NSA made some significant improvements to the UI since I last updated, including adding support for dark mode. My eyes are much relieved.

Ghidra dark mode actually looks kind of nice. Although the gradient at the top is still goofy. Although, I find that the text anti-aliasing / subpixel rendering could be better.

![[Pasted image 20231209173512.png]]

### Chapter 1: The Beginning

When you run lotto.exe, it opens a window and waits for you to enter a value. It responds instantly, so if you want to enter more than one number, you have to copy and paste.

![[Pasted image 20231209172453.png]]

When you enter a value, it says "you cannot buy a lotto ticket without money"

![[lotto1.png]]

Now, I don't see any way of getting money in this window, so this is a roadblock. I tried entering a command line argument when launching the application, but it didn't do anything.

The bulk of this challenge will be looking through this application in Ghidra and puzzling it out. I need to figure out what value to enter in order to get the flag, based on its' inner workings.

I imported the file into Ghidra and got this summary:

![[Pasted image 20231209175106.png]]

The compiler being `visualsutdio:unknown` indicates that this program was compiled with Microsoft Visual Studio, which is used to compile C and C++ code for Windows with LLVM.

I then opened lotto.exe in the code viewer, and analyzed the code, which decompiled it into C.

![[Pasted image 20231209175929.png]]

And this is what it looks like. Data and instructions are on the left, and code is on the right. Selecting elements on either side will highlight the corresponding element (if there is one) on the other side.

![[Pasted image 20231209180110.png]]

There were 37,544 addresses in this file. Most of these addresses were not relevant to solving the problem (otherwise I would never finish). At the top is the header, which contains information about the file that the operating system uses. Below the header there are a number of null bytes. 

The first function in the file is `entry`, which seemed like a main function. Many of the functions are unnamed and Ghidra gives them names like FUN_0040204c.

I'm finding it hard to read the text, so I changed the font, colors, and font size. While Ghidra's menus are often unintuitive, the customization options are surprisingly in-depth.

![[Pasted image 20231209184155.png]]

### Chapter 2: Analyzing the Code

Lotto.exe is very large. The majority of the file is comprised of functions. There are some "Thunk functions" which are used as proxies or helpers for other functions. Most of the functions are not thunk functions, and they have anywhere from a few lines of decompiled C to hundreds of lines. Most of the variable names and all of the comments from the source code are lost in compilation, so there wasn't much to work with to figure out what functions do. I needed to look at what the code is doing and work backwards to determine what the program is doing as a whole. Hence "reverse" engineering.

I used the symbol tree to confirm that there are in fact, a *lot* of functions.

![[toomanyfunctions.png]]

I took a cursory look at many of the functions and determined that most seem to fall into three categories:

- Program logic
- GUI and IO
- Memory management

I was concerned with the logic of the program and not the other elements, so part of the task of reverse engineering was identifying which functions I did or didn't need to care about. A good way of going about this is top-down analysis. By starting at the entry function which governs the overall functionality of the application and recursively analyzing the functions called in it, I could puzzle out the application.

