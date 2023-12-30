 #include <fcntl.h>
 #include <stdio.h>
 #include <unistd.h>
 #include <string.h>
 #include <linux/seccomp.h>
 #include <sys/prctl.h> 
int main()
   {
         int fd;
          char buffer[80];
         char msg[50] = "hello world";

         fd = open("sample.txt", O_RDWR);
         printf("fd = %d\n", fd);
     
         printf("Calling prctl() to set seccomp strict mode...\n");
          prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT);
 
         printf("Writing to an already open file...\n");
        write(fd, msg, strlen(msg));
 
         lseek(fd, 0, SEEK_SET);
  
         read(fd, buffer, strlen(msg));
  
          printf("\n %s was written to my file\n", buffer);
          close(fd);
  
          printf("The process will be killed before this line\n");
 }

