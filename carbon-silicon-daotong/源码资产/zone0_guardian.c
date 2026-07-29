#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <seccomp.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include "zone0_record.h"

// seccomp规则置于main最前置，消除TOCTOU时序漏洞
int main(int argc, char **argv)
{
    scmp_filter_ctx ctx;
    // 初始化seccomp，默认拒绝所有未放行系统调用
    ctx = seccomp_init(SCMP_ACT_KILL);
    if (!ctx)
    {
        perror("seccomp init fail");
        return 1;
    }

    // 仅放行IPC消息队列交互、基础进程生命周期调用
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(msgsnd), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(msgrcv), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);

    // 加载内核约束规则，进程启动瞬间完成加固
    seccomp_load(ctx);

    // 业务逻辑：zone0隔离域守护进程主逻辑
    key_t ipc_key = ZONE0_IPC_KEY;
    int msq_id = msgget(ipc_key, IPC_CREAT | 0644);

    while (1)
    {
        zone0_msg_t msg_buf;
        msgrcv(msq_id, &msg_buf, sizeof(msg_buf.data), 1, 0);
        zone0_log_record(&msg_buf);
        msgsnd(msq_id, &msg_buf, sizeof(msg_buf.data), 0);
    }

    seccomp_release(ctx);
    return 0;
}
