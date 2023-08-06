from future import print_function
import os
import pysam
import subprocess
import sys
import tempfile
import errno
import glob
import pandas
import numpy
import collections


def makeDir(path):
    try:
        os.mkdir(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def checkFile(fname):
    """file name if file exists, None otherwise"""
    if os.path.isfile(fname):
        return fname
    else:
        return None


def listFiles(pattern):
    l = glob.glob(pattern)
    if len(l) == 0:
        return None
    elif len(l) == 1:
        return l[0]
    else:
        return l
    

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def refAtPos(chrom, pos, genref='/mnt/xfs1/bioinfo/data/bcbio_nextgen/150607/genomes/Hsapiens/GRCh37/seq/GRCh37.fa'):
    ref_allel = pysam.faidx(genref, str(chrom)+':'+str(pos)+'-'+str(pos))[1].strip()
    return ref_allel


def df2sklearn(mydf, col_to_keep):
    if 'status' in mydf.columns:
        mydf['status01'] = 1
        mydf['status01'][mydf['status'] == 'N'] = 0
        col_to_keep += ['status01']
    col_to_keep = list(set(col_to_keep).intersection(set(mydf.columns)))
    print(col_to_keep)
    #res = mydf[col_to_keep]
    mydf[col_to_keep] = mydf[col_to_keep].astype(float)
    mydf = mydf.dropna(subset=col_to_keep)
    return mydf[col_to_keep] 


def varType(row):
    c1 = len(row['Ref']) == len(row['Alt'])
#    c2 = ',' in row['Ref']
#    c3 = ',' in row['Alt']
    if c1:
        return 'snp'
    else:
        return 'indel'


def runInShell(cmd, return_output=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        if return_output:
            return stdout
        else:
            return 0
    else:
        sys.stderr.write(stderr)
        return 1


def runBamReadcounts(vcffile, bamfile, output_dir,
                     genome_ref='/mnt/xfs1/bioinfo/data/bcbio_nextgen/150607/\
                     genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                     brc='/mnt/scratch/asalomatov/software/installs/\
                     bin/bam-readcount'):
    """exctract regions from vcf and supply them to bam-readcount"""
    makeDir(output_dir)
    if checkFile(vcffile) is None:
        sys.exit('No vcf file!')
    if checkFile(bamfile) is None:
        sys.exit('No bam file!')
    cat = 'cat '
    if os.path.splitext(vcffile)[1] == '.gz':
        cat = 'zcat '
    bam_name = os.path.splitext(os.path.basename(bamfile))[0]
    tmp_dir = tempfile.mkdtemp()    
    tmp_bed = tempfile.mktemp(dir=tmp_dir, suffix='.bed', prefix=bam_name+'_')    
    outp_fn = os.path.join(output_dir, bam_name+'.txt')    
    cmd1 = cat + vcffile + \
        " | grep -v ^# | awk \'{print $1\"\t\"$2\"\t\"$2}' > " + tmp_bed
    cmd2 = ' '.join([brc, '-f', genome_ref, bamfile, '-l',tmp_bed, \
            ' > '+outp_fn])
    cmd3 = ' '  # 'rm -rf '+tmp_dir
    cmd = ';'.join([cmd1, cmd2, cmd3])
    return runInShell(cmd)
    

def runBamReadcountsRegions(regionsfile,
                            bamfile,
                            output_file,
                            genome_ref='/mnt/xfs1/bioinfo/data/bcbio_nextgen/150607/genomes/Hsapiens/GRCh37/seq/GRCh37.fa',
                            brc='/mnt/scratch/asalomatov/software/installs/bin/bam-readcount'):
    """exctract features using bam-readcount"""
    if checkFile(regionsfile) is None:
        sys.exit('No regions file!')
    if checkFile(bamfile) is None:
        sys.exit('No bam file!')
    cmd = ' '.join([brc, '-f', genome_ref, bamfile, '-l', regionsfile,
                    ' > ' + output_file])
    return runInShell(cmd)
    

def readBamReadcount1(file_name, vartype):
    """Read bam-readcount output into pandas DF,
    vartype = ['SNP', 'INS', 'DEL', 'INDEL']
    """
    dir_name = os.path.dirname(file_name)
    tmp_file = file_name + '.' + vartype    
    if vartype == 'SNP':    
        cmd1 = 'cat ' + file_name + \
        " | grep -v + | grep -v - >" + tmp_file
    elif vartype == 'INS':    
        cmd1 = 'cat ' + file_name + \
        " | grep + >" + tmp_file
    elif vartype == 'DEL':    
        cmd1 = 'cat ' + file_name + \
        " | grep - >" + tmp_file
    elif vartype == 'INDEL':    
        cmd1 = 'cat ' + file_name + \
        " | grep -e '-\|+' >" + tmp_file
    else:
        sys.exit('unknown vartype...')
    runInShell(cmd1)
    if vartype == 'SNP':
        clm_names = ['CHROM', 'POS',
                'REF', 'DP', 'A', 'C', 'G', 'T']
        clm_dtypes = collections.OrderedDict()
        for i in clm_names:
            clm_dtypes[i] = str
        reader = pandas.read_csv(
            tmp_file,
            header=None,
            dtype=clm_dtypes,
            names=list(clm_names),
            usecols=[0,1,2,3,5,6,7,8],
            sep='\t')
        res = reader.apply(parseBamReadcount, axis=1)
        return reader[['CHROM', 'POS', 'REF', 'DP']].merge(res, left_index=True, right_index=True)


def readBamReadcount(file_name, n_clmns_per_allele=14):
    """Read bam-readcount output into pandas DF.
    """
    clm_names = ['CHROM', 'POS',
                 'REF', 'DP', 'ZERO', 'A', 'C', 'G', 'T', 'N', 'INDEL']
    clm_dtypes = collections.OrderedDict()
    for i in clm_names:
        clm_dtypes[i] = str
    reader = pandas.read_csv(
        file_name,
        header=None,
        dtype=clm_dtypes,
        names=list(clm_names),
        # usecols=[0, 1, 2, 3, 5, 6, 7, 8, 9, 10],
        sep='\t')
    reader['INDEL'][reader.INDEL.isnull()] = ':'.join(['0'] *
                                                      n_clmns_per_allele)
    reader.drop('ZERO', axis=1, inplace=True)
    # return reader
    res = reader.apply(parseBamReadcountIndel, axis=1)
    return reader[['CHROM', 'POS', 'REF', 'DP']].merge(res, left_index=True,
                                                       right_index=True)


def parseBamReadcount(row):
    # first split ref data
    ref_split = row[row['REF']].split(':')
    ref_split = ref_split[:1] + [float(x) for x in ref_split[1:]]
    # now arrgegate information for alt allels
    possib_alt = []
    if row['REF'] == 'A': possib_alt = ['C', 'G', 'T']
    if row['REF'] == 'C': possib_alt = ['A', 'G', 'T']
    if row['REF'] == 'G': possib_alt = ['A', 'C', 'T']
    if row['REF'] == 'T': possib_alt = ['A', 'C', 'G']
    num_allels = 0
    alt_read_count = 0
    cum_array = numpy.zeros(12)
    alts = []
    for i in possib_alt:
        if int(row[i][2]) > 0:
            num_allels += 1
            row_list = row[i].split(':')
            allel_count = float(row_list[1])
            alt_read_count += allel_count
            alts += row_list[:2]
            cum_array += allel_count * numpy.array(row_list[2:], dtype=float)
    if alt_read_count > 0:
        cum_array = cum_array / alt_read_count

    clmns_detail = ['base',
            'count',
            'avg_mapping_quality',
            'avg_base_quality',
            'avg_se_mapping_quality',
            'num_plus_strand',
            'num_minus_strand',
            'avg_pos_as_fraction',
            'avg_num_mismatches_as_fraction',
            'avg_sum_mismatch_qualities',
            'num_q2_containing_reads',
            'avg_dist_to_q2_start_in_q2_reads',
            'avg_clipped_length',
            'avg_dist_to_effective_3p_end']        
    res = pandas.Series(ref_split + [num_allels, '_'.join(alts), alt_read_count] +
            cum_array.tolist(),
            ['REF_'+ x for x in clmns_detail] + ['num_allels'] +
           ['ALT_'+ x for x in clmns_detail] )
    return res


def parseBamReadcountIndel(row):
    # first split ref data
    ref_split = row[row['REF']].split(':')
    ref_split = ref_split[:1] + [float(x) for x in ref_split[1:]]
    #  split indel data
    indel_split = row['INDEL'].split(':')
    indel_split = indel_split[:1] + [float(x) for x in indel_split[1:]]
    # now arrgegate information for alt allels
    possib_alt = []
    if row['REF'] == 'A': possib_alt = ['C', 'G', 'T']
    if row['REF'] == 'C': possib_alt = ['A', 'G', 'T']
    if row['REF'] == 'G': possib_alt = ['A', 'C', 'T']
    if row['REF'] == 'T': possib_alt = ['A', 'C', 'G']
    num_allels = 0
    alt_read_count = 0
    cum_array = numpy.zeros(12)
    alts = []
    for i in possib_alt:
        if int(row[i][2]) > 0:
            num_allels += 1
            row_list = row[i].split(':')
            allel_count = float(row_list[1])
            alt_read_count += allel_count
            alts += row_list[:2]
            cum_array += allel_count * numpy.array(row_list[2:], dtype=float)
    if alt_read_count > 0:
        cum_array = cum_array / alt_read_count

    clmns_detail = ['base',
                    'count',
                    'avg_mapping_quality',
                    'avg_base_quality',
                    'avg_se_mapping_quality',
                    'num_plus_strand',
                    'num_minus_strand',
                    'avg_pos_as_fraction',
                    'avg_num_mismatches_as_fraction',
                    'avg_sum_mismatch_qualities',
                    'num_q2_containing_reads',
                    'avg_dist_to_q2_start_in_q2_reads',
                    'avg_clipped_length',
                    'avg_dist_to_effective_3p_end']     
    res = pandas.Series(ref_split +
                        [num_allels, '_'.join(alts), alt_read_count] +
                        cum_array.tolist() +
                        indel_split,
                        ['REF_'+ x for x in clmns_detail] +
                        ['num_allels'] +
                        ['ALT_'+ x for x in clmns_detail] +
                        ['INDEL_'+ x for x in clmns_detail])
    return res


def addSuffix(x, sfx):
    return [i + sfx for i in x]


def splitVarId(x):
    res = x.split('_')
    return pandas.Series(res, ['ind_id', 'CHROM', 'POS'])


def splitAlleles(x):
    res = x.split('_')
    col_names = ['REF', 'ref_DP', 'ALT', 'alt_DP']
    if len(res) > 4:
        col_names += ['ALT1', 'alt1_DP']
    if len(res) == 8:
        col_names += ['ALT2', 'alt2_DP']
    DP = sum(map(int, res[1::2]))
    res += [DP]
    col_names += ['DP']
    return pandas.Series(res, col_names)


def mergeClmnsToInfo(df, clmn_list=[]):
    if len(clmn_list) == 0:
        clmn_list = df.columns
    x = None
    for i in clmn_list:
        df['col_i'] = i + '='
        if x is None:
            x = df['col_i'] + df[i].astype(str) + ';'
        else:
            x += df['col_i'] + df[i].astype(str) + ';'
    return x


def writePredAsVcf(pred_df, outp_file, min_DP=0):
    pred_df.reset_index(inplace=True, drop=True)
    res1 = pred_df.var_id.apply(splitVarId)
    res2 = pred_df.test_var_alleles.apply(splitAlleles)
    x = pred_df.merge(res1, left_index=True, right_index=True)
    x = x.merge(res2, left_index=True, right_index=True)
    print('shape all DP: %s' % x.shape)
    x = x[x['DP'] >= min_DP]
    print('shape DP >= %s' % min_DP)
    print(x.shape)
    required_fields = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER']
    for i in required_fields:
        if i not in x.columns:
            x[i] = '.'
    info_col = [i for i in x.columns if i not in required_fields]
    x['INFO'] = mergeClmnsToInfo(x, info_col)
    x[required_fields + ['INFO']].to_csv(outp_file, sep='\t', index=False,
                                         header=False)
    return 0


