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

Whether because of the decompilation process or the nature of C code (and my limited knowledge of the language), many of the functions are difficult to understand.

```C
LPVOID FUN_00406f3a(SIZE_T param_1,undefined *param_2)
{
  LPVOID pvVar1;
  
  pvVar1 = HeapAlloc(DAT_0040ad88,8,param_1);
  if (param_2 != (undefined *)0x0) {
    (*(code *)param_2)(pvVar1);
  }
  return pvVar1;
}
```

For example, this function returns a void pointer containing the memory address of allocated memory in the heap. It casts the function pointer param_2 to the code type if it isn't a null pointer, then executes the function it points to with the pointer to the heap as a parameter.

The C compiler makes optimization which make for strange C code when decompiled. For instance, an allocation on the stack may be used multiple times for different purposes, which gets decompiled to a local variable which is assigned and read multiple times for entirely unrelated purposes, which is not very readable code. In entry, as shown below, the variable iVar1 is assigned and read multiple times for totally unrelated purposes.

![[Pasted image 20231212203320.png]]

I've been moving recursively through functions in the entry function and functions inside those functions, and trying to puzzle out what they're doing and especially what global variables are used for. For instance, I found one global variable which is repeatedly used in memory related functions and I determined that it's a pointer to an allocated section on the heap. These memory management functions and variables probably aren't useful to me, but it's hard to tell at a glance.



One of the rabbit holes I went down is figuring out what the `heap_pointer` variable is being used for in `entry`.  The first if statement in the main loop is:

```C
    if (((main_loop_value == 0x332c) && (iVar1 = get_first_in_list(), iVar1 == 1)) &&
        (iVar1 = FUN_00405c02(), iVar1 == 0x300)) {
```

In which there are 3 checks which must pass to go on to the other if statements, otherwise it just loops again. `main_loop_value` seems to check for a specific value from the application window data, and the last check does the same for a function which I haven't analyzed yet. The one which I went deep into was the second condition, which needs to be equal to 1. (function names have been changed to reflect my understanding of them). The function `get_first_in_list` uses the global variable `heap_pointer`, which stores the address of an allocated section on the heap, containing a data structure. I think it's a list or an array. `return_value_unchanged` just returns the parameter it's given. I'm not sure why it's used. Maybe something to do with how global variables work. Then pointer arithmetic is used to ad 0x18 to the address, and the resulting address is dereferenced to get the value there.

```C
undefined4 get_first_in_list(void)

{
  int iVar1;
  
  iVar1 = return_value_unchanged(heap_pointer);
  return *(undefined4 *)(iVar1 + 0x18);
}
```

In order to figure out what `heap_pointer` was I looked at the 8 places in the app where it's referrenced. These were all in different functions, which had code related to the heap, memory management, or data structures. I'm still not sure what the list is actually used for, but it's probably important.

Schizo Ramblings

WHAT does CONCAT44 do?

One of the most important functions is probably is_correct_lotto, which determines if the program displays "those are not the winning numbers" or proceeds. However, this function has a number of elements which make no sense.

```C
undefined8 is_correct_lotto(undefined4 *String) {
  undefined4 extraout_ECX;
  undefined4 extraout_EDX;
  undefined8 int_1;
  ushort *pointer_to_string_on_heap;
  int int_2;

  int_2 = 0;
  pointer_to_string_on_heap = (ushort *)0x0;
  allocate_heap_and_copy_string_proxy(&pointer_to_string_on_heap,String);
  int_1 = string_to_int(pointer_to_string_on_heap);
  int_2 = (int)int_1;
  rearrange_bytes_in_int(int_2);
  int_1 = FUN_004076a0(extraout_ECX,extraout_EDX,pointer_to_string_on_heap);
  return int_1;
}
```

This function takes a pointer to the string which is taken from the text input box in the app. It makes a copy of the string on the heap, and uses that copy to find the value of the string as a number. It makes a copy of the number in int_2. This is one of the things that doesn't make sense. int_2 gets passed to a function which rearranges the bytes in it, but the return value isn't used. What's the point.

The second thing is that extraout_ECX and EDX are passed to FUN_00407a0 without being initialized, and furthermore, they aren't even used in the function they're passed to.

```C
undefined8 __fastcall FUN_004076a0(undefined4 param_1,undefined4 param_2,LPVOID param_3)
{
  undefined4 in_EAX;
  if (param_3 != (LPVOID)0x0) {
    HeapFree(heap_1,0,param_3);
  }
  return CONCAT44(param_2,in_EAX);
}
```

I learned how extraout variables work. They represent values in registers being passed to a function with the fast-call convention. This is probably the result of a compiler optimization, because god forbid anyone write C like this. I'm not sure why it didn't just inline the function though...

CONCAT44 is a Ghidra macro, which represents the operation of concatenating two 32 bit values, in this case, the EDX and EAX registers, to make a 64 bit value. (The 8 in undefined8 is 8 bytes, which is also called a quad word (a word is 16 bits)). The EAX register has the value of int_2 which had it's bytes rearranged since it was placed on EAX earlier. The other value is param_2 which is EDX

Ugh I don't know which values are actually on those registers because multiple functions in is_lotto_correct use them

