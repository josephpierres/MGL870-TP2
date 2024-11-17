# MGL870 - TP2 - Utilisation de l’apprentissage machine pour la détection des anomalies
## Pierre Joseph, Jonathan Mésidor, Mohamed Fehd Soufi
## Automne 2024


# Installation of the requirements
```bash
pip install requirements.txt
```

# Download logfiles
The following code will automatically download the **HDFS_v1** and **BGL** zip log files from https://github.com/logpai/loghub.
```bash
python download_logfiles.py
```
Moreoever, it prepares the folder structure as :
```bash
.
├── input
│   ├── HDFS_v1
│   └── BGL
├── HDFS_results
└── BGL_results
```
The zip log files will be downloaded and unzipped in `input/HDFS_v1` and `input/BGL` respectively.


# HDFS_v1
+ `MGL870-TP2-HDFS.ipynb`
+ `MGL870-TP2-HDFS-AIOps.ipynb`


# BGL
+ `MGL870-TP2-BGL.ipynb`
+ `MGL870-TP2-BGL-AIOps.ipynb`
  

# References
+ Adam J. Oliner, Jon Stearley. [What Supercomputers Say: A Study of Five System Logs](https://ieeexplore.ieee.org/document/4273008), in Proc. of IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2007.
+ Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. [Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics](https://arxiv.org/abs/2008.06448). IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.
+ Pinjia He, Jieming Zhu, Zibin Zheng, Michael R. Lyu. Drain: [An Online Log Parsing Approach with Fixed Depth Tree](https://ieeexplore.ieee.org/document/8029742/). IEEE International Conference on Web Services (ICWS), 2017.
+ Wei Xu, Ling Huang, Armando Fox, David Patterson, Michael Jordan. [Detecting Large-Scale System Problems by Mining Console Logs](https://people.eecs.berkeley.edu/~jordan/papers/xu-etal-sosp09.pdf), in Proc. of the 22nd ACM Symposium on Operating Systems Principles (SOSP), 2009.