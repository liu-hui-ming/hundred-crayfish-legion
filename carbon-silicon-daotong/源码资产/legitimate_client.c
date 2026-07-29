#define _GNU_SOURCE
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include "zone0_record.h"

int main()
{
    int msq_id = msgget(ZONE0_IPC_KEY, 0644);
    zone0_msg_t send_msg;
    send_msg.mtype = 1;
    snprintf(send_msg.data, sizeof(send_msg.data), "legitimate zone0 client payload");

    // 仅通过IPC合法通道交互，无直接文件写入行为
    msgsnd(msq_id, &send_msg, sizeof(send_msg.data), 0);
    msgrcv(msq_id, &send_msg, sizeof(send_msg.data), 1, 0);
    printf("Client receive ack: %s\n", send_msg.data);
    return 0;
}
