#!/bin/bash
set -e
# 全链路防御验收校验脚本
echo "===== Zone0 Defense Full Verification Script ====="

# 1. 编译全部源码
gcc zone0_guardian.c -o zone0_guardian -lseccomp
gcc legitimate_client.c -o legit_client
gcc legitimate_client_with_seccomp.c -o legit_seccomp_client -lseccomp
gcc malicious_attack.c -o mal_client

# 2. 后台启动守护进程
./zone0_guardian &
GUARDIAN_PID=$!
sleep 1

# 3. 合法客户端测试
echo "Run standard legitimate client"
./legit_client

# 4. 加固客户端自检测试（核心校验项）
echo "Run seccomp hardened self-check client"
./legit_seccomp_client

# 5. 恶意载荷攻击测试
echo "Run malicious attack simulation"
./mal_client

# 6. 收尾清理
kill $GUARDIAN_PID
rm -f zone0_guardian legit_client legit_seccomp_client mal_client
echo "===== All defense verification finished ====="
