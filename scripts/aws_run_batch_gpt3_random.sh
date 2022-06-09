log_mode="random_2022"

case=$1

if [ $case -eq 1 ]
then
  bash aws_run_gpt3_scheduled_Ngpu_training.sh gpt3_xl_pp8_dp8.sh 1 2 3 64 $log_mode $case
elif [ $case -eq 2 ]
then
  bash aws_run_gpt3_scheduled_Ngpu_training.sh gpt3_xl_pp8_dp8.sh 2 2 3 64 $log_mode $case
else
  bash aws_run_gpt3_scheduled_1gpu_training.sh gpt3_xl_pp8_dp8.sh 2 3 64 $log_mode $case
fi

sleep 5s
bash copy_rank0_logs.sh
