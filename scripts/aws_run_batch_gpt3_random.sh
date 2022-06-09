log_mode=$1
case=$2

bash aws_run_gpt3_scheduled_1gpu_training.sh gpt3_xl_pp8_dp8.sh 2 3 64 $log_mode $case
sleep 5s
bash copy_rank0_logs.sh
