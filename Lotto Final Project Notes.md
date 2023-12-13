The application I'm trying to reverse engineer is lotto.exe. This application opens a window which asks you to enter a lottery ticket. The goal is to enter the winning ticket. This challenge is quite hard. The lotto.exe file is a very large x86 assembly file with considerable complexity. My former teacher said that it took them the better part of a week. So, I think this is a reasonable conclusion to the hacking I've been doing this quarter.
### Setup

I first installed a C toolchain with MinGW so that I could play around with C compilation. This will help me reason about the relationship between C and assembly. I got a little confused by the proliferation of different toolchains for C compilation on Windows, but I followed the recommendation of the C/C++ extension for VSCode and used MinGW. I continue to be baffled that many applications on Windows require you to add them to the PATH manually.

I also updated my installation of Ghidra. The NSA made some significant improvements to the UI since I last updated, including adding support for color schemes. My eyes are very grateful. Ghidra dark mode actually looks nice. Although the ridiculous gradient at the top is still there, and the icons still look like they're from the stone age.
### Chapter 1: Getting Started

When I ran lotto.exe, it opened a window and waited for me to enter a value.

![[Pasted image 20231209172453.png]]

When I entered a value, it said "you cannot buy a lotto ticket without money"

![[lotto1.png]]

I didn't how I was supposed to get money. I tried entering a command line argument when launching the application, but it didn't do anything. It was time to look at the file.

The bulk of this challenge was looking through the application in Ghidra and puzzling it out. I needed to figure out what value to enter in order to get the flag, based on its' inner workings.

I imported the file into Ghidra and got a description of the app. The only noteworthy info was that the compiler is visualsutdio:unknown, which indicates that the app was compiled with Microsoft Visual Studio. Visual Studio is used to compile C and C++ code for Windows. It's actually not trivial to identify whether the source code is from C or C++. There can be artifacts from C++ objects, and other hints like name mangling. I think lotto was written in C, but I'm not certain.

I opened lotto.exe in the code viewer, and analyzed the code, which decompiled it into C. This is what it looks like in Ghidra;

![[Pasted image 20231209180110.png]]

Data and instructions are on the left, and code is on the right. Selecting elements on either side will highlight the corresponding element (if there is one) on the other side.

I found it hard to read the text, so I changed the font, colors, and font size. While Ghidra's menus are often unintuitive, the customization options are surprisingly in-depth.

![[Pasted image 20231209184155.png]]

Lotto.exe is pretty big. It spans 37,544 memory addresses, but luckily most of them aren't relevant to solving the challenge. The majority of the file is comprised of functions. There are some "Thunk functions" which are used as proxies or helpers for other functions. Most of the functions are not thunk functions, and they have anywhere from a few lines of decompiled C to hundreds of lines. Most of the variable names and all of the comments from the source code are lost in compilation, so there isn't much to work with to figure out what functions do. I had to look at what the code is doing and work backwards to determine what the program is doing as a whole. Hence "reverse" engineering.

The first function in the file is `entry`, which is the top level function of the application. All of the other functions are unnamed and Ghidra gives them names like FUN_0040204c. I used the symbol tree to confirm that there are in fact, a *lot* of functions.

![[toomanyfunctions.png]]

I took a cursory look at many of the functions and determined that most seem to fall into three categories:

- Program logic
- GUI and IO
- Memory management

I was concerned with the logic of the program and not the other elements, so part of the task of reverse engineering was identifying which functions I did or didn't need to care about. A good way of going about this is top-down analysis. By starting at the entry function which governs the overall functionality of the application and recursively analyzing the functions called in it, I could puzzle out the application.

Breaking down the entry function shows 3 main parts. Setup, a main loop, and cleanup. Here's the setup part with comments added explaining what I think each part is doing:

