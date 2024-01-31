import pandas as pd
import glob
import os
import subprocess

def checkManalyze(path,cpus=2,reduced_tree=True):
    
    # Run the checkm command
    output = path + "/fasta_check_output"
    input_ = path + "/fasta"
    format = os.listdir(input_)[0].rsplit('.',1)[-1]
    os.makedirs(output, exist_ok=True)
   
    #运行checkm命令
    # command = "conda run -n checkm nohup checkm lineage_wf " + input_ + " " + output + " -t " + str(t) + " -x " + format + " --reduced_tree > " + path+ "_check_output/checkManalyze.out 2>&1"

    # If checkm is in a specific environment, you can use the following command
    # you can use conda env list to check the path of checkm and replace the path in the command
    command = "conda run -p /home/xyy/miniconda3_py311/miniconda3_py311/envs/checkm nohup checkm lineage_wf " + input_ + " " + output + " -t " + str(cpus) + " -x " + format +  " --reduced_tree > " + input_+ "_check_output/checkManalyze.out 2>&1"
    subprocess.run(command, shell=True, check=True)

def checkM2csv(path):
    file = path + '/fasta_check_output/checkManalyze.out'
    with open (file,'r',encoding='utf-8') as f:
        lines=f.readlines()
        #获取非空行

    for i in range(len(lines)):
         # 选择以Bin Id开头的行以及后的行
        if lines[i].startswith('  Bin Id'):
            startlines=i
    strains=[]
    marker_lineage=[]
    completeness=[]
    contamination=[]
    heterogeneity=[]
    
    for line in lines[startlines+2:-3]:
        strains.append(line.split()[0])
        marker_lineage.append(line.split()[1])
        completeness.append(line.split()[12])
        contamination.append(line.split()[13])
        heterogeneity.append(line.split()[14])

    df=pd.DataFrame({'strains':strains,'marker_lineage':marker_lineage,'completeness':completeness,'contamination':contamination,'heterogeneity':heterogeneity})
    # 指定complete、contamination和heterogeneity列为float类型
    df[['completeness','contamination','heterogeneity']]=df[['completeness','contamination','heterogeneity']].astype(float)
    df.to_csv(file.split('.')[0]+'.csv',index=False)
    return df

def contamination_evaluation(path,completeness=95,contamination=15,contigs=1000,N50=5000):
    df=checkM2csv(path)
    print('The number of total strains is: ',len(df))

    # 选择completeness大于95且 contamination小于15的菌株,保存为非污染菌株
    df1=df[df['completeness']>=95]
    df1=df1[df1['contamination']<=15]
    print('The number of uncontaminated strains is: ',len(df1))
    df1.to_csv(path +'/fasta_check_output/checkm_uncontaminated.csv',index=False)
 
    # 选择completeness小于95或contamination小于15的菌株，保存为污染菌株
    df2=df[df['completeness']<95]
    df3=df[df['contamination']>15]
    df4=pd.concat([df2,df3])
    print('The number of contaminated strains is: ',len(df4))
    df4.to_csv(path +'/fasta_check_output/checkm_contaminated.csv',index=False)

    # 选择completeness大于95、contamination小于15，且contigs小于1000且N50大于5000的菌株
    ids = df1['strains'].tolist()
    genbank_list=[]
    for i in ids:
        genbank_list.append(i.split('.')[0])

    df_checkm_output=pd.read_csv(path +'/fasta_check_output/storage/bin_stats.analyze.tsv', sep='\t',header=None)

    id_list=df_checkm_output[0].tolist()

    genome_size_list=[]
    picked_id_list=[]
    # get the second column
    id_list2=df_checkm_output[1].tolist()
    for i in range(len(id_list2)):
        N50=int(id_list2[i].split("'N50 (contigs)': ",1)[1].split(', ',1)[0])
        contigs=int(id_list2[i].split("'# contigs': ",1)[1].split(', ',1)[0])
        genome_size=int(id_list2[i].split("'Genome size': ",1)[1].split(', ',1)[0])
        if contigs < 1000 and N50 > 5000:
                if id_list[i].split('.')[0] in genbank_list:
                    picked_id_list.append(id_list[i].split('.')[0])
                    genome_size_list.append(genome_size)
    # save the list to csv file
    df_filtered=pd.DataFrame({'id':picked_id_list,'genome_size':genome_size_list})
    df_filtered.to_csv(path+"/fasta_check_output/filtered_genomes.csv",index=False)

    # 挑选出不合格菌株
    if 'fasta_contaminated' not in os.listdir(path):
        os.mkdir(path + '/fasta_contaminated')   
    fasta_files=os.listdir(os.path.join(path,'fasta'))
    for file in fasta_files:
        if file.split('.')[0] not in picked_id_list:
            os.rename(path+'/fasta/'+file,path+'/fasta_contaminated/'+file)

def checkM_evaluation_workflow(path,cpus,completeness=95,contamination=15,contigs=1000,N50=5000):
    checkManalyze(path,cpus)
    contamination_evaluation(path,completeness,contamination,contigs,N50)
    print('CheckM analysis is Done!')

if __name__ == "__main__":
    file = r'/home/xyy/kita'
    checkM_evaluation_work(file)
    
   



    
    