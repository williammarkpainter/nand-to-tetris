@16900      // Start number 0
D=A
@3000
M=D
@17605      // Start number 1
D=A
@3001
M=D
@17606      // Start number 2
D=A
@3002
M=D
@16903      // Start number 3
D=A
@3003
M=D
@16905      // Start number 4
D=A
@3004
M=D
@16908      // Start number 5
D=A
@3005
M=D
@17389      // Start number 6
D=A
@3006
M=D
@17134      // Start number 7
D=A
@3007
M=D
@17966      // Start number 8
D=A
@3008
M=D
@16911      // Start number 9
D=A
@3009
M=D
@18159      // Start number 10
D=A
@3010
M=D
@16913      // Start number 11
D=A
@3011
M=D
@16914      // Start number 12
D=A
@3012
M=D
@17554      // Start number 13
D=A
@3013
M=D
@16915      // Start number 14
D=A
@3014
M=D
@16917      // Start number 15
D=A
@3015
M=D
@17302      // Start number 16
D=A
@3016
M=D
@17687      // Start number 17
D=A
@3017
M=D
@17304      // Start number 18
D=A
@3018
M=D
@16921      // End number 19
D=A
@3019
M=D
@18436      // End number 0
D=A
@4000
M=D
@17733      // End number 1
D=A
@4001
M=D
@17734      // End number 2
D=A
@4002
M=D
@18439      // End number 3
D=A
@4003
M=D
@18441      // End number 4
D=A
@4004
M=D
@18444      // End number 5
D=A
@4005
M=D
@17997      // End number 6
D=A
@4006
M=D
@17422      // End number 7
D=A
@4007
M=D
@18222      // End number 8
D=A
@4008
M=D
@17188      // End number 9
D=A
@4009
M=D
@18447      // End number 10
D=A
@4010
M=D
@18449      // End number 11
D=A
@4011
M=D
@17138      // End number 12
D=A
@4012
M=D
@17682      // End number 13
D=A
@4013
M=D
@18451      // End number 14
D=A
@4014
M=D
@17333      // End number 15
D=A
@4015
M=D
@17718      // End number 16
D=A
@4016
M=D
@18455      // End number 17
D=A
@4017
M=D
@17720      // End number 18
D=A
@4018
M=D
@17337      // End number 19
D=A
@4019
M=D
@2          // # MAIN CODE START # Address 2 keeps track of the -1 or 0 writing
M=-1        // Set address 2 to -1 to start with writing black on sreccn, Main loop start 
@3          // # INTINIATE LOOP START # Address 3 keeps track of the run number (LB_Main_Start)
M=0         // Which is intially set to 0
@20         // Address 4 holds the max number of character components, which is currentl 20
D=A
@4
M=D
@3          // ## START of component loop [LB_comp_start], set address 0 =  3000 + value in address 3,
D=M
@3000
A=D+A
D=M
@0
M=D         // Value in RAM[0] is not set to RAM[3000+RAM[3]], this is the start memeor address for the character component
@3          // Value in RAM[1] =  4000 + value in address 3
D=M
@4000
A=D+A
D=M
@1
M=D         // Value in RAM[1] is not set to RAM[4000+RAM[3]], this is the start memeor address for the character component
@2          // ##START WRITE LOOP## [LB_startwrite], this is the loop entry point for writing each charater
D=M         // D now how the write value from RAM[2], this is either -1 or 0 
@0          // Set the Address register to the memory location pointed to in address 0 
A=M
M=D         // Set the value of the memory location to the value in D which is from RAM[2] and is either 0 or 1
@32         // Increment RAM[0] by 32 and set that new value in  D as well
D=A
@0      
MD=M+D  
@1          // If the value in RAM[1] is still greater than the value in RAM[0] then loop back to LB_startwrite to continue writing the next line
D=M-D
@182        // Set jump address to LB_startwrite
D;JGT       // The Jump instruction
@3          // Once the charcater component has been compleated, we need to increament the run component counter in RAM[3] to take us to the next 
MD=M+1      // Get the Value in RAM[3] into the the data regisrty and check is less than RAM[4] (which is the maximum component count.
@4
D=M-D
@168        // jump address to LB_comp_start to write the next component 
D;JGT
@5          // Once all character components have been written, run through a delay loop of 24,000 * 20
M=0         // The delay outer loop counter is held in RAM[5]
@5          // The outer loop starts here LB_Delay_loop_start
M=M+1       // Increment RAM[5], the outerloop counter here
@6          // There is an inner delay loop of 20 
M=0         // The innter delay loop counter is held in RAM[6]
@6          // This is the start of the inner loop (LB_Inner_CounterLoop) to further control the speed of the flashing
D=1         // pointless process
MD=M+1      // Increment and set RAM[6] and Data Register
@20         // set the Addresss resigister to 20
D=A-D       
@207        // set jump address for Inner Loop
D; JGT      // Jump to LB_Inner_CounterLoop if RAM[6] < 20
@5          // Once innner loop is compleated, need to check outer loop, which was incremented in line 205
D=M     
@24000      // Check if outerloop is greater, than 24_000
D=D-A
@203        // set jump address to LB_Delay_loop_start instruction
D;JLT       // jump if counter - 24000 is less than 0
@2          // once the delay loop has been compleated, flip the writing colour in RAM[2] from -1 to 0, or 0 to -1
M=!M
@162        // Set jump address to LB_Main_Start
0;JMP       // Unconditional jump for infinate loop


