  .syntax unified

  .text

  .global memset_reg
  .type memset_reg, STT_FUNC
memset_reg:
  // call with the following (note that the arguments are not validated prior to use):
  // r0 - address of first word to write (inclusive)
  // r1 - address of first word following the address in r0 to NOT write (exclusive)
  // r2 - word value to be written
  // both addresses in r0 and r1 needs to be divisible by 4!
  .L_loop_begin:
    str r2, [r0], 4 // store the word in r2 to the address in r0, post-indexed
    cmp r0, r1
  bne .L_loop_begin
  bx lr

  .global reset_handler
  .type reset_handler, STT_FUNC
reset_handler:
  bl SystemInit

  // read the first rng data and save it
  ldr r0, =0            // r0 - previous value
  ldr r1, =0            // r1 - whether to compare the previous value
  bl rng_read

  // read the next rng data and make sure it is different than previous
  // r0 - value returned from previous call
  ldr r1, =1            // r1 - whether to compare the previous value
  bl rng_read
  mov r4, r0            // save TRNG output in r4

  // wipe memory to remove any possible vestiges of sensitive data
  // use unpredictable value as a defense against side-channels
  ldr r0, =ccmram_start // r0 - point to beginning of CCMRAM
  ldr r1, =ccmram_end   // r1 - point to byte after the end of CCMRAM
  mov r2, r4            // r2 - the word-sized value to be written
  bl memset_reg

  ldr r0, =sram_start   // r0 - point to beginning of SRAM
  ldr r1, =sram_end     // r1 - point to byte after the end of SRAM
  mov r2, r4            // r2 - the word-sized value to be written
  bl memset_reg

  // setup environment for subsequent stage of code
  ldr r0, =ccmram_start // r0 - point to beginning of CCMRAM
  ldr r1, =ccmram_end   // r1 - point to byte after the end of CCMRAM
  ldr r2, =0            // r2 - the word-sized value to be written
  bl memset_reg

  ldr r0, =sram_start   // r0 - point to beginning of SRAM
  ldr r1, =sram_end     // r1 - point to byte after the end of SRAM
  ldr r2, =0            // r2 - the word-sized value to be written
  bl memset_reg

  // copy data in from flash
  ldr r0, =data_vma     // dst addr
  ldr r1, =data_lma     // src addr
  ldr r2, =data_size    // size in bytes
  bl memcpy

  // enter the application code
  bl main

  // loop forever if the application code returns
  b .

  .end
