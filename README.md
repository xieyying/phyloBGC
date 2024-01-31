# phyloBGC

phyloBGC is a tool to generate Biosynthetic Gene Cluster (BGC) networking based on phylogenesis. It includes four main steps:

1. Download specific genus genomes from NCBI
2. Evaluate the contamination by checkM
3. Check the taxonomy using gtdbtk
4. Analyze the BGCs using antiSMASH
5. Generate BGC networking by BiGSCAPE

## Installation

Before using phyloBGC, you need to install it. Follow these steps:

1. Create a new conda environment with Python 3.8:

```bash
conda create -n phylo python=3.8
```
2. Download or clone the phyloBGC program.

3. Navigate to the directory where pyproject.toml is located in phyloBGC.

4. Install the program in editable mode:
```bash
pip install --editable .
```
5. Install other dependencies:

   - **CheckM**: Install using bioconda. Follow the instructions provided in the [CheckM Installation Guide](https://github.com/Ecogenomics/CheckM/wiki/Installation#how-to-install-checkm).

   - **GTDB-Tk 2.3.2**: Install using bioconda. Follow the instructions provided in the [GTDB-Tk Installation Guide](https://ecogenomics.github.io/GTDBTk/installing/index.html).

   - **antiSMASH**: Install using Docker (antiSMASH standalone). Follow the instructions provided in the [antiSMASH Installation Guide](https://docs.antismash.secondarymetabolites.org/install/).

   - **BiG-SCAPE**: Install using Docker. Follow the instructions provided in the [BiG-SCAPE Installation Guide](https://bigscape-corason.secondarymetabolites.org/installation/).

# Usage
There are two main ways to use phyloBGC: step by step or all in one.

Step by Step
Here is an example of how to use phyloBGC step by step:

```bash
conda activate phylo
phyloBGC download -g 'Kitasatospora' -p $direction -complete
phyloBGC check -g 'Kitasatospora' -p $direction
phyloBGC taxonomy -g 'Kitasatospora' -p /home/xyy/kita
phyloBGC antismash  -p $direction
phyloBGC antismash  -p $direction
phyloBGC bigscape  -p $direction
```

Note: You can add your own genome data in .fna format into the folder $direction/fasta to be analyzed together.

All in One
Alternatively, you can run all steps at once:

```bash 
phyloBGC all -g 'Kitasatospora' -p /home/xyy/kita_all -complete

```

This command will download complete genomes in the genus of Kitasatospora. If you want to download all genomes in the genus of Kitasatospora, you can use the following command:

```bash
phyloBGC all -g 'Kitasatospora' -p /home/xyy/kita_all

```

Contributing
If you have suggestions for how phyloBGC could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For more, check out the Contributing Guide.

License
MIT © Yunying Xie