#/bin/bash
# GNU parallel命令是非常强大的并行计算命令，使用-j参数控制其并发数量。

all_num=10
thread_num=6

a=$(date +%H%M%S)


parallel -j 5 "sleep 1;echo {}" ::: `seq 1 10`

b=$(date +%H%M%S)

echo -e "startTime:\t$a"
echo -e "endTime:\t$b"
