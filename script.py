import os
import argparse
import re
from Bio import Entrez
import pandas as pd
import statistics as st

def apps(name, deep):
       cmd = f'bwa mem ./fasta/influensa_hemmaglutinin.fasta ./fastq/{name}.fastq | samtools view -S -b - | samtools sort  -o ./bam/{name}_sorted.bam'
       os.system(cmd)
       cmd = f'samtools index ./bam/{name}_sorted.bam'
       os.system(cmd)
       cmd = f'samtools mpileup -d {deep} -f ./fasta/influensa_hemmaglutinin.fasta ./bam/{name}_sorted.bam | varscan mpileup2snp --min-var-freq 0.001 --variants --output-vcf 1 > {name}_varscan_results.vcf'
       os.system(cmd)

def snps(names):
    means = []
    sts =[]
    df = pd.read_csv('results_id.txt', sep = ' ', encoding='utf-8', dayfirst=True)
    df =df.replace('%','', regex=True)
    df =df.replace(',','.', regex=True)
    df['Freq']=df['Freq'].astype(float)
    for i in range (1,len(names)):
        l = df['Freq'][df.Assembly == f'{names[i]}']
        local_mean = st.mean(l)
        local_sd = st.stdev(l)
        means += [local_mean]
        sts += [local_sd]

    treshold = st.mean([means[x]+3*sts[x] for x in range(len(means))])
    SNPS = df[df.Freq > treshold][df.Assembly == f'{names[0]}']
    SNPS.to_csv('SNPS.csv')



def main():
  try:
    os.makedirs('bam')
  except:
    pass
  try:
    os.makedirs('fasta')
  except:
    pass


  seq= Entrez.efetch(db='nucleotide', id='KF848938.1', rettype='fasta', retmode='text')
  with open('./fasta/influensa_hemmaglutinin.fasta', 'w') as w:
      w.write(seq.read())
  cmd = 'bwa index ./fasta/influensa_hemmaglutinin.fasta'
  os.system(cmd)
  names = []
  st = []
  st1 = []
  with open('result_fastq.txt', 'r') as r:
     links=r.readlines()
  for i in range(len(links)-2):
       name = re.search('\w{3}\d{7}', links[i]).group() 
       cmd = f'wget -P fastq {links[i]}'
       os.system(cmd)
       cmd = f'gunzip ./fastq/{name}.fastq.gz'
       os.system(cmd)
       reads = sum(1 for line in open(f'./fastq/{name}.fastq'))/4
       with open(f'./fastq/{name}.fastq', 'r') as r:
            lines=r.readlines()
       av=max(len(lines[i].replace('\n','')) for i in range(1,len(lines),4))
       deep = int(reads*av/1665)
       print(deep)
       print(av)
       apps(name, deep)
       go = ' NR> 24 {print $1, $2, $4, $5, $10}'
       goo = f'cat {name}_varscan_results.vcf'
       cmd = f"{goo} | awk '{go}' >> results.txt"
       os.system(cmd)
       cmd = f"{goo} | awk '{go}' > res.txt"
       os.system(cmd)
       strings=sum(1 for line in open('res.txt'))
       names += [name for i in range(strings)]
  with open ('results.txt' , 'r') as f:
       lines =f.readlines()


  #str_ ='#CHROM POS REF ALT Sample1'
  #pattern = re.compile(re.escape(str_))
  #with open('results.txt','w') as f:
    # for i in range(len(lines)):
      #  result = pattern.search(lines[i])
       # if (result is None) or (i == 0):
           # f.write(lines[i])
       
  with open ('results.txt') as f, open ('results_id.txt', 'w') as f1:
        for x, y in enumerate(f):
            y=y.rstrip()
            id_ =names[x % len(names)]
            y += ' ' + id_
            f1.write(y + '\n')
  with open ('results_id.txt') as f:
        A=f.read()      
        A=A.replace(':',' ')   
  with open('results_id.txt','w') as f:
         f.write('CHROM POS ID REF ALT QUAL FILTER INFO V1 V2 Freq V1 V2 V3 V4 V5 V6 V7 Assembly\n')
         f.write(A)
  #print(A)
  os.remove('./results.txt')
  snps(names)
  
if __name__=='__main__':
   main()
