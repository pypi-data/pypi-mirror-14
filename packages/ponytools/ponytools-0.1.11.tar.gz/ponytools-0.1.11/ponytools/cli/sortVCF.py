#!/usr/bin/env python3
import sys
from optparse import OptionParser


def log(message,*formatting):
    print(message.format(*formatting),file=sys.stderr)

def sortVCF(vcf_file,fasta_file,temp_dir="/tmp",out="sorted.vcf"):
    headers = list()
    variants = list()
    cur_byte = 0
    chroms = list() 
    temps  = dict()
    log("Sorting {}",vcf_file)
    # Get the chromosome order
    with open(fasta_file,'r') as FASTA:
        for line in FASTA:
            if line.startswith('>'):
                chrom,*info = line.strip().lstrip('>').split()
                log("Found chromosome {}",chrom)
                chroms.append(chrom)
                temps[chrom] = open(os.path.join(temp_dir,chrom+'.tmp'),'w')
    # Get headers and extract positions with file byte offsets
    log("Reading in VCF: {}",vcf_file)
    with open(vcf_file,'r') as VCF:
        for i,line in enumerate(VCF):
            line = line.strip()
            if line.startswith("#"):
                headers.append(line)
            else:
                chrom,pos,*junk = line.split()
                print(line,file=temps[chrom])
    # close all temp files
    for key,val in temps.items():
        log("Closing tmp file: {}",key)
        val.close()
    log("soring chroms")
    with open(out,'w') as OUT:
        # print headers
        print("\n".join(headers),file=OUT)
        for chrom in chroms:
            # read in that chroms bullshit
            with open(os.path.join(temp_dir,chrom+'.tmp'),'r') as CHROM:
                variants =  CHROM.readlines()
                # sort by position
                variants.sort(key=lambda x: int(x.split()[1]))
                log("printing chrom {}",chrom)
                print("".join(variants),file=OUT,end="")
                os.remove(os.path.join(temp_dir,chrom+'.tmp'))

def main(args):
    parser=OptionParser()
    parser.add_option('--vcf',help='unsorted VCF file')
    parser.add_option('--fasta',help='fasta file')
    parser.add_option('--out',default='sorted.vcf',help='output name [default: sorted.vcf]')

    options,args = parser.parse_args(args)
    
    sortVCF(options.vcf,options.fasta,out=options.out)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:])) 
