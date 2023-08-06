
# Auto generated tab completion for the temci (0.5) benchmarking tool.


#compdef temci
_temci(){
    # printf '%s ' "${words[@]}" > /tmp/out
    local ret=11 state

    local -a common_opts
    common_opts=(
        --log_level"[Logging level]: :('debug' 'info' 'warn' 'error' 'quiet')"
	--settings_file"[Additional settings file]: :_files -g '*\.yaml'"
	--tmp_dir"[Used temporary directory]: :()"
    )

    typeset -A opt_args
    _arguments   -C  ':subcommand:->subcommand' '2: :->second_level' '*::options:->options' && ret=0
    #echo $state > tmp_file

    local sub_cmd=""
    case $words[1] in
        temci)
            sub_cmd=$words[2]
            ;;
        *)
            sub_cmd=$words[1]
    esac

    #echo $words[@] >> tmp_file

    case $words[2] in
        (clean)
            state="options"
            ;;
    esac


    case $state in
    subcommand)
        local -a subcommands
        subcommands=(
            "exec:Implements a simple run driver that just executes one of the passed run_cmds" "build:Build program blocks" "assembler:Wrapper around the gnu assembler to allow assembler randomization" "clean:Clean up the temporary files" "short:Utility commands to ease working directly on the command line" "setup:Compile all needed binaries in the temci scripts folder" "completion:Creates completion files for several shells." "version:Print the current version (0.5)" "report:Generate a report from benchmarking result" "init:Helper commands to initialize files (like settings)"
        )

        _describe -t subcommands 'temci subcommand' subcommands && ret=0
    ;;
    
    second_level)

        #echo $words[@] > tmp_file
        case $words[2] in
    
            (short)
                #echo "here" > tmp_file
                local -a subcommands
                subcommands=(
                    "exec:Exec code snippets directly with the exec run driver"
                )
                _describe -t subcommands 'temci subcommand' subcommands && ret=0 && return 0
                ;;
        
            (completion)
                #echo "here" > tmp_file
                local -a subcommands
                subcommands=(
                    "zsh:Creates a new tab completion file for zsh and returns it's file name"
	"bash:Creates a new tab completion file for zsh and returns it's file name"
                )
                _describe -t subcommands 'temci subcommand' subcommands && ret=0 && return 0
                ;;
        
            (init)
                #echo "here" > tmp_file
                local -a subcommands
                subcommands=(
                    "settings:Create a new settings file temci.yaml in the current directory"
	"build_config:Interactive cli to create (or append to) a build config file"
	"run_config:Interactive cli to create (or append to) a run config file"
                )
                _describe -t subcommands 'temci subcommand' subcommands && ret=0 && return 0
                ;;
        
            (build|report|exec)
                _arguments "2: :_files -g '*\.yaml' "            ;;
        esac
        ;;
        
    (options)
        local -a args
        args=(
        $common_opts
        )
        #echo "options" $words[@] > tmp_file


        case $words[1] in

        
        exec)
            case $words[2] in
                *.yaml)
                    args=(
                    $common_opts
                    {--append,--no-append}"[Append to the output file instead of overwriting by adding new run data blocks]"
	{--cpu_governor,--no-cpu_governor}"[Enable:   Allows the setting of the scaling governor of all cpu cores, to ensure that all use the same.]"
	--cpu_governor_governor"[New scaling governor for all cpus]: :()"
	{--cpuset_active,--no-cpuset_active}"[Use cpuset functionality?]"
	--cpuset_base_core_number"[Number of cpu cores for the base (remaining part of the) system]: :(0 1 2 3)"
	--cpuset_parallel"[0: benchmark sequential, > 0: benchmark parallel with n instances, -1: determine n automatically]: :()"
	--cpuset_sub_core_number"[Number of cpu cores per parallel running program.]: :(0 1 2 3)"
	{--disable_cpu_caches,--no-disable_cpu_caches}"[Enable:   Disable the L1 and L2 caches on x86 and x86-64 architectures.]"
	{--disable_hyper_threading,--no-disable_hyper_threading}"[Disable the hyper threaded cores. Good for cpu bound programs.]"
	{--disable_swap,--no-disable_swap}"[Enable:   Disables swapping on the system before the benchmarking and enables it after.]"
	--discarded_blocks"[First n blocks that are discarded]: :()"
	--driver"[Possible plugins are: 'exec']: :('exec')"
	{--drop_fs_caches,--no-drop_fs_caches}"[Enable:   Drop page cache, directoy entries and inodes before every benchmarking run.]"
	{--drop_fs_caches_free_dentries_inodes,--no-drop_fs_caches_free_dentries_inodes}"[Free dentries and inodes]"
	{--drop_fs_caches_free_pagecache,--no-drop_fs_caches_free_pagecache}"[Free the page cache]"
	{--env_randomize,--no-env_randomize}"[Enable:   Adds random environment variables.]"
	--env_randomize_key_max"[Maximum length of each random key]: :()"
	--env_randomize_max"[Maximum number of added random environment variables]: :()"
	--env_randomize_min"[Minimum number of added random environment variables]: :()"
	--env_randomize_var_max"[Maximum length of each random value]: :()"
	--in"[Input file with the program blocks to benchmark]: :_files -g '*\.yaml'"
	--max_runs"[Maximum number of benchmarking runs]: :()"
	--max_time"[Maximum time the whole benchmarking should take +- time to execute one block.]: :()"
	--min_runs"[Minimum number of benchmarking runs]: :()"
	{--nice,--no-nice}"[Enable:   Allows the setting of the nice and ionice values of the benchmarking process.]"
	--nice_io_nice"[Specify the name or number of the scheduling class to use;0 for none, 1 for realtime, 2 for best-effort, 3 for idle.]: :(0 1 2 3)"
	--nice_nice"[Niceness values range from -20 (most favorable to the process) to 19 (least favorable to the process).]: :()"
	{--other_nice,--no-other_nice}"[Enable:   Allows the setting of the nice value of all other processes (tha have nice > -10).]"
	--other_nice_min_nice"[Processes with lower nice values are ignored.]: :()"
	--other_nice_nice"[Niceness values for other processes.]: :()"
	--out"[Output file for the benchmarking results]: :_files -g '*\.yaml'"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_repeat"[If runner=perf_stat make measurements of the programrepeated n times. Therefore scale the number of times a program.is benchmarked.]: :()"
	{--preheat,--no-preheat}"[Enable:   Preheats the system with a cpu bound task]"
	--preheat_time"[Number of seconds to preheat the system with an cpu bound task]: :()"
	{--random_cmd,--no-random_cmd}"[Pick a random command if more than one run command is passed.]"
	--run_block_size"[Number of benchmarking runs that are done together]: :()"
	--runner"[If not '' overrides the runner setting for each program block]: :('' 'perf_stat' 'rusage' 'spec')"
	--runs"[if != -1 sets max and min runs to it's value]: :()"
	--send_mail"[If not empty, recipient of a mail after the benchmarking finished.]: :()"
	{--show_report,--no-show_report}"[Print console report if log_level=info]"
	{--shuffle,--no-shuffle}"[Randomize the order in which the program blocks are benchmarked.]"
	{--sleep,--no-sleep}"[Enable:   Sleep a given amount of time before the benchmarking begins.]"
	--sleep_seconds"[Seconds to sleep]: :()"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_tester"[Possible plugins are: 'anderson', 'ks', 't']: :('t' 'ks' 'anderson')"
	--stats_uncertainty_range"[Range of p values that allow no conclusion.]: :()"
	{--stop_start,--no-stop_start}"[Enable:   Stop almost all other processes.]"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	{--stop_start_dry_run,--no-stop_start_dry_run}"[Just output the to be stopped processes but don't actually stop them?]"
	--stop_start_min_id"[Processes with lower id are ignored.]: :()"
	--stop_start_min_nice"[Processes with lower nice values are ignored.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	{--sync,--no-sync}"[Enable:   Call sync before each program execution.]"
                    )
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
                *)
                    _arguments "1:: :echo 3" && ret=0
            esac
        ;;
        
        (report)
            #echo "(report)" $words[2]
            case $words[2] in
                *.yaml)
                    args=(
                    $common_opts
                    --console_out"[Output file name or stdard out (-)]: :_files"
	--html2_alpha"[Alpha value for confidence intervals]: :()"
	--html2_boxplot_height"[Height per run block for the big comparison box plots]: :()"
	--html2_fig_width_big"[Width of all big plotted figures]: :()"
	--html2_fig_width_small"[Width of all small plotted figures]: :()"
	{--html2_gen_pdf,--no-html2_gen_pdf}"[Generate pdf versions of the plotted figures?]"
	{--html2_gen_tex,--no-html2_gen_tex}"[Generate simple latex versions of the plotted figures?]"
	--html2_html_filename"[Name of the HTML file]: :()"
	--html2_out"[Output directory]: :()"
	{--html2_show_zoomed_out,--no-html2_show_zoomed_out}"[Show zoomed out (x min = 0) figures in the extended summaries?]"
	--html_compare_against"[Run to to use as base run for relative values in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_compared_props"[Properties to include in comparison table]: :()"
	--html_html_filename"[Name of the HTML file]: :()"
	--html_out"[Output directory]: :()"
	--html_pair_kind"[Kind of plot to draw for pair plots (see searborn.joinplot)]: :('scatter' 'reg' 'resid' 'kde' 'hex')"
	--html_plot_size"[Width of the plots in centimeters]: :()"
	--in"[File that contains the benchmarking results]: :_files -g '*\.yaml'"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--reporter"[Possible plugins are: 'console', 'html', 'html2']: :('console' 'html' 'html2')"
	--tester"[Possible plugins are: 'anderson', 'ks', 't']: :('t' 'ks' 'anderson')"
	--uncertainty_range"[Range of p values that allow no conclusion.]: :()"
                    )
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
                *)
                    _arguments "1:: :echo 3" && ret=0
            esac
        ;;
        (build)
            case $words[2] in
                *.yaml)
                    args=(
                    $common_opts
                    --in"[Input file with the program blocks to build]: :_files -g '*\.yaml'"
	--out"[Resulting run config file]: :()"
                    )
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
                *)
                    _arguments "1:: :echo 3" && ret=0
            esac
        ;;
    
        (short)
            case $words[2] in
            
                exec)
                    #echo "exec" $words[@] > tmp_file
                    args+=(
                        
                        {--append,--no-append}"[Append to the output file instead of overwriting by adding new run data blocks]"
	{--append,--no-append}"[Append to the output file instead of overwriting by adding new run data blocks]"
	{--cpu_governor,--no-cpu_governor}"[Enable:   Allows the setting of the scaling governor of all cpu cores, to ensure that all use the same.]"
	--cpu_governor_governor"[New scaling governor for all cpus]: :()"
	{--cpuset_active,--no-cpuset_active}"[Use cpuset functionality?]"
	--cpuset_base_core_number"[Number of cpu cores for the base (remaining part of the) system]: :(0 1 2 3)"
	--cpuset_parallel"[0: benchmark sequential, > 0: benchmark parallel with n instances, -1: determine n automatically]: :()"
	--cpuset_sub_core_number"[Number of cpu cores per parallel running program.]: :(0 1 2 3)"
	{--disable_cpu_caches,--no-disable_cpu_caches}"[Enable:   Disable the L1 and L2 caches on x86 and x86-64 architectures.]"
	{--disable_hyper_threading,--no-disable_hyper_threading}"[Disable the hyper threaded cores. Good for cpu bound programs.]"
	{--disable_hyper_threading,--no-disable_hyper_threading}"[Disable the hyper threaded cores. Good for cpu bound programs.]"
	{--disable_swap,--no-disable_swap}"[Enable:   Disables swapping on the system before the benchmarking and enables it after.]"
	--discarded_blocks"[First n blocks that are discarded]: :()"
	--discarded_blocks"[First n blocks that are discarded]: :()"
	--driver"[Possible plugins are: 'exec']: :('exec')"
	--driver"[Possible plugins are: 'exec']: :('exec')"
	{--drop_fs_caches,--no-drop_fs_caches}"[Enable:   Drop page cache, directoy entries and inodes before every benchmarking run.]"
	{--drop_fs_caches_free_dentries_inodes,--no-drop_fs_caches_free_dentries_inodes}"[Free dentries and inodes]"
	{--drop_fs_caches_free_pagecache,--no-drop_fs_caches_free_pagecache}"[Free the page cache]"
	{--env_randomize,--no-env_randomize}"[Enable:   Adds random environment variables.]"
	--env_randomize_key_max"[Maximum length of each random key]: :()"
	--env_randomize_max"[Maximum number of added random environment variables]: :()"
	--env_randomize_min"[Minimum number of added random environment variables]: :()"
	--env_randomize_var_max"[Maximum length of each random value]: :()"
	--in"[Input file with the program blocks to benchmark]: :_files -g '*\.yaml'"
	--in"[Input file with the program blocks to benchmark]: :_files -g '*\.yaml'"
	--max_runs"[Maximum number of benchmarking runs]: :()"
	--max_runs"[Maximum number of benchmarking runs]: :()"
	--max_time"[Maximum time the whole benchmarking should take +- time to execute one block.]: :()"
	--max_time"[Maximum time the whole benchmarking should take +- time to execute one block.]: :()"
	--min_runs"[Minimum number of benchmarking runs]: :()"
	--min_runs"[Minimum number of benchmarking runs]: :()"
	{--nice,--no-nice}"[Enable:   Allows the setting of the nice and ionice values of the benchmarking process.]"
	--nice_io_nice"[Specify the name or number of the scheduling class to use;0 for none, 1 for realtime, 2 for best-effort, 3 for idle.]: :(0 1 2 3)"
	--nice_nice"[Niceness values range from -20 (most favorable to the process) to 19 (least favorable to the process).]: :()"
	{--other_nice,--no-other_nice}"[Enable:   Allows the setting of the nice value of all other processes (tha have nice > -10).]"
	--other_nice_min_nice"[Processes with lower nice values are ignored.]: :()"
	--other_nice_nice"[Niceness values for other processes.]: :()"
	--out"[Output file for the benchmarking results]: :_files -g '*\.yaml'"
	--out"[Output file for the benchmarking results]: :_files -g '*\.yaml'"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_props"[Measured properties]: :()"
	--perf_stat_repeat"[If runner=perf_stat make measurements of the programrepeated n times. Therefore scale the number of times a program.is benchmarked.]: :()"
	{--preheat,--no-preheat}"[Enable:   Preheats the system with a cpu bound task]"
	--preheat_time"[Number of seconds to preheat the system with an cpu bound task]: :()"
	{--random_cmd,--no-random_cmd}"[Pick a random command if more than one run command is passed.]"
	--run_block_size"[Number of benchmarking runs that are done together]: :()"
	--run_block_size"[Number of benchmarking runs that are done together]: :()"
	--runner"[If not '' overrides the runner setting for each program block]: :('' 'perf_stat' 'rusage' 'spec')"
	--runs"[if != -1 sets max and min runs to it's value]: :()"
	--runs"[if != -1 sets max and min runs to it's value]: :()"
	--send_mail"[If not empty, recipient of a mail after the benchmarking finished.]: :()"
	--send_mail"[If not empty, recipient of a mail after the benchmarking finished.]: :()"
	{--show_report,--no-show_report}"[Print console report if log_level=info]"
	{--show_report,--no-show_report}"[Print console report if log_level=info]"
	{--shuffle,--no-shuffle}"[Randomize the order in which the program blocks are benchmarked.]"
	{--shuffle,--no-shuffle}"[Randomize the order in which the program blocks are benchmarked.]"
	{--sleep,--no-sleep}"[Enable:   Sleep a given amount of time before the benchmarking begins.]"
	--sleep_seconds"[Seconds to sleep]: :()"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_properties"[Properties to use for reporting and null hypothesis tests]: :(__ov-time cache-misses cycles task-clock instructions branch-misses cache-references all)"
	--stats_tester"[Possible plugins are: 'anderson', 'ks', 't']: :('t' 'ks' 'anderson')"
	--stats_tester"[Possible plugins are: 'anderson', 'ks', 't']: :('t' 'ks' 'anderson')"
	--stats_uncertainty_range"[Range of p values that allow no conclusion.]: :()"
	--stats_uncertainty_range"[Range of p values that allow no conclusion.]: :()"
	{--stop_start,--no-stop_start}"[Enable:   Stop almost all other processes.]"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes"[Each process which name (lower cased) starts with one of the prefixes is not ignored. Overrides the decision based on the min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	--stop_start_comm_prefixes_ignored"[Each process which name (lower cased) starts with one of the prefixes is ignored. It overrides the decisions based on comm_prefixes and min_id.]: :()"
	{--stop_start_dry_run,--no-stop_start_dry_run}"[Just output the to be stopped processes but don't actually stop them?]"
	--stop_start_min_id"[Processes with lower id are ignored.]: :()"
	--stop_start_min_nice"[Processes with lower nice values are ignored.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	--stop_start_subtree_suffixes"[Suffixes of processes names which are stopped.]: :()"
	{--sync,--no-sync}"[Enable:   Call sync before each program execution.]"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-d,--with_description}"[DESCRIPTION COMMAND: Benchmark the command and set its description attribute.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
	{-wd,--without_description}"[COMMAND: Benchmark the command and use itself as its description.]: :_command"
                    )

                    #echo "sdf" $args[@] > tmp_file
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
            
            esac
            ;;
        
        (completion)
            case $words[2] in
            
                zsh)
                    #echo "zsh" $words[@] > tmp_file
                    args+=(
                        
                        
                    )

                    #echo "sdf" $args[@] > tmp_file
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
            
                bash)
                    #echo "bash" $words[@] > tmp_file
                    args+=(
                        
                        
                    )

                    #echo "sdf" $args[@] > tmp_file
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
            
            esac
            ;;
        
        (init)
            case $words[2] in
            
                settings)
                    #echo "settings" $words[@] > tmp_file
                    args+=(
                        
                        
                    )

                    #echo "sdf" $args[@] > tmp_file
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
            
                build_config)
                    #echo "build_config" $words[@] > tmp_file
                    args+=(
                        
                        
                    )

                    #echo "sdf" $args[@] > tmp_file
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
            
                run_config)
                    #echo "run_config" $words[@] > tmp_file
                    args+=(
                        
                        
                    )

                    #echo "sdf" $args[@] > tmp_file
                    _arguments "1:: :echo 3" $args && ret=0
                ;;
            
            esac
            ;;
        
    esac



        case $sub_cmd in
    
        clean)
            # echo "clean" $words[@] >> tmp_file
            args+=(
                
            )
            case $words[2] in
                $sub_cmd)
                    _arguments "1:: :echo 3" $args && ret=0
                    ;;
                *)
                    # echo "Hi" >> tmp_file
                    _arguments $args && ret=0
                    ;;
            esac
        ;;
    
        esac

        #_arguments $common_opts && ret=0 && return 0
    ;;
    esac
    }

    compdef _temci temci=temci
    