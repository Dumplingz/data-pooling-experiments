for size in 1MB 10MB 100MB 1GB 10GB
# for size in 1MB 10MB
do
    echo "Running join_scenario_experiment for $size"
    python -m join $size 10 &> join_scenario_experiment_$size.log
done