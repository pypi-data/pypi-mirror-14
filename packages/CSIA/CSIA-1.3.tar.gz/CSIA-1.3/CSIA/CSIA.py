##----INTRO-----------##
Tool = 'CSIA'
Versi = '1.0'
Author = 'Yingxiang Li'
Email = 'xlccalyx@gmail.com'
Date = 'Apr 02, 2016'
UpdateDate = '04032016'
Home = 'www.calyx.biz'
FullName = 'CRISPR Sequence Indel Analysis'
Aim = 'This program is for analysis of indel of CRISPR sequence.'

##----START-----------##
import argparse, time, sys, os, commands
from argparse import RawTextHelpFormatter

##----PREPARE---------##
Parse = argparse.ArgumentParser(description = '\tTool:   ' + Tool + 'v' + Versi + '\n\tDate:   ' + Date + '\n\tAuthor: ' + Author + ' (' + Email + ')' + '\n\tHome:   ' + Home + '\n\tMust-install:\n\t        bwa: 0.7.5a; fastqc: v0.11.2; samtools: 0.1.19; java: 1.7.0_95', formatter_class=RawTextHelpFormatter)

Parse.add_argument('-R', '--reference', help = "reference direction, fasta format. (eg: my_ref.fa)", required = True)
Parse.add_argument('-D', '--data', help = "one sample's sequenced fastq folder, ONLY fastq in. one file for single end, two files for paired end. (eg: my_data/)", required = True)
Parse.add_argument('-O', '--output', help = "output folder for all result and recording. if not exists, will be created. (eg: my_output/)", required = True)

Parse.add_argument('-N', '--name', help = "sample name, default is name of output folder. (eg: my_sample)")
Parse.add_argument('-P', '--pvalue', help = "minimal p value of indels, default: 0.05.", default = '0.05')
Parse.add_argument('-B', '--basequality', help = "minimal base quality, default: 30.", default = '30')
Parse.add_argument('-V', '--varfreq', help = "minimal indel frequency, default: 0.0001.", default = '0.0001')
Parse.add_argument('-F', '--fastqc', help = "run fastqc to process quality control, default activated. -F will disable.", action = "store_false", default = True)
Parse.add_argument('-U', '--unlimited', help = "read depth is unlimited when checking indels, default: disable.", action = "store_true")
Parse.add_argument('-E', '--readcount', help = "collect read counts of sequence, default: disable.", action = "store_true")
Parse.add_argument('-C', '--consensus', help = "return consensus turn, default: disable.", action = "store_true")
Parse.add_argument('-S', '--snp', help = "look for SNP, default: disable.", action = "store_true")

Args = Parse.parse_args()

Refer_D = Args.reference
Data_F = Args.data
Outpu_F = Args.output

Name = Args.name
PValue = Args.pvalue
BaseQuali = Args.basequality
VarFreq = Args.varfreq
FastQC = Args.fastqc
Unlim = Args.unlimited
ReadCount = Args.readcount
Conse = Args.consensus
Snp = Args.snp

##----MAIN------------##
#-Basic----#
print '\n\t' + '-'*42
print '\t|Tool:\t' + Tool + 'v' + Versi
print '\t|Author:\t' + Author + '(xlccalyx@gmail.com)'
print '\t|<BEGIN@'+ time.strftime("%Y-%m-%d %X", time.localtime())+ '>'

#-Function-#
#--common--
def fun_MakeDir(Path_):
	Path_ = Path_.strip().rstrip("\\")
	if not os.path.exists(Path_):
		os.makedirs(Path_)
	return Path_

def fun_Write(File_, File_D_):
	Out_ = open(File_D_, 'w')
	Out_.writelines(File_)
	Out_.close()

def fun_BashOrder(Log_F_, OrderName_, Order_):
	Bash_D_ = fun_MakeDir(Log_F_) + OrderName_ + '.sh'
	Bash_O_ = 'bash ' + Bash_D_ + ' > ' + Log_F_ + OrderName_ + '.log 2>&1'
	fun_Write(Order_, Bash_D_)
	os.system(Bash_O_)

def fun_PrintTime(FunctName_, Finis_ = 0):
	if Finis_ == 0:
		print FunctName_ + '  running@' + time.strftime("%Y-%m-%d %X", time.localtime())
	else:
		print FunctName_ + ' finished@' + time.strftime("%Y-%m-%d %X", time.localtime())

#--special-
#--bwa: index--
def Fun_BwaIndex(Log_F_, Refer_D_):
	fun_PrintTime('bwa index')
	BwaIndex_O_ = 'bwa index -a bwtsw ' + Refer_D_
	ReferName_ = os.path.basename(os.path.splitext(Refer_D_)[0])
	fun_BashOrder(Log_F_, 'Bwa_Index.' + ReferName_, BwaIndex_O_)
	fun_PrintTime('bwa index', 1)

