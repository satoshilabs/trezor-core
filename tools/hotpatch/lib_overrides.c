#include <dlfcn.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

static int PAGE_SIZE;

#define FUN_SIZE(fun) (fun##_end-fun)
#define PTR_PAGE_ALIGN(ptr) \
  (void*)((unsigned long long)ptr & (unsigned long long)(~(PAGE_SIZE-1)))

void override_void_void(void) {};
void override_void_void_end(void) {};

static void override_constructor() __attribute__((constructor));
void override_constructor() {
  printf("### binary_override_start\n");

  PAGE_SIZE = getpagesize();

  // override storage_wipe with empty function

    // get storage_wipe memory location
  void* sym_ptr = dlsym(RTLD_DEFAULT, "storage_wipe");
  void* page_ptr = PTR_PAGE_ALIGN(sym_ptr);
  long fun_size = FUN_SIZE(override_void_void);

  printf("### storage_wipe <<< void(void) @ %p ! %p : %ld\n", sym_ptr, page_ptr, fun_size);

    // unprotect memory page
  if (mprotect(page_ptr, PAGE_SIZE, PROT_READ|PROT_WRITE|PROT_EXEC) != 0) {
    perror("error");
  }
    // override function bytes
  bcopy(override_void_void, sym_ptr, FUN_SIZE(override_void_void));
}

