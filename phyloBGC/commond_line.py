from phyloBGC.main import *
import os
import argparse

import importlib_resources

#通过终端选择运行模式
__version__ = '0.1.0'


def main():

    print("\n\nphyloBGC (%s) \n" %__version__)
    #命令行参数设置
    parser = argparse.ArgumentParser(description='phyloBGC: a tool to generate BGC networks based on phylogenesis.')

    parser.add_argument('-v', '--version', action='version', version=__version__, 
            help='print version and exit')
    parser.add_argument('run', metavar='subcommand', 
            help='one of the subcommands: download, check, taxonomy, antismash, bigscape, all')
    parser.add_argument('-g', '--genus',
            help="genus name, e.g. 'Streptomyces'")
    parser.add_argument('-p', '--path', 
            help='the path to save the results')
    parser.add_argument('-f', '--format', default='fasta', 
            help='the format of the genome files, default: fasta')
    parser.add_argument('-c', '--completeness', default=95, type=int,
            help='the completeness of the genome, default: 95')
    parser.add_argument('-t', '--contamination', default=15, type=int,
            help='the contamination of the genome, default: 15')    
    parser.add_argument('-n', '--contigs', default=1000, type=int,
            help='the number of contigs of the genome, default: 1000')
    parser.add_argument('-N', '--N50', default=5000, type=int,
            help='the N50 of the genome, default: 5000')
    parser.add_argument('-C', '--cpus', default=56, type=int,
            help='the number of cpus to use, default: 56')
    parser.add_argument('-m', '--mode', default='global',
            help='the mode of bigscape, default: global')
    parser.add_argument('-complete', '--complete_genomes', action='store_true',
            help='only download complete genomes, default: False')
    args = parser.parse_args()

    #处理命令行参数

    if args.run not in ['download', 'check', 'taxonomy', 'antismash', 'bigscape', 'all']:
        print("Expecting one of the subcommands: create_dataset, train_model, analyze_mzml, viz_result, extract_ms2.")
    if args.run == 'download':
        if args.genus is None:
            print('Please specify the genus name.')
        else:
            if args.path is None:
                print('Please specify the path to save the results.')
            else:
                if args.complete_genomes:
                    download_complete_genomes_workflow(args.genus,args.path,args.format)
                else:
                    download_all_genomes_workflow(args.genus,args.path,args.format)
    if args.run == 'check':
        if args.path is None:
            print('Please specify the path to save the results.')
        else:
            checkM_evaluation_workflow(args.path,args.cpus,args.completeness,args.contamination,args.contigs,args.N50)
    if args.run == 'taxonomy':
        if args.path is None:
            print('Please specify the path to save the results.')
        else:
            gtbtk_analysis_workflow(args.path, args.genus, args.cpus)
    if args.run == 'antismash':
        if args.path is None:
            print('Please specify the path to save the results.')
        else:
            run_antismash_workflow(args.path,args.cpus)
    if args.run == 'bigscape':
        if args.path is None:
            print('Please specify the path to save the results.')
        else:
            run_bigscape_workflow(args.path,args.mode)
    if args.run == 'all':
        if args.genus is None:
            print('Please specify the genus name.')
        else:
            if args.path is None:
                print('Please specify the path to save the results.')
            else:
                if args.complete_genomes:
                    pyloBGC_complete_genomes(args.genus,args.path,args.format,args.completeness,args.contamination,args.contigs,args.N50,args.cpus,args.mode)
                else:
                    pyloBGC_all_genomes(args.genus,args.path,args.format,args.completeness,args.contamination,args.contigs,args.N50,args.cpus,args.mode)

  
if __name__ == '__main__':
    main()