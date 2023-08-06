
    # Auto generated tab completion for the temci (0.5) benchmarking tool.


    _temci(){
        local cur=${COMP_WORDS[COMP_CWORD]}
        local prev=${COMP_WORDS[COMP_CWORD-1]}

        local common_opts=(
            --log_level
	--settings_file
	--tmp_dir
        )
        local args=(
            --log_level
	--settings_file
	--tmp_dir
        )
        local run_common_opts=(
            --append
	--no-append
	--disable_hyper_threading
	--no-disable_hyper_threading
	--discarded_blocks
	--driver
	--in
	--max_runs
	--max_time
	--min_runs
	--out
	--run_block_size
	--runs
	--send_mail
	--show_report
	--no-show_report
	--shuffle
	--no-shuffle
	--stats_properties
	--stats_tester
	--stats_uncertainty_range
        )
        local report_common_opts=(
            --console_out
	--html2_alpha
	--html2_boxplot_height
	--html2_fig_width_big
	--html2_fig_width_small
	--html2_gen_pdf
	--no-html2_gen_pdf
	--html2_gen_tex
	--no-html2_gen_tex
	--html2_html_filename
	--html2_out
	--html2_show_zoomed_out
	--no-html2_show_zoomed_out
	--html_compare_against
	--html_compared_props
	--html_html_filename
	--html_out
	--html_pair_kind
	--html_plot_size
	--in
	--properties
	--reporter
	--tester
	--uncertainty_range
        )
        local build_common_opts=(
            --in
	--out
        )

        
                case ${COMP_WORDS[1]} in
                init)
                    case ${COMP_WORDS[2]} in
            
                        build_config)
                            args=(
                                ${common_opts[@]}
                                
                                
                            )
                            # printf '   _%s ' "${args[@]}" >> /tmp/out
                            # printf '   __%s ' "${args[*]}" >> /tmp/out
                            COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                        ;;
                
                        settings)
                            args=(
                                ${common_opts[@]}
                                
                                
                            )
                            # printf '   _%s ' "${args[@]}" >> /tmp/out
                            # printf '   __%s ' "${args[*]}" >> /tmp/out
                            COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                        ;;
                
                        run_config)
                            args=(
                                ${common_opts[@]}
                                
                                
                            )
                            # printf '   _%s ' "${args[@]}" >> /tmp/out
                            # printf '   __%s ' "${args[*]}" >> /tmp/out
                            COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                        ;;
                
                        *)
                            local args=( )
                            COMPREPLY=( $(compgen -W "" -- $cur) ) && return 0
                    esac
                    ;;
                *)
                ;;
              esac
            
                case ${COMP_WORDS[1]} in
                completion)
                    case ${COMP_WORDS[2]} in
            
                        bash)
                            args=(
                                ${common_opts[@]}
                                
                                
                            )
                            # printf '   _%s ' "${args[@]}" >> /tmp/out
                            # printf '   __%s ' "${args[*]}" >> /tmp/out
                            COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                        ;;
                
                        zsh)
                            args=(
                                ${common_opts[@]}
                                
                                
                            )
                            # printf '   _%s ' "${args[@]}" >> /tmp/out
                            # printf '   __%s ' "${args[*]}" >> /tmp/out
                            COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                        ;;
                
                        *)
                            local args=( )
                            COMPREPLY=( $(compgen -W "" -- $cur) ) && return 0
                    esac
                    ;;
                *)
                ;;
              esac
            
                case ${COMP_WORDS[1]} in
                short)
                    case ${COMP_WORDS[2]} in
            
                        exec)
                            args=(
                                ${common_opts[@]}
                                
                                --append
	--no-append
	--append
	--no-append
	--cpu_governor
	--no-cpu_governor
	--cpu_governor_governor
	--cpuset_active
	--no-cpuset_active
	--cpuset_base_core_number
	--cpuset_parallel
	--cpuset_sub_core_number
	--disable_cpu_caches
	--no-disable_cpu_caches
	--disable_hyper_threading
	--no-disable_hyper_threading
	--disable_hyper_threading
	--no-disable_hyper_threading
	--disable_swap
	--no-disable_swap
	--discarded_blocks
	--discarded_blocks
	--driver
	--driver
	--drop_fs_caches
	--no-drop_fs_caches
	--drop_fs_caches_free_dentries_inodes
	--no-drop_fs_caches_free_dentries_inodes
	--drop_fs_caches_free_pagecache
	--no-drop_fs_caches_free_pagecache
	--env_randomize
	--no-env_randomize
	--env_randomize_key_max
	--env_randomize_max
	--env_randomize_min
	--env_randomize_var_max
	--in
	--in
	--max_runs
	--max_runs
	--max_time
	--max_time
	--min_runs
	--min_runs
	--nice
	--no-nice
	--nice_io_nice
	--nice_nice
	--other_nice
	--no-other_nice
	--other_nice_min_nice
	--other_nice_nice
	--out
	--out
	--perf_stat_props
	--perf_stat_repeat
	--preheat
	--no-preheat
	--preheat_time
	--random_cmd
	--no-random_cmd
	--run_block_size
	--run_block_size
	--runner
	--runs
	--runs
	--send_mail
	--send_mail
	--show_report
	--no-show_report
	--show_report
	--no-show_report
	--shuffle
	--no-shuffle
	--shuffle
	--no-shuffle
	--sleep
	--no-sleep
	--sleep_seconds
	--stats_properties
	--stats_properties
	--stats_tester
	--stats_tester
	--stats_uncertainty_range
	--stats_uncertainty_range
	--stop_start
	--no-stop_start
	--stop_start_comm_prefixes
	--stop_start_comm_prefixes_ignored
	--stop_start_dry_run
	--no-stop_start_dry_run
	--stop_start_min_id
	--stop_start_min_nice
	--stop_start_subtree_suffixes
	--sync
	--no-sync
	--with_description
	-d
	--without_description
	-wd
                            )
                            # printf '   _%s ' "${args[@]}" >> /tmp/out
                            # printf '   __%s ' "${args[*]}" >> /tmp/out
                            COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                        ;;
                
                        *)
                            local args=( )
                            COMPREPLY=( $(compgen -W "" -- $cur) ) && return 0
                    esac
                    ;;
                *)
                ;;
              esac
            

        case ${COMP_WORDS[1]} in
            report)
                case ${COMP_WORDS[2]} in
                *.yaml)
                    args=(
                        $common_opts
                        $report_common_opts
                    )
                    COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                ;;
                esac
                ;;
            build)
                case ${COMP_WORDS[2]} in
                *.yaml)
                    args=(
                        $common_opts
                        $build_common_opts
                    )
                    COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                ;;
                esac
                ;;
            
            exec)
                case ${COMP_WORDS[2]} in
                *.yaml)
                    args=(
                        $common_opts
                        $run_common_opts
                        --append
	--no-append
	--cpu_governor
	--no-cpu_governor
	--cpu_governor_governor
	--cpuset_active
	--no-cpuset_active
	--cpuset_base_core_number
	--cpuset_parallel
	--cpuset_sub_core_number
	--disable_cpu_caches
	--no-disable_cpu_caches
	--disable_hyper_threading
	--no-disable_hyper_threading
	--disable_swap
	--no-disable_swap
	--discarded_blocks
	--driver
	--drop_fs_caches
	--no-drop_fs_caches
	--drop_fs_caches_free_dentries_inodes
	--no-drop_fs_caches_free_dentries_inodes
	--drop_fs_caches_free_pagecache
	--no-drop_fs_caches_free_pagecache
	--env_randomize
	--no-env_randomize
	--env_randomize_key_max
	--env_randomize_max
	--env_randomize_min
	--env_randomize_var_max
	--in
	--max_runs
	--max_time
	--min_runs
	--nice
	--no-nice
	--nice_io_nice
	--nice_nice
	--other_nice
	--no-other_nice
	--other_nice_min_nice
	--other_nice_nice
	--out
	--perf_stat_props
	--perf_stat_repeat
	--preheat
	--no-preheat
	--preheat_time
	--random_cmd
	--no-random_cmd
	--run_block_size
	--runner
	--runs
	--send_mail
	--show_report
	--no-show_report
	--shuffle
	--no-shuffle
	--sleep
	--no-sleep
	--sleep_seconds
	--stats_properties
	--stats_tester
	--stats_uncertainty_range
	--stop_start
	--no-stop_start
	--stop_start_comm_prefixes
	--stop_start_comm_prefixes_ignored
	--stop_start_dry_run
	--no-stop_start_dry_run
	--stop_start_min_id
	--stop_start_min_nice
	--stop_start_subtree_suffixes
	--sync
	--no-sync
                    )
                    COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) ) && return 0
                ;;
                esac
                ;;
        
            *)
            ;;
        esac

        case ${COMP_WORDS[1]} in
            (report|build|exec)
                local IFS=$'
'
                local LASTCHAR=' '
                COMPREPLY=($(compgen -o plusdirs -o nospace -f -X '!*.yaml' -- "${COMP_WORDS[COMP_CWORD]}"))

                if [ ${#COMPREPLY[@]} = 1 ]; then
                    [ -d "$COMPREPLY" ] && LASTCHAR=/
                    COMPREPLY=$(printf %q%s "$COMPREPLY" "$LASTCHAR")
                else
                    for ((i=0; i < ${#COMPREPLY[@]}; i++)); do
                        [ -d "${COMPREPLY[$i]}" ] && COMPREPLY[$i]=${COMPREPLY[$i]}/
                    done
                fi
                return 0
                ;;
            
            clean)
                args=(--log_level
	--settings_file
	--tmp_dir)
                ;;
            
            init)
                args=(build_config run_config settings)
                ;;
            
            completion)
                args=(bash zsh)
                ;;
            
            short)
                args=(exec)
                ;;
            
            *)
                args=(assembler build clean completion exec init report setup short version)
        esac
        COMPREPLY=( $(compgen -W "${args[*]}" -- $cur) )
    }
    shopt -s extglob
    complete -F _temci temci
    