#--FastQC: quality control--
def Fun_FastQC(Outpu_F_, Log_F_, Fastq1_D_, Fastq2_D_, FastQC_):
	if FastQC_:	
		fun_PrintTime('fastqc')
		FastQC_O_ = 'fastqc -q --extract -o ' + fun_MakeDir(Outpu_F_ + 'FastQC/') + ' ' + Fastq1_D_ + ' ' + Fastq2_D_
		fun_BashOrder(Log_F_, 'FastQC_QualiyControl', FastQC_O_)
		fun_PrintTime('fastqc', 1)

#--bwa: map--
def Fun_BwaMap(Outpu_F_, Log_F_, Fastq1_D_, Fastq2_D_, Name_, Refer_D_):
	fun_PrintTime('bwa map')
	SinglOrPair_ = ['Pa', 'Si'][Fastq2_D_ == '']
	BwaMap_D_ = fun_MakeDir(Outpu_F + 'Bwa/') + Name_ + '.sam'
	BwaMap_O_ = '''bwa mem -t 10 -R "@RG\\tID:''' + Name_ + '.BwaMap_' + SinglOrPair_ + '''\\tLB:bwa\\tPL:NA\\tSM:''' + Name_ + '" ' + Refer_D_ + ' '+ Fastq1_D_ + ' ' + Fastq2_D_ + ' > '+ BwaMap_D_
	fun_BashOrder(Log_F_, 'Bwa_Map', BwaMap_O_)	
	fun_PrintTime('bwa map', 1)
	
#--samtools: sam to bam--
def Fun_SamToolsSamToBam(Outpu_F_, Log_F_, Name_):
	fun_PrintTime('samtools sam to bam')
	BwaMap_D_ = Outpu_F + 'Bwa/' + Name_ + '.sam'
	Bam_D_ = fun_MakeDir(Outpu_F_ + 'SamTools/') + Name_ + '.bam'
	SamToolsSamToBam_O_ = 'samtools view -bhS ' + BwaMap_D_ + ' -o ' + Bam_D_
	fun_BashOrder(Log_F_, 'SamTools_SamToBam', SamToolsSamToBam_O_)
	fun_PrintTime('samtools sam to bam', 1)

#--samtools: sort--
def Fun_SamToolsSort(Outpu_F_, Log_F_, Name_):
	fun_PrintTime('samtools sort')
	Bam_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.bam'
	BamSortName_ = Outpu_F_ + 'SamTools/' + Name_ + '.Sort'
	SamToolsSort_O_ = 'samtools sort ' + Bam_D_ + ' ' + BamSortName_
	fun_BashOrder(Log_F_, 'SamTools_Sort', SamToolsSort_O_)
	fun_PrintTime('samtools sort', 1)

#--samtools: index--
def Fun_SamToolsIndex(Outpu_F_, Log_F_, Name_):
	fun_PrintTime('samtools index')
	BamSort_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.Sort.bam'
	SamToolsIndex_O_ = 'samtools index ' + BamSort_D_
	fun_BashOrder(Log_F_, 'SamTools_Index', SamToolsIndex_O_)
	fun_PrintTime('samtools index', 1)

#--samtools: multi pile up--
def Fun_SamToolsMultiPileUp(Outpu_F_, Log_F_, Name_, Refer_D_, Unlim_):
	fun_PrintTime('samtools mpileup')
	BamSort_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.Sort.bam'
	MultiPileUp_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.mpu'
	SamToolsMultiPileUp_O_ = 'SamTools mpileup' + ['', ' -d10000000'][Unlim_] + ' -f ' + Refer_D_ + ' ' + BamSort_D_ + ' > ' + MultiPileUp_D_
	fun_BashOrder(Log_F_, 'SamTools_MultiplePileUp', SamToolsMultiPileUp_O_)
	fun_PrintTime('samtools mpileup', 1)

#--varscan: indel--
def Fun_VarScanIndel(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, VarFreq_, PValue_):
	fun_PrintTime('varscan indel')
	MultiPileUp_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.mpu'
	VarScanIndel_D_ = fun_MakeDir(Outpu_F_, 'VarScan/') + Name_ + '.indel.tab'
	VarScanIndel_O_ = 'java -jar ' + VarScan_ + ' pileup2indel ' + MultiPileUp_D_ + ' --min-avg-qual ' + BaseQuali_  + ' --min-var-freq ' + VarFreq_+ ' --p-value ' + PValue_ + ' > ' + VarScanIndel_D_
	fun_BashOrder(Log_F_, 'VarScan_Indel', VarScanIndel_O_)
	fun_PrintTime('varscan indel', 1)

#--varscan2: read count--
def Fun_VarScanReadCount(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, ReadCount_):
	if ReadCount_:
		fun_PrintTime('varscan2 read count')
		MultiPileUp_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.mpu'
		VarScanReadCount_D_ = Outpu_F_, 'VarScan/' + Name_ + '.read.tab'
		VarScanReadCount_O_ = 'java -jar ' + VarScan_ + ' readcounts ' + MultiPileUp_D_ +  ' --min-avg-qual ' + BaseQuali_ + ' > ' + VarScanReadCount_D_
		fun_BashOrder(Log_F_, 'VarScan_ReadCount', VarScanReadCount_O_)
		fun_PrintTime('varscan2 read count', 1)

