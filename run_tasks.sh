export resdir=/fs/clip-realspeech/projects/lfe/eval/utt_abx
export PATH=/fs/clip-realspeech/software/conda/bin:$PATH
source activate abx

# params to be changed
export task=WSJ_sample12_norej_min3_max100
export err=$resdir/err/$task.txt
export out=$resdir/out/$task.txt
sbatch --job-name=$task.task --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task"
sbatch --job-name=$task.stats --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task_stats --stats"

export task=GPJ_sample12_norej_min3_max100
export err=$resdir/err/$task.txt
export out=$resdir/out/$task.txt
sbatch --job-name=$task.task --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task"
sbatch --job-name=$task.stats --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task_stats --stats"

export task=BUC_sample20_norej_min3_max100
export err=$resdir/err/$task.txt
export out=$resdir/out/$task.txt
sbatch --job-name=$task.task --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task"
sbatch --job-name=$task.stats --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task_stats --stats"

export task=CSJ_sample20_norej_min3_max100
export err=$resdir/err/$task.txt
export out=$resdir/out/$task.txt
sbatch --job-name=$task.task --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task"
sbatch --job-name=$task.stats --mem-per-cpu=4000 --ntasks=1 -p dpart --qos batch --time 1-00:00:00 -e $err -o $out --wrap "python /fs/clip-realspeech/projects/lfe/code/lfe-repo/generate_task_utt.py $resdir/items/$task.item $resdir/tasks/$task.task_stats --stats"