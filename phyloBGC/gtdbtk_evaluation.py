import pandas as pd
import glob
import os
import subprocess
    
def gtdbtkAnalyze(path, cpus=8):
    # Run the checkm command
    input_ = path + "/fasta"
    output = path + "/fasta_classify_wf"

    format = os.listdir(input_)[0].rsplit('.',1)[-1]
  
    # Run gtdbtk command
    command = ['conda run -n gtdbtk-2.3.2 nohup gtdbtk classify_wf --genome_dir '+input_+ ' --out_dir ' + output +' --skip_ani_screen --extension '+ format +' --cpus '+ str(cpus)]

    # If gtdbtk is in a specific environment, you can use the following command
    # you can use conda env list to check the path of gtdbtk and replace the path in the command
    command = ['conda run -p /home/xyy/miniconda3_py311/miniconda3_py311/envs/gtdbtk-2.3.2 nohup gtdbtk classify_wf --genome_dir '+input_+ ' --out_dir ' + output +' --skip_ani_screen --extension '+ format +' --cpus '+ str(cpus)]
    subprocess.run(command, shell=True, check=True)

    # building tree
    path_ = os.path.join(path, 'fasta_classify_wf','align')
    if 'gtdbtk.bac120.user_msa.fasta.gz' in os.listdir(path_):
        subprocess.run(['gunzip', path_ + '/gtdbtk.bac120.user_msa.fasta.gz'], check=True)
   
    command = ['conda run -n gtdbtk-2.3.2 gtdbtk infer --msa_file '+ path_ +'/gtdbtk.bac120.user_msa.fasta --out_dir '+ path_ +'/infer --cpus '+ str(cpus)]     
    # command = ['conda run -p /home/xyy/miniconda3_py311/miniconda3_py311/envs/gtdbtk-2.3.2 gtdbtk infer --msa_file '+ path_ +'/gtdbtk.bac120.user_msa.fasta --out_dir '+ path_ +'/infer --cpus '+ str(cpus)]
    subprocess.run(command, shell=True, check=True)

    command = ['conda run -n gtdbtk-2.3.2 gtdbtk decorate --input_tree '+ path_ +'/infer/gtdbtk.unrooted.tree --output_tree '+ path_ +'/output.tree --gtdbtk_classification_file '+ path +'/fasta_classify_wf/gtdbtk.bac120.summary.tsv']
    # command = ['conda run -p /home/xyy/miniconda3_py311/miniconda3_py311/envs/gtdbtk-2.3.2 gtdbtk decorate --input_tree '+ path_ +'/infer/gtdbtk.unrooted.tree --output_tree '+ path_ +'/output.tree --gtdbtk_classification_file '+ path +'/fasta_classify_wf/gtdbtk.bac120.summary.tsv']
    subprocess.run(command, shell=True, check=True)

    print('gtdbtk analysis is done!')


def gtdbtkEvaluation(path,genus):
    file = path + '/fasta_classify_wf/gtdbtk.bac120.summary.tsv'
    df = pd.read_csv(file, sep='\t', header=0)
    df = df[['user_genome','classification']]
    genbank_list = df['user_genome'].tolist()
    classification_list = df['classification'].tolist()
    correct_list = []
    for i in range(len(classification_list)):
        classification_list[i] = classification_list[i].split('g__')[1].split(';')[0]
        if classification_list[i] == genus:
            correct_list.append(genbank_list[i].split('.')[0])

    # 挑选除去分类不正确的基因组

    if 'fasta_incorrect_classfication' not in os.listdir(path):
        os.mkdir(path + '/fasta_incorrect_classfication')   
    fasta_files=os.listdir(os.path.join(path,'fasta'))
    for file in fasta_files:
        if file.split('.')[0] not in correct_list:
            os.rename(path+'/fasta/'+file,path+ '/fasta_incorrect_classfication/' +file)

    print('The number of correct strains is: ',len(correct_list))
    print('gtbtk evaluation is done!')

# 主函数
def gtbtk_analysis_workflow(path, genus, cpus=56):
    gtdbtkAnalyze(path, cpus)
    gtdbtkEvaluation(path, genus)

 

if __name__ == '__main__':
    path = '/home/xyy/test'
    # gtdbtkAnalyze(path)
    # gtdbtkEvaluation(path,'Kitasatospora')
    gtdbtk_building_tree(path)