#--varscan: consensus call--
def Fun_VarScanConseCall(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, PValue_, Conse_):
	if Conse_:
		fun_PrintTime('varscan2 consensus call')
		MultiPileUp_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.mpu'
		VarScanConsenCall_D_ = Outpu_F_, 'VarScan/' + Name_ + '.consensus.tab'
		VarScanConsenCall_O_ = 'java -jar ' + VarScan_ + ' pileup2cns ' + MultiPileUp_D_ +  ' --min-avg-qual ' + BaseQuali_ + ' --p-value ' + PValue_ + ' > ' + VarScanConsenCall_D_
		fun_BashOrder(Log_F_, 'VarScan_ConseCall', VarScanConsenCall_O_)
		fun_PrintTime('varscan2 consensus call', 1)

#--varscan: snp--
def Fun_VarScanSnp(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, VarFreq_, PValue_, Snp_):
	if Snp_:
		fun_PrintTime('varscan2 snp')
		MultiPileUp_D_ = Outpu_F_ + 'SamTools/' + Name_ + '.mpu'
		VarScanSnp_D_ = Outpu_F_, 'VarScan/' + Name_ + '.snp.tab'
		VarScanSnp_O_ = 'java -jar ' + VarScan_ + ' pileup2snp ' + MultiPileUp_D_ +  ' --min-avg-qual ' + BaseQuali_  + ' --min-var-freq ' + VarFreq_+ ' --p-value ' + PValue_ + ' > ' + VarScanSnp_D_
		fun_BashOrder(Log_F_, 'VarScan_Snp', VarScanSnp_O_)
		fun_PrintTime('varscan2 snp', 1)

#--main----
def FUN_MAIN(Refer_D_, Data_F_, Outpu_F_, Name_, PValue_, BaseQuali_, VarFreq_, FastQC_, Unlim_, ReadCount_, Conse_, Snp_):
	if not os.path.isfile(Refer_D_):
		print 'Reference doesn\'t exist!'
	elif len(os.listdir(Data_F_)) == 0:
		print 'Data doesn\' exist!'
	else:
		if Name_ == None:
			Name_ = os.path.basename(os.path.splitext(Outpu_F_)[0])
		Outpu_F_ = fun_MakeDir(Outpu_F_ + '/') 
		Log_F_ = fun_MakeDir(Outpu_F_ + '/Log/')
#		VarScan_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'VarScan/VarScan.v2.3.9.jar')
		VarScan_ = resource_filename('CSIA', 'VarScan.v2.3.9.jar')
#--bwa: index--
		Fun_BwaIndex(Log_F_, Refer_D_)
#--fastq files--
		Fastq1_D_ = Data_F_ + sorted(os.listdir(Data_F_))[0]
		Fastq2_D_ = '' if len(os.listdir(Data_F_)) <= 1 else Data_F_ + sorted(os.listdir(Data_F_))[1]
#--fastqc: quality control--
		Fun_FastQC(Outpu_F_, Log_F_, Fastq1_D_, Fastq2_D_, FastQC_)
#--bwa: map--
		Fun_BwaMap(Outpu_F_, Log_F_, Fastq1_D_, Fastq2_D_, Refer_D_, Name_)		
#--samtools: sam to bam--
		Fun_SamToolsSamToBam(Outpu_F_, Log_F_, Name_)
#--samtools: sort
		Fun_SamToolsSort(Outpu_F_, Log_F_, Name_)
#--samtools: index
		Fun_SamToolsIndex(Outpu_F_, Log_F_, Name_)
#--samtools: multi pile up--
		Fun_SamToolsMultiPileUp(Outpu_F_, Log_F_, Refer_D_, Name_, Unlim_)
#--varscan: indel
		Fun_VarScanIndel(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, VarFreq_, PValue_)
#--varscan: read count--
		Fun_VarScanReadCount(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, ReadCount_)
#--varscan: consensus call--
		Fun_VarScanConseCall(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, PValue_, Conse_)
#--varscan: snp--
		Fun_VarScanSnp(Outpu_F_, Log_F_, Name_, VarScan_, BaseQuali_, VarFreq_, PValue_, Snp_)

#-Process--#
if __name__ == '__main__':
    try:
        FUN_MAIN(Refer_D, Data_F, Outpu_F, Name, PValue, BaseQuali, VarFreq, FastQC, Unlim, ReadCount, Conse, Snp)
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted me! ;-) Bye!\n")
        sys.exit(0)	

##----CODA------------##
print '''\t|~~~~~~~~~~~~~www.calyx.biz~~~~~~~~~~~~~
\t|                 __.                   
\t|  ___.  ____.   |  |  __. __.__.   __. 
\t|_/ ___\ \__  \  |  | <   y  |\  \ /  / 
\t|\  c___  /  a \_|  l__\___  | >  x  <  
\t| \_____>(______/|____//_____|/__/ \__\\
\t|~~~~~~~~~~~~~www.calyx.biz~~~~~~~~~~~~~'''
print '\t|<END  @' + time.strftime("%Y-%m-%d %X", time.localtime()) + '>'
print '\t' + '-'*42 + '\n'

##----TEST------------##
