#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
#include<unistd.h>
#include<seccomp.h>
 
int main() {
    pid_t pid;
 
    /*
     * Initializing the filter of type scmp_filter_ctx and defining the action 
     * to be performed In our case it is SCMP_ACT_KILL which is going to kill 
     * all the system calls that have not been added to our seccomp rule .
     **/
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    
    /*
     * Next we have to define the seccomp rules, 
     * These system calls our process can run
     **/
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fork), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    

    printf ("After this line seccomp is activated \n");
 
    //Activate the seccomp filter mode .
    seccomp_load(ctx);
    
    fork();
    
    printf("You can able to see this line\n");
    
    pid = getpid();
    printf("you should not see this line %d\n", pid);

    return 0;
}
