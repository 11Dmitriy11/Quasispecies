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
  names = ['id']
  st = []
  st1 = []
  with open('result_fastq.txt', 'r') as r:
     links=r.readlines()
  for i in range(len(links)-2):
       name = re.search('\w{3}\d{7}', links[i]).group() 
       #cmd = f'wget -P fastq {links[i]}'
       #os.system(cmd)
       #cmd = f'gunzip ./fastq/{name}.fastq.gz'
       #os.system(cmd)
       #apps(name)
       go = '{print $1, $2, $3, $4, $5}'
       goo = f'cat {name}_varscan_results.vcf'
       cmd = f"{goo} | awk '{go}' >> results.txt"
       os.system(cmd)
       cmd = f"{goo} | awk '{go}' > res.txt"
       os.system(cmd)
       strings=sum(1 for line in open('res.txt'))
       names += [name for i in range(strings-1)]
  with open ('results.txt' , 'r') as f:
       lines =f.readlines()


  str_ ='Chrom Position Ref Var Cons:Cov:Reads1:Reads2:Freq:P-value'
  pattern = re.compile(re.escape(str_))
  with open('results.txt','w') as f:
     for i in range(len(lines)):
        result = pattern.search(lines[i])
        if (result is None) or (i == 0):
            f.write(lines[i])
       
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
         f.write(A)
  print(A)
  os.remove('./results.txt')
  
if __name__=='__main__':
   main()
