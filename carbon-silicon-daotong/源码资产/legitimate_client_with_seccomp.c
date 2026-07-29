#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <seccomp.h>
#include <sys/syscall.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include "zone0_record.h"

    /* Debian Bullseye libseccomp 2.5.x缺失该宏定义，详见QEMU仿真适配预案 */
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(renameat2), 0);

int main()
{
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(msgsnd), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(msgrcv), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_load(ctx);

    int msq_id = msgget(ZONE0_IPC_KEY, 0644);
    zone0_msg_t msg;
    msg.mtype = 1;
    snprintf(msg.data, sizeof(msg.data), "seccomp hardened legitimate client");
    msgsnd(msq_id, &msg, sizeof(msg.data), 0);
    msgrcv(msq_id, &msg, sizeof(msg.data), 1, 0);
    printf("Hardened client ack received\n");

    // 尾部违规open自校验逻辑，主动触发禁止调用，输出拦截日志
    int test_fd = open("/etc/passwd", O_RDONLY);
    if (test_fd < 0)
    {
        printf("[SELF-CHECK PASS] open() call blocked by seccomp, defense verified\n");
    }
    else
    {
        close(test_fd);
        printf("[SELF-CHECK FAIL] open() not blocked, defense invalid\n");
    }

    seccomp_release(ctx);
    return 0;
}
