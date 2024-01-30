import os
import glob
import subprocess
import time

def rename_contigs(directory):
    # Get all files in the specified directory
    files = glob.glob(os.path.join(directory, "fasta", "*"))

    for file_path in files:
        print(file_path)
        # Create new name by taking the first 15 characters of the original name and adding .format
        format = file_path.split('.')[-1]
        print(format)
        new_name = os.path.join(directory,'fasta',os.path.basename(file_path)[0:15] + "."+format)
        print(new_name)
        os.rename(file_path, new_name)

        
        # Get the base name of the file
        file_name = os.path.basename(new_name)

        # Count the number of lines starting with ">", and replace ">" with ">filename"
        with open(new_name) as file:
            lines = file.readlines()

        count = 1
        with open(new_name, "w") as file:
            for line in lines:
                if line.startswith(">"):
                    # Replace ">" with ">filename_N<count>"
                    line = line.replace(">", ">" + file_name.rsplit('.',1)[0] + "_N" + str(count) + " ")
                    line = line.split(' ')[0] + '\n'
                    count += 1
                    print(line)
                file.write(line)

    print("Total number of files: ", len(files))
    print("Renaming contigs is done!")

def run_antismash(path):
    # Get all files not directions in the specified directory
    files = [file for file in os.listdir(os.path.join(path,'fasta')) if not os.path.isdir(file)]
    if 'antismash' not in os.listdir(path):
        os.mkdir(path + '/antismash')


    for i, file_name in enumerate(files, start=1):
        print(f"Running {file_name} ... ({i} of {len(files)})")
        start_time = time.time()
        input_ = os.path.join(path,'fasta',file_name)
        output = os.path.join(path,'antismash',file_name.replace('.fna', ''))

        # Construct the command
        command = ['nohup run_antismash '+ input_ +' '+ output + ' --fullhmmer --cb-general --cb-subclusters --cb-knownclusters --asf --pfam2go --tfbs --rre --genefinding-tool prodigal']

        # Run the command
        subprocess.run(command, shell=True, check=True)

        end_time = time.time()
        print(f"{file_name} has finished")
        print(f"Time taken: {end_time - start_time} seconds")
        print('antismash analysis is done!')
# 主函数
def run_antismash_workflow(path):
    rename_contigs(path)
    run_antismash(path)

if __name__ == '__main__':
    directory = r'/home/xyy/test'
    # rename_contigs(directory)
    run_antismash(directory)
