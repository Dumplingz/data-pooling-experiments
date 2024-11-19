for size in 1MB 10MB 100MB 1GB 10GB
# for size in 1MB 10MB
# for size in 10GB
do
    echo "Running join_scenario_experiment for $size"
    python -m join $size 11 &> join_scenario_experiment_$size.log
done
