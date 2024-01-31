import os
import fnmatch
import subprocess
import pandas as pd

def not_edge_bgc(path):
    # get antiSMASH output GBK files
    files=os.walk(os.path.join(path,'antismash'))

    edge_cluster=[]
    not_edge_bgc_num=0
    not_edge_path=os.path.join(path,'antismash_not_edge_bgc')
    if not os.path.exists(not_edge_path):
        os.mkdir(not_edge_path)

    for dirpath, dirnames, filenames in os.walk(os.path.join(path,'antismash')):
        for f in filenames:
            if fnmatch.fnmatch(f, '*region*.gbk'):
                f=os.path.join(dirpath,f)
                with open(f,encoding="utf-8-sig") as f1:
                    lines=f1.readlines()
                    contig_edge_number=0
                    for line in lines:
                        if ('contig_edge="True"' in line):
                            contig_edge_number=+1

                    if contig_edge_number>=1:
                        # edge_cluster.append(True)
                        continue
                        
                    else:
                        # edge_cluster.append(False)
                        not_edge_bgc_num+=1
                        os.system("cp "+ f + " " + not_edge_path)
            else:
                continue
    print("The number of not edge BGCs is: ",not_edge_bgc_num)

def run_bigscape (path,mode='global'):
    
    input_ = os.path.join(path,'antismash_not_edge_bgc')
    output = os.path.join(path,'antismash_not_edge_bgc_bigscape')
    command = ['nohup run_bigscape ' + input_ + ' ' + output + '_' +mode +  ' --cutoffs 0.3 0.4 0.5 0.6 0.7  --clan_cutoff 0.5 0.8 --mix --no_classify --include_singletons --mode global --mibig']
    subprocess.run(command, shell=True, check=True)

def treeTospecies(path):
    file = path+'/fasta_classify_wf/align/output.tree-taxonomy'
    # 读取文件
    with open(file, 'r') as f:
        lines = f.readlines()

    user_id=[]
    species=[]
    for line in lines:
        if line.startswith('GCF'):
            name=line.split('\t')[0]
            id=name.split('.')[0]+'.'+name.split('.')[1].split('_')[0]
        else:
            id=line.split('\t')[0]
        user_id.append(id)

        strain=line.split('\t')[1].split(';')[-1].split('\n')[0].split(' s__')[-1]
        # species.append(strain)
        if strain=='':
            species.append('S. sp '+id.split('.')[0])
            
        else:
            species.append(strain)
    return user_id,species

def extract_strains(Network_Annotations_Full):
    
    df = pd.read_csv(Network_Annotations_Full, sep='\t', header=0)
    strains = []
    ID = df['Accesion ID'].tolist()
    for id in ID:
        id = id.split('_N')[0]
        strains.append(id)
    return strains


def speciesToGCF(path,mode='global'):

    files = os.walk(os.path.join(path, 'antismash_not_edge_bgc_bigscape_' + mode, 'network_files'))
    
    for dirpath, dirnames, filenames in files:
        for f in filenames:
            if fnmatch.fnmatch(f, 'Network_Annotations_Full.tsv'):
                file = os.path.join(dirpath,f)
                df = pd.read_csv(file, sep='\t', header=0)
                strains = extract_strains(file)
                strains_to_species = dict(zip(treeTospecies(path)[0], treeTospecies(path)[1]))

                # 使用列表推导进行匹配
                species = [strains_to_species.get(s, None) for s in strains]
                df['species'] = species
                df['strains'] = strains
                df.to_csv(file.rsplit('.')[0]+'_add_species.csv', index=False)

            # 删除不相关的known BGC
            if fnmatch.fnmatch(f, 'mix_clustering_c*.tsv'):
                file1 = os.path.join(dirpath,f)
                df_network = pd.read_csv(file1, sep='\t', header=0)
                # 获取#BGC Name列中不是以BGC开头的数据
                df_network1 = df_network[~df_network['#BGC Name'].str.contains('BGC')]
                Family_Number = df_network1['Family Number'].tolist()

                #获取df_network中family number在Family_Number中的数据
                df_network2 = df_network[df_network['Family Number'].isin(Family_Number)]
                df_network2.to_csv(file1,sep='\t',index=False)

                BGC_names = df_network2['#BGC Name'].tolist()

                files_ = os.walk(os.path.join(path, 'antismash_not_edge_bgc_bigscape_' + mode, 'network_files'))
                for dirpath_, dirnames_, filenames_ in files_:
                    for f_ in filenames_:
                        if fnmatch.fnmatch(f_, '*.network'):
                            if f_.split('_c')[1].split('.network')[0] == f.split('clustering_c')[1].split('.tsv')[0]:
                                print(f_)
                                df_net = pd.read_csv(os.path.join(dirpath_,f_), sep='\t', header=0)
                                df_net = df_net[df_net['Clustername 1'].isin(BGC_names)]
                                # 将df_net存为os.path.join(dirpath_,f_，并覆盖原来的文件
                                df_net.to_csv(os.path.join(dirpath_,f_), sep='\t',index=False)
    print('Species to GCF is done!')

# 主函数
def run_bigscape_workflow(path,mode='global'):
    not_edge_bgc(path)
    run_bigscape(path,mode)
    speciesToGCF(path,mode)
    print('Bigscape analysis is done!')

if __name__ == "__main__":
    directory = r'/home/xyy/test'
    # not_edge_bgc(directory)
    # run_bigscape(directory)
    # directory = r'C:\Users\xyy\Desktop\python\phyloBGC'
    speciesToGCF(directory)

