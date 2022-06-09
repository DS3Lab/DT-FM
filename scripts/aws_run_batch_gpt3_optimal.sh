case=$1
if [ $case -eq 1 ]
then
  bash aws_run_gpt3_optimal_Ngpu_training.sh gpt3_xl_pp8_dp8.sh 1 2 3 64 $case
elif [ $case -eq 2 ]
then
  bash aws_run_gpt3_optimal_Ngpu_training.sh gpt3_xl_pp8_dp8.sh 2 2 3 64 $case
else
  bash aws_run_gpt3_optimal_1gpu_training.sh gpt3_xl_pp8_dp8.sh 2 3 64 $case
fi
sleep 5s
bash copy_rank0_logs.sh
