#!/usr/bin/sh
# Note, despite the date in the filename (20101123), the last modified
# timestamp on the 1000G site for this download was 10/12/12 1:28:00 PM 
#wget ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/phase1/analysis_results/integrated_call_sets/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz \
#-O ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.2012Oct12.vcf.gz

#wget ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/phase1/analysis_results/integrated_call_sets/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz.tbi -O ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.2012Oct12.vcf.gz.tbi

# 1000g phase 3 data
#wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.autosomes.phase3_shapeit2_mvncall_integrated_v5.20130502.sites.vcf.gz
#wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.autosomes.phase3_shapeit2_mvncall_integrated_v5.20130502.sites.vcf.gz.tbi


#vt decompose -s ALL.autosomes.phase3_shapeit2_mvncall_integrated_v5.20130502.sites.vcf.gz \
#	| vt normalize -r /data/human/b37/human_g1k_v37_decoy.fasta - | bgzip -c > ALL.autosomes.phase3_shapeit2_mvncall_integrated_v5.20130502.sites.tidy.vcf.gz
#tabix ALL.autosomes.phase3_shapeit2_mvncall_integrated_v5.20130502.sites.tidy.vcf.gz


# gemini version 0.16.2
wget -O - ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5a.20130502.sites.vcf.gz \
	| vt decompose -s - | vt normalize -r /data/human/b37/human_g1k_v37_decoy.fasta -w 500000 - \
	| bgzip -c > ALL.wgs.phase3_shapeit2_mvncall_integrated_v5a.20130502.sites.tidy.vcf.gz
#tabix ALL.wgs.phase3_shapeit2_mvncall_integrated_v5a.20130502.sites.tidy.vcf.gz