```C
void entry(void)

{
  int iVar1;
  undefined8 uVar2;
  int iVar3;
  int iVar4;
  UINT uExitCode;
  
  memset(&DAT_0040ad88,0,0x20); //Memory stuff
  DAT_0040ad8c = GetModuleHandleW((LPCWSTR)0x0);
  DAT_0040ad88 = HeapCreate(0,0x1000,0);
  
  FUN_004075a0(); //I have no idea what these do
  ... //more unnamed functions with no parameters, which I excerpted for brevity
  DAT_0040ada0 = 0;
  DAT_0040ad90 = 0x7a6a;
  FUN_00403008((LPVOID *)&DAT_0040ada4,(undefined4 *)&DAT_0040a0f2);
  _OOBECompleteWnfQueryCallback@28((HWND__)0x0,0,0,0x142,0x56,u_Lotto!_0040a0e4,0xc80001);
  //Given that the above line contains the text that appears in window, this probably creates the window
  FUN_0040363f((HWND)0x1,8,10,0x132,0x14,(LPCWSTR)&DAT_0040a020,0x2000);
  FUN_004039bb((HWND)0x3,8,0x23,0xce,0x28,u_Enter_a_lotto_number!_0040a0b8);
  //And this line sets the initial state of the text box which asks you to enter a number
```

Here's the main loop:

```C
  do {
    DAT_0040ad9c = FUN_004042fc();
    if (((DAT_0040ad9c == 0x332c) && (iVar1 = FUN_00405bf3(), iVar1 == 1)) &&
        (iVar1 = FUN_00405c02(), iVar1 == 0x300)) { //I don't know what this does, but it involves DAT_0040ad9c which is what determines whether the loop continues
      if (DAT_0040ada0 == 0) { //This checks if I have no money, and denies me from entering a lottery ticket
         FUN_004039db((int *)0x3,u_You_cannot_buy_a_lotto_ticket_wi_0040a060);
      }
      else {
         iVar1 = DAT_0040afcc;
         FUN_00403a26((int *)0x1,DAT_0040afcc);
         FUN_00407620(&DAT_0040ad98,iVar1);
         uVar2 = FUN_00402000(DAT_0040ad98);
         if ((int)uVar2 == 0) { //This function checks if the lotto number is correct or not
           FUN_004039db((int *)0x3,u_Those_are_not_winning_numbers._0040a022); //And this one sets the text to display "Those are not the winning numbers"
         }
         else { //This stuff happens if the lotto number is correct. It displays the flag, which is encoded so I can't just read it from the file
           iVar1 = DAT_0040afcc;
           iVar3 = DAT_0040afcc;
           iVar4 = DAT_0040afcc;
           uVar2 = FUN_00403040((ushort *)DAT_0040ad98);
           uVar2 = FUN_004021df((int)uVar2);
           FUN_00405710((short *)uVar2,iVar1);
           DAT_0040afcc = DAT_0040afcc + 2;
           FUN_004039db((int *)0x3,(LPCWSTR)(iVar3 + DAT_0040a140));
           DAT_0040afcc = iVar4;
         }
      }
    }
  } while (DAT_0040ad9c != 0x333c); //This variable is set at the start of the loop to the output of FUN_004042fc(), then checked in the following if statement
```

An important tool in reverse engineering is to give variables descriptive psudonyms. As I worked, I changed the names of variables to reflect my understanding of them. For instance, I renamed `DAT_0040ad9c` to `main_loop_value` because it detemines if the program keeps looping. I also renamed `FUN_004039db` to `display_text` since it decides which text shows in the app.

Here's after the loop:

```C
  uExitCode = 0; //Means the proccess exits successfully
  FUN_00401220();
  FUN_004075f0();
  HeapDestroy(DAT_0040ad88);
                      /* WARNING: Subroutine does not return */
  ExitProcess(uExitCode);
```

I went into each function and renamed many of them based on what I thought they did. Here's the current state of `entry`:

