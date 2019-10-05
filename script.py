import os
import argparse
import re
from Bio import Entrez

def apps(name):
       cmd = f'bwa mem ./fasta/influensa_hemmaglutinin.fasta ./fastq/{name}.fastq | samtools view -S -b | samtools sort > ./bam/{name}.bam'
       os.system(cmd)
       cmd = f'samtools index ./bam/{name}.bam'
       os.system(cmd)
       cmd = f'samtools mpileup -f ./fasta/influensa_hemmaglutinin.fasta ./bam/{name}.bam | varscan mpileup2snp --min-var-freq 0.001 --variants --output-vcf1 > {name}_varscan_results.vcf'
       os.system(cmd)    


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
  with open('result_fastq.txt', 'r') as r:
     links=r.readlines()
  for i in range(len(links)-2):
       name = re.search('\w{3}\d{7}', links[i]).group() 
       print(name)
       #cmd = f'wget -P fastq {links[i]}'
       #os.system(cmd)
       #cmd = f'gunzip ./fastq/{name}.fastq.gz'
       #os.system(cmd)
       #apps(name)
  
if __name__=='__main__':
   main()
