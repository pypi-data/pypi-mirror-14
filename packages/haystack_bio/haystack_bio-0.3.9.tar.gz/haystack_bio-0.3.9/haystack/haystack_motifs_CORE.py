#python modules
import multiprocessing
import subprocess as sb
import os
import sys
import random
import datetime
import argparse
import logging
import ntpath
import shutil
from collections import defaultdict
import codecs
import platform
import pickle as cp
import re

#commmon functions
from haystack_common import determine_path,query_yes_no,which,logging,error,warn,debug,info,check_file,CURRENT_PLATFORM,HAYSTACK_VERSION,system_env

#dependencies
from bioutilities import Genome_2bit, Coordinate, Sequence, Fimo
import numpy as np
np.seterr(divide='ignore')
np.seterr(invalid='ignore')
from scipy import stats
from scipy.misc import factorial
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as pl
pl.rc('font', **{'size'   : 18})
from jinja2 import Environment, FileSystemLoader

#external
from external import estimate_qvalues,generate_weblogo


####SUPPORT CLASSES AND FUNCTIONS#################################################################


def smooth(x,window_len=200,window='hanning'):
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')
    y=np.convolve(w/w.sum(),s,mode='valid')
    return y[window_len/2:-window_len/2+1]

def generate_motif_profile(profile_target,profile_bg,motif_id,output_filename,smooth_size=200,window_size=5000):
    s_smoothed=smooth(profile_target,smooth_size) 
    #bg_mean=profile_bg.mean()
    #fc_s_bg=s_smoothed/bg_mean

    #
    bg_smoothed=smooth(profile_bg,smooth_size)
    fc_s_bg=(s_smoothed+0.1)/(bg_smoothed+0.1)
    
    #
    fig=pl.figure(figsize=(9, 8))
    ax = fig.add_subplot(111)
    ax.plot(range(-window_size/2,window_size/2),fc_s_bg,'-g',linewidth=3)
    ax.hold(True)
    ax.plot([-window_size/2, window_size/2],[1,1],'--k')
    pl.title(motif_id)
    pl.xlabel('bp')
    pl.ylabel('Fold change')
    fig.savefig(output_filename)
    fig.savefig(output_filename.replace('.png','.pdf'))
    pl.close()




def combine_pvalues(x):
    #k=x.prod()
    k= np.exp(np.log(x).sum())
    p=0
    for i in range(len(x)):	
        p+=np.power(-np.log(k),i)/factorial(i)

    #print k --i
    #print p
    return k*p