I wasn't able to understand what is_correct_lotto was doing. It returns a value which seems to be 0 if the lotto number entered is wrong and something other than 0 if the number is correct. But it's behavior doesn't line up with that. It seems to just convert to int, shuffle some bits, and then append something else to it. Turns out, there's a conditional jump in the assembly for is_correct_lotto!! Apparently sometimes the decompiler just doesn't work correctly and skips over stuff like this. I realize that writing a decompiler is very hard but this is awful. I've been trying to avoid having to read the assembly because I'm not very good at it but I'm coming to the realization that it's mandatory for this.

![[Pasted image 20231215065752.png]]

The highlighted `JNZ` (jump if not zero) instruction isn't represented in the control flow of the function in C. 

Code breakdown.
`MOV EBX, int_1` copies the value from int_1 onto the general purpose `EBX` register. `CMP` compares the value of `int_1` in the `EBX` register and `DAT_0040ad90`, one of the global variables. If they're the same, the Zero Flag (ZF) is set to 1, othersize it's set to 0. Then `JNZ` checks the flag and jumps to LAB_00402037 if it's 1. The result is that the function has an if/else functionality with two branches. They simply set int_1 to 0 or to 1. This is the value that I think ends up getting returned, and represents whether the lotto number was correct or not.

![[Pasted image 20231215072758.png]]


I'm still figuring out what the function in the last segment is doing. It's the one which uses fastcall to use the registers directly.

### I figured everything out. Here's the line-by-line

PUSH      EBX      
_saves a value from the calling function for later_

XOR       EAX,EAX    
_sets EAX to 0_

PUSH      EAX    
_adds a 0 to the stack to use as a parameter_

PUSH      EAX    
_adds another one_

MOV       EDX,dword ptr [ESP + String]    
_copies the pointer to the input string to EDX_

LEA       ECX=>pointer_to_string_on_heap,[ESP]    
_copies the adress at the top of the stack to EXC, essentially making a pointer to the second 0_

CALL      allocate_heap_and_copy_string_proxy    
_copies the string to the heap and uses the pointer in EXC to make the element on the stack a pointer to it_

PUSH      dword ptr [ESP]=>pointer_to_string_on_heap    
_makes a copy of the string-on-heap pointer on the stack to use as a parameter_

CALL      string_to_int    
_turns it into an int, which goes on EDX and EAX because ints are 64 bits and registers are 32_

MOV       dword ptr [ESP + int_2], int_1    
_copies the int stored in EDX and EAX (which are collectively int_1) onto the other 0 on the stack_

PUSH      dword ptr [ESP + int_2]    
_makes a copy of int_2 on the stack_

CALL      rearrange_bytes_in_int    
_swaps the positions of the 2nd and 4th bytes in the provided 32 bit int, such that a,b,c,d becomes d,a,c,b. This value is returned onto EAX_

MOV       EBX,int_1
_copies EAX onto EBX_

CMP       EBX,dword ptr [DAT_winning_lotto]
_checks if ebx is equal to the global value DAT_winning_lotto, which is set in entry(). If it is, the Zero Flag (ZF) is set to 1, otherwise 0

JNZ       LAB_00402037
_jumps if ZF is not 0_

MOV       int_1,0x1


JMP       LAB_0040203d


LAB_00402037
XOR       int_1,int_1


JMP       LAB_0040203d



LAB_0040203d
PUSH      dword ptr [ESP]=>pointer_to_string_on_heap


CALL      concat_edx_and_eax_and_free_heap


ADD       ESP,0x8


POP       EBX


RET       0x4





Oh my god why didn't I read the friggin assembly this makes so much more sense.

Also shoutout to ChatGPT, this would have been impossible without it's insights. It's remarkably able to break down what assembly code or unreadable C code is doing, and while it's insights often lack depth, being able to throw tens of functions at it and get a quick analysis of what they probably do helped me to narrow down which functions I needed to pay special attention to, as well as figure out what's generally going on in this app. I think the future of human programmers assisted by AI is bright. Although perhaps one day it will get too good and replace us. One can only wonder what a society would do with unlimited programmers though. Every man could be a game developer. I would be out of a job, but society would surely be very different. Good thing I know how to do some construction.

![[Pasted image 20231215155935.png]]

Dynamic analysis in IDA.

I entered 1. The number 1 is correctly placed onto EAX by string_to_int. Then it gets rearranged and becomes: ![[Pasted image 20231215162050.png]]


```C
#include <stdio.h>
#include <stdint.h>

uint32_t rearrange_bytes(uint32_t param_1) {
    return (uint32_t)(uint8_t)param_1 << 16 | //d -> b
           (param_1 >> 24) << 8 | //a -> c
           (param_1 << 8) >> 24 | //b -> d
           ((param_1 << 16) >> 24) << 24; //c -> a
} //a,b,c,d -> c,d,a,b


int main() {
    uint32_t target = 0x7a6a;
    uint32_t found = 0;
    uint32_t test;

    for (test = 0; test <= 0xFFFFFFFF; test++) {
        if (rearrange_bytes(test) == target) {
            found = test;
            break;
        }
    }

    if (found != 0) {
        printf("Found matching integer: 0x%08X (decimal: %u)\n", found, found);
    } else {
        printf("No matching integer found.\n");
    }

    return 0;
}
```

HOLY SHIT

![[Pasted image 20231215162911.png]]

![](Pasted%20image%2020231215163635.png)