```C
...
  memset(&DAT_0040ad88,0,0x20);
  DAT_0040ad8c = GetModuleHandleW((LPCWSTR)0x0);
  DAT_0040ad88 = HeapCreate(0,0x1000,0);
  heap_stuff();
  entry_data_structure_stuff_1();
  create_window();
  tls_alloc_proxy();
  make_heap_2();
  heap_stuff?();
  ???();
  windows_stuff();
  load_assets();
  more_initialization();
  money_amount = 0;
  DAT_0040ad90 = 0x7a6a;
  FUN_00403008((LPVOID *)&DAT_0040ada4,(undefined4 *)&DAT_0040a0f2);
  _OOBECompleteWnfQueryCallback@28((HWND__)0x0,0,0,0x142,0x56,u_Lotto!_0040a0e4,0xc80001);
  FUN_0040363f((HWND)0x1,8,10,0x132,0x14,(LPCWSTR)&DAT_0040a020,0x2000);
  FUN_004039bb((HWND)0x3,8,0x23,0xce,0x28,u_Enter_a_lotto_number!_0040a0b8);
  do {
    main_loop_value = get_window_info_proxy();
    if (((main_loop_value == 0x332c) && (iVar1 = FUN_00405bf3(), iVar1 == 1)) &&
        (iVar1 = FUN_00405c02(), iVar1 == 0x300)) {
      if (money_amount == 0) {
         display_text((int *)0x3,u_You_cannot_buy_a_lotto_ticket_wi_0040a060);
      }
      else {
         iVar1 = int_1;
         FUN_00403a26((int *)0x1,int_1);
         FUN_00407620(&DAT_0040ad98,iVar1);
         uVar2 = FUN_00402000(DAT_0040ad98);
         if ((int)uVar2 == 0) {
           display_text((int *)0x3,u_Those_are_not_winning_numbers._0040a022);
         }
         else {
           iVar1 = int_1;
           iVar3 = int_1;
           iVar4 = int_1;
           uVar2 = FUN_00403040((ushort *)DAT_0040ad98);
           uVar2 = FUN_004021df((int)uVar2);
           FUN_00405710((short *)uVar2,iVar1);
           int_1 = int_1 + 2;
           display_text((int *)0x3,(LPCWSTR)(iVar3 + allocated_heap_1));
           int_1 = iVar4;
         }
      }
    }
  } while (main_loop_value != 0x333c);
  uExitCode = 0;
  FUN_00401220();
  FUN_004075f0();
  HeapDestroy(DAT_0040ad88);
                      /* WARNING: Subroutine does not return */
  ExitProcess(uExitCode);
}
```

I figured out why I was getting the message "You cannot buy a lotto ticket with no money". The money_amount variable is set to 0, then checked if it's equal to 0. These are the only two places where the variable is referrenced, so it's impossible to satisfy this requirement.

Luckily, Ghidra allows me to patch the instructions, so I was able to remove the requirement. 

![[Pasted image 20231210194230.png]]

As shown above, I can modify the assembly where the value is set to 0 to set it to whatever I want. I get this strange message upon clicking "Patch instruction" though. 

![[Pasted image 20231210194353.png]]

I exported and ran the patched exe and when I enter a number, I get a different message than before. The patch worked!

![[Pasted image 20231210195228.png]]

Having seen that I can patch the app, I decided I should try patching it to give me the flag. I expected it not to work. It would be too easy if this were the whole challenge.

The if statement which checks for the correct value uses the instruction JZ which means "Jump if Zero". I changed JZ to JNZ which jumps if not zero. This inverts the if statement, so it should give me the flag if I get the lotto number wrong. 

The patched instructions:

![[Pasted image 20231210205336.png]]
And the new decompiled code, which has the if statement inverted:

![[Pasted image 20231210203851.png]]

But did it work?

Nope. Of course it's not that easy. Entering a number in the modified lotto.exe gives me gibberish. When I entered a second number, it crashed.

![[Pasted image 20231210201511.png]]

As I suspected, the process which outputs the flag uses the input in some way. Which means that the input must be correct in order for the flag to be revealed.

### Chapter 2: The Hard Part