def sample_wr(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result


class constant_missing_dict (dict):
    def __missing__ (self, key):
        return 0

def pickable_defaultdict(t=list):
    return defaultdict(t)

def calculate_average_ngram_presence(coordinates,genome,ngram):
    ngram_presence=np.zeros(len(coordinates))
    ngram_reversed=Sequence.reverse_complement(ngram)
    for idx,c in enumerate(coordinates):
        seq=genome.extract_sequence(c)
        ngram_presence[idx]=(seq.count(ngram)+seq.count(ngram_reversed))/float(len(c))

    return ngram_presence

def get_random_coordinates(coords,genome):
    random_coords=[]
    for c in coords:
        random_bpstart=np.random.randint(1,genome.chr_len[c.chr_id]-len(c)+1)
        random_coords.append(Coordinate(c.chr_id,random_bpstart,random_bpstart+len(c)-1))
    return random_coords

# CLASS TO DEFINE THE FIMO CONSUMER
class FimoSequencesConsumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means we should exit
                #print '%s: Exiting' % proc_name
                break
            #print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.result_queue.put(answer)
        return

# CLASS FOR THE FIMO TASK
class FimoOnSingleSequence(object):
    def __init__(self, seq, fimo_instance,idx_seq):
        self.seq = seq
        self.fimo = fimo_instance
        self.idx_seq=idx_seq
    def __call__(self):
        #print 'Running Fimo on',str(self.idx_seq)
        return self.idx_seq,self.fimo.extract_motifs(self.seq, report_mode='full')
    def __str__(self):
        return 'Fimo Instance on:'+str(self.idx_seq)


def ParallelFimoScanning(target_coords,meme_motifs_filename,genome,nucleotide_bg_filename,temp_directory='/tmp',p_value=1e-4,num_consumers=multiprocessing.cpu_count(),mask_repetitive=False,window_length=None,internal_window_length=None):
    # Establish communication queues
    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()
    
    # Start consumers
    debug('Creating %d fimo consumers' % num_consumers)
    consumers = [ FimoSequencesConsumer(tasks, results)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()


    #Initialize Fimo
    info('Initiliaze Fimo and load motifs')
    fimo=Fimo(meme_motifs_filename,nucleotide_bg_filename,temp_directory=temp_directory,p_value=p_value)

    #print 'DEBUG:',target_coords[0],len(target_coords[0])
    original_target_coords=target_coords
    
    if window_length:
        internal_bpstart=window_length/2-internal_window_length/2
        internal_bpend=window_length/2+internal_window_length/2
        #print 'DEBUG:',target_coords[0],window_length,internal_window_length,internal_bpstart,internal_bpend
        original_target_coords=target_coords
        target_coords=Coordinate.coordinates_of_intervals_around_center(target_coords,window_length)
        #print 'DEBUG:',target_coords[0],len(target_coords[0])
        
    
    # Enqueue jobs
    num_jobs = len(target_coords)
    for idx,c in enumerate(target_coords):
        seq=genome.extract_sequence(c,mask_repetitive=mask_repetitive)
        tasks.put(FimoOnSingleSequence(seq, fimo,idx))
    
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)

    motifs_profiles_in_sequences=dict()
    idxs_seqs_with_motif=dict()
    motif_coords_in_seqs_with_motif=dict()
    
    for motif_id in fimo.motif_ids:
        motifs_profiles_in_sequences[motif_id]=np.zeros(len(c))
        idxs_seqs_with_motif[motif_id]=set()
        motif_coords_in_seqs_with_motif[motif_id]=pickable_defaultdict()

    motifs_in_sequences_matrix=np.zeros((len(target_coords),len(fimo.motif_ids)))

    # Build the final matrix
    for idx in xrange(len(target_coords)):
        idx_seq,row= results.get()
        motif_in_center=set()
        for motif in row:
            
            try:
                motifs_profiles_in_sequences[motif['id']][motif['start']:motif['end']]+=1.0
                
                if motif['start']>=internal_bpstart and motif['end']<=internal_bpend: #keep track only if is in the internal window!
                    idxs_seqs_with_motif[motif['id']].add(idx_seq)
                    motifs_in_sequences_matrix[idx_seq,fimo.motif_id_to_index[motif['id']]]=+1
                    motif_in_center.add(motif['id'])
    
                    motif_coords_in_seqs_with_motif[motif['id']][original_target_coords[idx_seq]].append((int(motif['start']+target_coords[idx_seq].bpstart-1),int(motif['end']+target_coords[idx_seq].bpstart-1) ))
            except:
                print motif['id'],motif['start'],motif['end']
            

    return motifs_in_sequences_matrix,motifs_profiles_in_sequences,idxs_seqs_with_motif,motif_coords_in_seqs_with_motif,fimo.motif_names, fimo.motif_ids

################################################################################

def main():

  
    print '\n[H A Y S T A C K   M O T I F S]'
    print('\n-MOTIF ENRICHMENT ANALYSIS- [Luca Pinello - lpinello@jimmy.harvard.edu]\n')
    print 'Version %s\n' % HAYSTACK_VERSION
    
    bootstrap=False
    ngram_correction='g'

    #mandatory
    parser = argparse.ArgumentParser(description='HAYSTACK Parameters')
    parser.add_argument('bed_target_filename', type=str,  help='A bed file containing the target coordinates on the genome of reference')
    parser.add_argument('genome_name', type=str,  help='Genome assembly to use from UCSC (for example hg19, mm9, etc.)')

    #optional
    parser.add_argument('--bed_bg_filename', type=str,  help="A bed file containing the backround coordinates on the genome of reference (default random sampled regions from the genome)", default='random_background')
    parser.add_argument('--meme_motifs_filename', type=str, help='Motifs database in MEME format (default JASPAR CORE 2016)')
    parser.add_argument('--nucleotide_bg_filename',type=str, help='Nucleotide probability for the background in MEME format (default precomupted on the Genome)')
    parser.add_argument('--p_value', type=float, help='FIMO p-value for calling a motif hit significant (deafult: 1e-4)',default=1e-4)
    parser.add_argument('--no_c_g_correction',  help='Disable the matching of the C+G density of the background',action='store_true')
    parser.add_argument('--c_g_bins', type=int,help='Number of bins for the C+G density correction (default: 8)',default=8)
    parser.add_argument('--mask_repetitive', help='Mask repetitive sequences',action='store_true')
    parser.add_argument('--n_target_coordinates', type=int, help='Number of target coordinates to use (default: all)',default=np.inf)
    parser.add_argument('--use_entire_bg', help='Use the entire background file (use only when the cg correction is disabled)',action='store_true')   
    parser.add_argument('--bed_score_column', type=int, help='Column in the bedfile that represents the score (default: 5)',default=5)
    parser.add_argument('--bg_target_ratio', type=int, help='Background size/Target size ratio (default: 1.0)',default=2)
    parser.add_argument('--bootstrap',  help='Enable the bootstrap if the target set or the background set are too small, choices: True, False (default: False)',action='store_true')
    parser.add_argument('--temp_directory',  help='Directory to store temporary files  (default: /tmp)', default='/tmp')
    parser.add_argument('--no_random_sampling_target',  help='Select the best --n_target_coordinates using the score column from the target file instead of randomly select them',action='store_true')
    parser.add_argument('--name',  help='Define a custom output filename for the report', default='')
    parser.add_argument('--internal_window_length', type=int, help='Window length in bp for the enrichment (default: average lenght of the target sequences)')
    parser.add_argument('--window_length', type=int, help='Window length in bp for the profiler (default:internal_window_length*5)')
    parser.add_argument('--min_central_enrichment', type=float, help='Minimum central enrichment to report a motif (default:>1.0)',default=1.0)
    parser.add_argument('--disable_ratio',  help='Disable target/bg ratio filter',action='store_true')
    parser.add_argument('--dump', help='Dump all the intermediate data, choices: True, False (default: False)',action='store_true')
    parser.add_argument('--output_directory',type=str, help='Output directory (default: current directory)',default='')
    parser.add_argument('--smooth_size',type=int, help='Size in bp for the smoothing window (default: internal_window_length/4)')
    parser.add_argument('--gene_annotations_filename',type=str, help='Optional gene annotations file from the UCSC Genome Browser in bed format to map each region to its closes gene')
    parser.add_argument('--gene_ids_to_names_filename',type=str, help='Optional mapping file between gene ids to gene names (relevant only if --gene_annotation_filename is used)')
    parser.add_argument('--n_processes',type=int, help='Specify the number of processes to use. The default is #cores available.',default=multiprocessing.cpu_count())
    parser.add_argument('--version',help='Print version and exit.',action='version', version='Version %s' % HAYSTACK_VERSION)

    args = parser.parse_args()

    args_dict=vars(args)
    for key,value in args_dict.items():
        if key=='n_target_coordinates':
            n_target_coordinates=value
        else:
            exec('%s=%s' %(key,repr(value)))

    
    bed_score_column-=1

    if no_c_g_correction:
        c_g_correction=False
    else:
        c_g_correction=True

    if no_random_sampling_target:
        random_sampling_target=False
    else:
        random_sampling_target=True
        

    check_file(bed_target_filename)

    if not  bed_bg_filename == 'random_background':
        check_file(bed_bg_filename)


    if meme_motifs_filename:
        check_file(meme_motifs_filename)
    else:
        meme_motifs_filename=os.path.join(determine_path('motif_databases'),'JASPAR_CORE_2016_vertebrates.meme')
        
    annotation_directory=determine_path('gene_annotations')
    if gene_annotations_filename:

        if which('java') is None:
            error('The mapping to the closest gene requires Java free available from: http://java.com/en/download/')
            use_gene_annotations=False
        else:
            check_file(gene_annotations_filename) 
            info('Using %s as gene annotations file' % gene_annotations_filename)
            use_gene_annotations=True
    else:
            gene_annotations_filename=os.path.join(annotation_directory,'%s_genes.bed' % genome_name)
            gene_ids_to_names_filename=os.path.join(annotation_directory,'%s_genes_id_to_names' % genome_name)
            
            if os.path.exists(gene_annotations_filename) and os.path.exists(gene_ids_to_names_filename):
                use_gene_annotations=True
            else:
                use_gene_annotations=False
                info('No gene annotations file specified')


    target_name=ntpath.basename(bed_target_filename.replace('.bed',''))
    bg_name=ntpath.basename(bed_bg_filename.replace('.bed',''))
    #timestamp=(datetime.datetime.now().isoformat()[:-3].replace('T','(')+str(np.random.randint(10000))+')').replace(':','.')

    if name:
        directory_name='HAYSTACK_MOTIFS_on_'+name
    else:
        directory_name='HAYSTACK_on_'+target_name+'_VS_'+bg_name

    if output_directory:
        output_directory=os.path.join(output_directory, directory_name)
    else:
        output_directory=directory_name


    info('###PARAMETERS USED###\n\t\t -TARGET: %s \n\t\t -BACKGROUND: %s \n\t\t -BG_TARGET_RATIO: %s\n\t\t -C+G CORRECTION: %s\n\t\t -MASKING REPETITIVE: %s\n\t\t -COORDINATES TO ANALYZE: %s\n\t\t -OUTPUT DIRECTORY: %s\n'\
         %(bed_target_filename,bed_bg_filename,str(bg_target_ratio),str(c_g_correction),str(mask_repetitive),'ALL' if np.isinf(n_target_coordinates) else str(n_target_coordinates),output_directory))

    info('Initializing Genome:%s' %genome_name)

    genome_directory=determine_path('genomes')
    genome_2bit=os.path.join(genome_directory,genome_name+'.2bit')

    if os.path.exists(genome_2bit):
        genome=Genome_2bit(genome_2bit)
    else:
        info("\nIt seems you don't have the required genome file.")
        if query_yes_no('Should I download it for you?'):
            sb.call('haystack_download_genome %s' %genome_name,shell=True,env=system_env)
            if os.path.exists(genome_2bit):
                info('Genome correctly downloaded!')
                genome=Genome_2bit(genome_2bit)
            else:
                error('Sorry I cannot download the required file for you. Check your Internet connection.')
                sys.exit(1)
        else:
            error('Sorry I need the genome file to perform the analysis. Exiting...')
            sys.exit(1)

    if not nucleotide_bg_filename:
        nucleotide_bg_filename=os.path.join(genome_directory,genome_name+'_meme_bg')

    check_file(nucleotide_bg_filename)
        


    N_TARGET=None
    N_BG=None
    COMMAND_USED=' '.join(sys.argv)

    _n_target_coordinates=n_target_coordinates


    info('Loading Target coordinates from bed:%s' % bed_target_filename)
    target_coords=Coordinate.bed_to_coordinates(bed_target_filename,cl_score=bed_score_column)

    if len(target_coords) == 0:
    	info('No coordinates to analyze in your input file. Exiting.')
    	sys.exit(1)

    #calculate automatically the average lenght of the target regions


    if internal_window_length:
        info('Using the user defined internal window length:%d' % internal_window_length )
        if internal_window_length % 2:
            internal_window_length+=1
            
    else:
                        
        internal_window_length=int(np.mean(map(len,target_coords)))
        if internal_window_length % 2:
            internal_window_length+=1
        info('Using the average length of target coordinates as internal window length:%d' % internal_window_length )

        if not window_length:
            window_length=internal_window_length*5

    info('Total window length:%d' % window_length ) 

        

    if not smooth_size:
        smooth_size=internal_window_length/5

    target_coords=Coordinate.coordinates_of_intervals_around_center(target_coords,internal_window_length)
        

    if len(target_coords)>n_target_coordinates:
        if random_sampling_target:
            info('Sampling %d coordinates among the %d total' %( n_target_coordinates,len(target_coords)))
            target_coords=random.sample(target_coords,n_target_coordinates)
        else:
            info('Selecting the best %d coordinates among the %d total' %( n_target_coordinates,len(target_coords)))
            sorted_idxs_by_score=np.argsort([c.score for c in target_coords])[::-1]
            target_coords=[target_coords[idx] for idx in sorted_idxs_by_score[:n_target_coordinates]]
    else:
        
        if random_sampling_target and bootstrap and not np.isinf(n_target_coordinates):
            warn('Number of target regions < %d' % n_target_coordinates)
            info('bootstrapping to obtain enough target regions')
            target_coords=sample_wr(target_coords,n_target_coordinates)
        else:
            info('Using all the %d target coordinates' % len(target_coords))
            

    info('Extracting Motifs in target coordinates')
    positive_matrix,motifs_profiles_in_sequences, idxs_seqs_with_motif,motif_coords_in_seqs_with_motif,motif_names,motif_ids=ParallelFimoScanning(target_coords,
                                                                                                                                                  meme_motifs_filename,
                                                                                                                                                  genome,nucleotide_bg_filename,
                                                                                                                                                  temp_directory=temp_directory,
                                                                                                                                                  p_value=p_value,
                                                                                                                                                  mask_repetitive=mask_repetitive,
                                                                                                                                                  window_length=window_length,
                                                                                                                                                  internal_window_length=internal_window_length,
                                                                                                                                                  num_consumers=n_processes)
    n_target_coordinates=len(target_coords) #fix for the bootstrap!




    if bed_bg_filename == 'random_background':
        info('Extracting Random Coordinates from the genome...')

        if c_g_correction:
            info('Calculating the C+G content of the target coordinates')
            bg_coords=[]
            c_g_content_target=calculate_average_ngram_presence(target_coords,genome,ngram_correction)

            info('Extract a Matching C+G Background')
            bins=np.hstack((np.linspace(0,1,c_g_bins),np.inf))

            for _ in range(bg_target_ratio):
                for idx_c,c in enumerate(target_coords):
                    c_bin=np.nonzero(np.histogram(c_g_content_target[idx_c],bins)[0])[0][0]
                    c_random_bin=-1
                    
                    while c_random_bin != c_bin:
                        random_bpstart=np.random.randint(1,genome.chr_len[c.chr_id]-len(c)+1)
                        c_random=Coordinate(c.chr_id,random_bpstart,random_bpstart+len(c)-1)
                        seq=genome.extract_sequence(c_random)
                        c_g_content_c_random=(seq.count('c')+seq.count('g'))/float(len(c))
                        c_random_bin=np.nonzero(np.histogram(c_g_content_c_random,bins)[0])[0][0]

                    #print bg_target_ratio,c_bin,c_random_bin, ' still to match:',len(target_coords)-idx_c
                    bg_coords.append(c_random)

            c_g_content_bg=calculate_average_ngram_presence(bg_coords,genome,ngram_correction)
            bg_hist=np.histogram(c_g_content_bg,bins)[0]
            debug('original: '+str(np.histogram(c_g_content_target,bins)[0]))
            debug('obtained:'+str(np.histogram(c_g_content_bg,bins)[0]))

        else:
            bg_coords=get_random_coordinates(target_coords,genome)
        
        info('Done!')
       
    else:
        info('Loading Background Coordinates from:%s' % bed_bg_filename)
        bg_coords=Coordinate.bed_to_coordinates(bed_bg_filename)
        bg_coords=Coordinate.coordinates_of_intervals_around_center(bg_coords,internal_window_length)

        if use_entire_bg:
            bg_target_ratio=float(len(bg_coords))/n_target_coordinates
            info('Using all the coordinates in the BG, BG/TG:%f', bg_target_ratio)

        
        if c_g_correction:
            info('Calculating the C+G content')
            c_g_content_target=calculate_average_ngram_presence(target_coords,genome,ngram_correction)   
            c_g_content_bg=calculate_average_ngram_presence(bg_coords,genome,ngram_correction)

            info('Extract a Matching C+G Background')
            bins=np.hstack((np.linspace(0,1,c_g_bins),np.inf))
            target_hist=np.histogram(c_g_content_target,bins)[0]
            bg_hist=np.histogram(c_g_content_bg,bins)[0]
            ratios=bg_hist/(target_hist*1.0);
            debug('original:%s' %target_hist)
            debug('bg:%s' %bg_hist)
            debug('ratios:%s' %ratios)
            K_MATCH=min(bg_target_ratio,ratios[~np.isnan(ratios) & ~np.isinf(ratios) & (ratios>0) &(target_hist/float(target_hist.sum())>0.05)].min())

            debug('K_MATCH:%d' %K_MATCH)

            to_match=np.int32(np.floor(K_MATCH*target_hist))

            debug('to_match:%s' %to_match)
            
            idxs_corrected_bg=np.array([],dtype=int)

            for idx_bin in range(len(bins)-1):
                idxs_matching_regions=np.nonzero((c_g_content_bg>=bins[idx_bin]) & (c_g_content_bg<bins[idx_bin+1]))[0]
                to_take=np.random.permutation(len(idxs_matching_regions))
                to_take=to_take[range(min(len(idxs_matching_regions),to_match[idx_bin]))]
                idxs_corrected_bg= np.hstack((idxs_corrected_bg,idxs_matching_regions[to_take]))  

            debug('original:%s' %target_hist)
            debug('K:%d' %K_MATCH)
            debug('to sample:%s' %to_match) 
            debug( 'obtained:%s' % np.histogram(c_g_content_bg[idxs_corrected_bg],bins)[0] )
            bg_coords=[bg_coords[idx] for idx in idxs_corrected_bg]
            c_g_content_bg=calculate_average_ngram_presence(bg_coords,genome,ngram_correction)
            debug(np.histogram(c_g_content_bg,bins)[0])
            if np.array_equal(K_MATCH*target_hist,np.histogram(c_g_content_bg,bins)[0]):
                info('C+G content perfectly matched!\n\ttarget:%s\n\tbg    :%s' % (target_hist,np.histogram(c_g_content_bg,bins)[0]))
            else:
                warn('C+G content not perfectly matched\n\ttarget:%s\n\tbg    :%s'%(target_hist,np.histogram(c_g_content_bg,bins)[0]))

            debug(target_hist/np.histogram(c_g_content_bg,bins)[0])


    if len(bg_coords)>=bg_target_ratio*n_target_coordinates:
        bg_coords=random.sample(bg_coords,int(bg_target_ratio*n_target_coordinates))
    else:
        if bootstrap and len(bg_coords)<(bg_target_ratio*n_target_coordinates*0.95): #allow a small tollerance!
            info('bootstrapping to obtain enough background regions')
            bg_coords=sample_wr(bg_coords,int(bg_target_ratio*n_target_coordinates))
            c_g_content_bg=calculate_average_ngram_presence(bg_coords,genome,ngram_correction)
            debug('After bootstrap:\n\ttarget:%s\n\tbg    :%s' % (target_hist,np.histogram(c_g_content_bg,bins)[0]))

    info('Extracting Motifs in background coordinates')
    negative_matrix,motifs_profiles_in_bg,idxs_seqs_with_motif_bg=ParallelFimoScanning(bg_coords,
                                                                                       meme_motifs_filename,
                                                                                       genome,nucleotide_bg_filename,
                                                                                       temp_directory=temp_directory,
                                                                                       p_value=p_value,
                                                                                       mask_repetitive=mask_repetitive,
                                                                                       window_length=window_length,
                                                                                       internal_window_length=internal_window_length,
                                                                                       num_consumers=n_processes)[0:3]

    #allocate date for reports
    N_MOTIFS=len(motif_ids)
    rankings=np.zeros(N_MOTIFS,dtype=np.int16)
    motif_ratios=np.zeros(N_MOTIFS)
    support_p=np.zeros(N_MOTIFS)
    support_n=np.zeros(N_MOTIFS)
    fisher_p_values=np.zeros(N_MOTIFS)
    central_enrichment=np.zeros(N_MOTIFS)

    N_seq_p=positive_matrix.shape[0]
    N_seq_n=negative_matrix.shape[0]

    profile_presence_p=(positive_matrix>0).sum(0)
    profile_presence_n=(negative_matrix>0).sum(0)

    support_p=profile_presence_p/float(N_seq_p)
    support_n=profile_presence_n/float(N_seq_n)

    internal_bpstart=window_length/2-internal_window_length/2
    internal_bpend=window_length/2+internal_window_length/2

    for idx,motif_id in enumerate(motif_ids):
        fisher_p_values[idx]= stats.fisher_exact([[ profile_presence_p[idx], N_seq_p-profile_presence_p[idx]], [ profile_presence_n[idx], N_seq_n-profile_presence_n[idx]]])[1]
        central_enrichment[idx]=motifs_profiles_in_sequences[motif_id][internal_bpstart:internal_bpend].mean()/ np.hstack([motifs_profiles_in_sequences[motif_id][:internal_bpstart],motifs_profiles_in_sequences[motif_id][internal_bpend:]]).mean()
        
    motif_ratios=(support_p+0.01)/(support_n+0.01)

    #Foundamental!
    if not disable_ratio:
        motif_ratios[support_p<0.03]=1
    
    rankings=stats.rankdata(-motif_ratios)


    #filter here positive or positive and negative#################################
    if not disable_ratio:
        idxs_to_keep=np.nonzero(motif_ratios>1)[0]
    else:
        idxs_to_keep=range(len(motif_ratios))
        

    rankings=rankings[idxs_to_keep]
    motif_ratios=motif_ratios[idxs_to_keep]
    support_p=support_p[idxs_to_keep]
    support_n=support_n[idxs_to_keep]
    fisher_p_values=fisher_p_values[idxs_to_keep]
    central_enrichment=central_enrichment[idxs_to_keep]

    motif_ids=[motif_ids[_] for _ in idxs_to_keep]
    motif_names=[motif_names[_] for _ in idxs_to_keep]
    motif_idxs=[_ for _ in idxs_to_keep]

    try:
        qvalues=estimate_qvalues(fisher_p_values); # we test the ones only with ratio >1
    except:
        print fisher_p_values

    #qvalues=estimate_qvalues(fisher_p_values,m=len(motif_ids))
    ################################################################################


    #generate reports in html
    info('Generating HTML report...')
    imgs_directory=os.path.join(output_directory,'images')
    genes_list_directory=os.path.join(output_directory,'genes_lists')
    motif_regions_directory=os.path.join(output_directory,'motifs_regions')

    #create folders
    if not os.path.exists(imgs_directory):
        os.makedirs(imgs_directory)
    if use_gene_annotations and not os.path.exists(genes_list_directory):
        os.makedirs(genes_list_directory)
    if not os.path.exists(motif_regions_directory):
        os.makedirs(motif_regions_directory)


    j2_env = Environment(loader=FileSystemLoader(determine_path('extra')+'/templates/'),trim_blocks=True)

    info('DIRECTORY:%s' % determine_path('extra')+'/templates/')
    template= j2_env.get_template('report_template.html')

    #copy haystack logo and bg
    shutil.copyfile(determine_path('extra')+'/templates/haystack_logo.png', os.path.join(imgs_directory,'haystack_logo.png'))
    shutil.copyfile(determine_path('extra')+'/templates/noise.png', os.path.join(imgs_directory,'noise.png'))

    motifs_dump=[]
    for i in np.argsort(rankings):
        if (support_p[i]>=0.03 or disable_ratio)  and fisher_p_values[i]<0.01  and  (motif_ratios[i]>1 or disable_ratio) and central_enrichment[i]>min_central_enrichment:
        #if (support_p[i]>=0.01 or  support_n[i]>=0.01) and fisher_p_values[i]<0.1 and  (central_enrichment[i]>1.1 or central_enrichment[i]<0.9) and  ( motif_ratios[i]>1.1 or motif_ratios[i]<0.9):
       
            info('Generating logo and profile for:'+motif_ids[i])
            
            #create motif logo
            img_logo=os.path.join(imgs_directory,'logo_'+motif_ids[i])
            generate_weblogo(motif_ids[i],meme_motifs_filename,img_logo,title=motif_ids[i],SEQLOGO=determine_path('extra')+'/seqlogo')
            generate_weblogo(motif_ids[i],meme_motifs_filename,img_logo,title=motif_ids[i],SEQLOGO=determine_path('extra')+'/seqlogo',file_format='pdf')
            #fix the weblogo prefix problem
            img_logo_url=os.path.join('images','logo_'+motif_ids[i]+'.png')
            
            #create motif enrichment profile
            img_profile=os.path.join(imgs_directory,'profile_'+motif_ids[i]+'.png')
            motif_profile_target=motifs_profiles_in_sequences[motif_ids[i]]/N_seq_p
            motif_profile_bg=motifs_profiles_in_bg[motif_ids[i]]/N_seq_n

            #print motif_profile_target.shape, motif_profile_bg.shape
            generate_motif_profile(motif_profile_target,motif_profile_bg,motif_ids[i],img_profile,smooth_size=smooth_size,window_size=window_length)
            img_profile_url=os.path.join('images','profile_'+motif_ids[i]+'.png')
            
            #create regions
            info('Extracting regions with:'+motif_ids[i])
            regions=os.path.join(motif_regions_directory,motif_ids[i]+'_motif_region_in_target.bed')
            with open(regions,'w+') as outfile:
                outfile.write('Chromosome\tStart\tEnd\tMotif hits inside region\tNumber of hits\n')
                for c,locations in motif_coords_in_seqs_with_motif[motif_ids[i]].items():
                    outfile.write('\t'.join([c.chr_id,str(c.bpstart),str(c.bpend),';'.join(['-'.join(map(str,map(int,l))) for l in locations]),str(len(locations))])+'\n')
            regions_url=os.path.join('motifs_regions',motif_ids[i]+'_motif_region_in_target.bed')
            
            #map closest downstream genes
            genes_url=None
            if use_gene_annotations:
                info('Mapping regions with:%s to the clostest genes' % motif_ids[i])

                peak_annotator_path=os.path.join(determine_path('extra/'),'PeakAnnotator.jar')
                    
                if gene_ids_to_names_filename:
                    sb.call('java -jar '+peak_annotator_path+' -u TSS -p %s -a %s -s %s -o %s &> %s' \
                            %(regions,gene_annotations_filename,gene_ids_to_names_filename,genes_list_directory,os.path.join(genes_list_directory,'log_peakannotator.txt')),  shell=True,env=system_env)
                else:
                    sb.call('java -jar '+peak_annotator_path+' -u TSS -p %s -a %s  -o %s &> %s' \
                            %(regions,gene_annotations_filename,genes_list_directory,os.path.join(genes_list_directory,'log_peakannotator.txt')),  shell=True,env=system_env)

                
                genes_url=os.path.join('genes_lists',motif_ids[i]+'_motif_region_in_target.tss.bed')
                                
                
            motifs_dump.append({'id':motif_ids[i],'name':motif_names[i],'support_p':support_p[i]*100,
                                 'support_n':support_n[i]*100, 'ratio':motif_ratios[i],'rank':float(rankings[i]),
                                 'pvalue':fisher_p_values[i],'qvalue':qvalues[i],'central_enrichment':central_enrichment[i],
                                 'img_logo':img_logo_url,'img_profile':img_profile_url,'regions':regions_url,'genes':genes_url,'idx_motif':motif_idxs[i]})


    outfile= codecs.open(os.path.join(output_directory,"Haystack_report.html"), "w", "utf-8")
    outfile.write(template.render(motifs_dump=motifs_dump,bed_target_filename=bed_target_filename,bed_bg_filename=bed_bg_filename, N_TARGET=N_seq_p, N_BG=N_seq_n,\
                                  meme_motifs_filename=meme_motifs_filename, COMMAND_USED=COMMAND_USED,use_gene_annotations=use_gene_annotations))
    outfile.close()    

    if dump:
        info('Saving all the intermediate data on: %s ...' % output_directory)
        dump_directory=os.path.join(output_directory,'dump')
        
        if not os.path.exists(dump_directory):
            os.makedirs(dump_directory)
            
        np.save(os.path.join(dump_directory,'matrix_'+target_name),positive_matrix)
        np.save(os.path.join(dump_directory,'matrix_BG_'+target_name),negative_matrix)
        
        cp.dump(motifs_dump,open(os.path.join(dump_directory,target_name+'_motif_dumps.pickle'),'w'))

        #cp.dump( motifs_profiles_in_sequences,open( os.path.join(dump_directory,target_name+'_profiles.pickle'),'w'))
        #cp.dump( motifs_profiles_in_bg,open( os.path.join(dump_directory,bg_name+'_profiles.pickle'),'w'))

        cp.dump(idxs_seqs_with_motif,open(os.path.join(dump_directory,target_name+'_motif_seqs_idxs.pickle'),'w'))
        cp.dump(idxs_seqs_with_motif_bg,open(os.path.join(dump_directory,bg_name+'_motif_seqs_idxs.pickle'),'w'))

        cp.dump(motif_coords_in_seqs_with_motif,open(os.path.join(dump_directory,target_name+'_motif_coords_in_seqs_with_motif.pickle'),'w'))

        Coordinate.coordinates_to_bed(target_coords,os.path.join(dump_directory,'Target_coordinates_selected_on_'+target_name+'.bed'),minimal_format=False)
        Coordinate.coordinates_to_bed(bg_coords,os.path.join(dump_directory,'BG_coordinates_selected_on_'+ bg_name+'.bed'),minimal_format=True)

    info('All done! Ciao!')
    sys.exit(0)

