#ifndef ZONE0_RECORD_H
#define ZONE0_RECORD_H

#include <sys/msg.h>
#define ZONE0_IPC_KEY 0x07282026
#define MSG_DATA_LEN 256

typedef struct {
    long mtype;
    char data[MSG_DATA_LEN];
} zone0_msg_t;

void zone0_log_record(zone0_msg_t *msg)
{
    FILE *log_fp = fopen("zone0_runtime.log", "a");
    if (log_fp)
    {
        fprintf(log_fp, "[%ld] %s\n", msg->mtype, msg->data);
        fclose(log_fp);
    }
}

#endif
