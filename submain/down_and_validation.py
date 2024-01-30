import os
import subprocess
import hashlib

# 下载链霉菌完成基因组
def download_complete_genomes(genus,path,format="fasta"):
    command = ["nohup", "ncbi-genome-download", "-s", "refseq", "--assembly-levels", "complete", "--formats", format, "-g", genus, "-o", path,"bacteria"]
    subprocess.run(command)

# 下载所有链霉菌基因组
def download_all_genomes(genus,path,format="fasta"):
    command = ["nohup", "ncbi-genome-download", "-s", "refseq", "--formats", format, "--genus", genus,'-o',path, "bacteria"]
    subprocess.run(command)

# 校验
def validate(path):
    # 获取所有以.gz结尾的文件的路径
    file_paths = [os.path.join(root, file) for root, dirs, files in os.walk(path +"/refseq/bacteria/") for file in files if file.endswith(".gz")]

    # 计算文件数量
    file_count = len(file_paths)

    # 获得MD5校验文件，文件名MD5SUMS
    md5 = [os.path.join(root, file) for root, dirs, files in os.walk(path +"/refseq/bacteria/") for file in files if file == "MD5SUMS"]

    # 统计校验通过的文件数量
    valid_count = 0
    for i in range(file_count):
        with open(md5[i], 'r') as f:
            if hashlib.md5(open(file_paths[i], 'rb').read()).hexdigest() in f.read():
                valid_count += 1

    print(f"Total files: {file_count}, Valid files: {valid_count}")

# 将所有GenBank文件放入GBKs文件夹中
def move_files(path):
    os.makedirs(path+"/fasta", exist_ok=True)
    command = "mv " + path + "/refseq/bacteria/*/*.gz " + path + "/fasta"
    print(command)

    subprocess.run(command, shell=True)

# 解压
def unzip_files(path):
    command = "gunzip " + path+"/fasta/*"
    print(command)
    subprocess.run(command, shell=True)

# 主函数
def download_all_genomes_workflow(genus,path,format="fasta"):
    download_all_genomes(format, genus,path)
    validate(path)
    move_files(path)
    unzip_files(path)
    print('All fasta files in ', genus, ' are downloaded and prepared.')

def download_complete_genomes_workflow(genus,path,format="fasta"):
    download_complete_genomes(format, genus,path)
    validate(path)
    move_files(path)
    unzip_files(path)
    print('Complete fasta files in ', genus, ' are downloaded and prepared.')

if __name__ == "__main__":
    download_complete_genomes_workflow("Kitasatospora", "test")