#import packages
import os
from .submain.down_and_validation import download_all_genomes_workflow,download_complete_genomes_workflow
from .submain.checkM_evaluation import contamination_evaluation
from .submain.gtdbtk_evaluation import gtbtk_analysis_workflow
from .submain.run_antismash import run_antismash_workflow
from .submain.run_bigscape import run_bigscape_workflow

#download genomes and prepare fasta files
def pyloBGC_all_genomes(genus,path,format="fasta",completeness=95,contamination=15,contigs=1000,N50=5000,cpus=56,mode='global'):
    download_all_genomes_workflow(genus,path,format)
    contamination_evaluation(path,completeness,contamination,contigs,N50)
    gtbtk_analysis_workflow(path, genus, cpus)
    run_antismash_workflow(path,mode)
    run_bigscape_workflow(path,mode)
    print('BGCs networks in ', genus, ' are generated.')

def pyloBGC_complete_genomes(genus,path,format="fasta",completeness=95,contamination=15,contigs=1000,N50=5000,cpus=56,mode='global'):
    download_complete_genomes_workflow(genus,path,format="fasta")
    contamination_evaluation(path,completeness,contamination,contigs,N50)
    gtbtk_analysis_workflow(path, genus, cpus)
    run_antismash_workflow(path,mode)
    run_bigscape_workflow(path,mode)
    print('BGCs networks in ', genus, ' are generated.')

if __file__ == '__main__':
    pass

