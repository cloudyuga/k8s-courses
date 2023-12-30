#include <stdio.h>
#include <sys/utsname.h>
#include <seccomp.h>

void main() {
    puts("Calling uname before setting up seccomp");
    struct utsname unameData;
    uname(&unameData);
    printf("%s \n", unameData.sysname);

    puts("Calling uname after setting up seccomp");
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_ALLOW);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(uname), 0);
    seccomp_load(ctx);

    uname(&unameData);
    printf("%s \n", unameData.sysname);
}
