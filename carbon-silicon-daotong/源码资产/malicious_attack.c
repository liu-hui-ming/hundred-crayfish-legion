#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include "zone0_record.h"

// 模拟恶意客户端：尝试直写本地文件、越权读写，用于防御有效性测试
int main()
{
    // 尝试违规本地文件写入
    int fd = open("/tmp/attack_payload.log", O_WRONLY | O_CREAT, 0644);
    if (fd > 0)
    {
        write(fd, "malicious payload", 17);
        close(fd);
        printf("Malicious write success\n");
    }
    else
    {
        printf("Malicious file write blocked\n");
    }

    // 尝试通过IPC通道投递异常载荷
    int msq_id = msgget(ZONE0_IPC_KEY, 0644);
    zone0_msg_t bad_msg;
    bad_msg.mtype = 99;
    snprintf(bad_msg.data, sizeof(bad_msg.data), "overflow malicious string");
    msgsnd(msq_id, &bad_msg, sizeof(bad_msg.data), 0);
    return 0;
}
