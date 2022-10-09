@16900  // Start number 0
D=A
@3000
M=D
@17605  // Start number 1
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
@2      // Address 2 keeps track of the -1 or 0 writing
M=-1    // Set address 2 to -1 to start with writing black on sreccn, Main loop start LB_Main_Start
@3      // Address 3 keeps track of the run number
M=0
@20     // Address 4 holds the max number
D=A
@4
M=D
@3      // ## START of component loop [LB_comp_start], set address 0 =  3000 + value in address 3
D=M
@3000
A=D+A
D=M
@0
M=D
@3   // set address 1 =  4000 + value in address 3
D=M
@4000
A=D+A
D=M
@1
M=D
@2      // ##START WRITE LOOP## [LB_startwrite]
D=M
@0      // set the memory location pointed to in address 0 to the value in address 2
A=M
M=D
@32     // Increment Address 0 by 32 set into D as well for check if still less than
D=A
@0      
MD=M+D  
@1
D=M-D
@182     // Set jump address to LB_startwrite
D;JGT
@3      // Increament run component counter Address 3
MD=M+1  // Get the Value in Address 3 into the the data regisrty and check is less than address 4
@4
D=M-D
@168     // jump address to LB_comp_start
D;JGT
@5      // set delay for 5000  jumps, using Address 5 as counter
M=0     
@5      // LB_Delay_loop_start
M=M+1     
@6
M=0     
@6      // LB_Inner_CounterLoop to further control the speed of the flashing
D=1     // pointless process
MD=M+1
@20
D=A-D   
@207
D; JGT
@5      // outside innerloop
D=M     
@24000
D=D-A
@203    // set jump address to LB_Delay_loop_start instruction
D;JLT   // jump if counter - 5000 is less than 0
@2      // Flip the writing colour in Address 2
M=!M
@161    // jump to LB_Main_Start
0;JMP


