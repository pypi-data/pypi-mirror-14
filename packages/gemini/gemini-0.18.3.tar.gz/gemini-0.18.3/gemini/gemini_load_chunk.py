#!/usr/bin/env python

# native Python imports
import os.path
import re
import sys
import sqlite3
import numpy as np
import shutil
import uuid
import geneimpacts

# third-party imports
import cyvcf2 as vcf

# gemini modules
import version
from ped import load_ped_file
import gene_table
import infotag
import database
import annotations
import popgen
import structural_variants as svs
from gemini_constants import *
from compression import pack_blob
from gemini.config import read_gemini_config

class empty(object):
    def __getattr__(self, key):
        return None

empty = empty()

def get_phred_lik(gt_phred_likelihoods, dtype=np.int32, empty_val=-1):
    """
    Force each sample to have 3 GL's (0/0, 0/1, 1/1).
    If no samples have GL's, then we just return None to save space.
    """
    m = np.iinfo(dtype).max - 1
    out = []
    all_empty = True
    empty_line = [empty_val] * 3
    for row in gt_phred_likelihoods:
        # we only try to use the correct PL's if it already has size 3
        if row is not None and isinstance(row, (list, tuple)) and len(row) == 3:
            out.append([min(m, int(v)) if v is not None else empty_val for v in row])
            all_empty = False
        else:
            out.append(empty_line)
    if all_empty:
        return None
    return np.array(out, dtype=dtype)

def get_extra_effects_fields(args):
    """Retrieve additional effects fields contained in the VCF.

    Useful for merging VEP databases with additional fields.
    """
    loader = GeminiLoader(args, prepare_db=False)
    return [x[0] for x in loader._extra_effect_fields]

def load_clinvar(cpath):
    from cyvcf2 import VCF
    from collections import defaultdict

    lookup = {}
    for v in VCF(cpath):
        info = v.INFO
        gene = info.get('GENEINFO')
        if gene is None: continue
        diseases = [x for x in info.get('CLNDBN').split("|") if not x in (".", "not_specified", "not_provided")]
        if diseases == []: continue

        genes = [x.split(":")[0] for x in gene.split("|")]
        for gene in genes:
            key = v.CHROM, gene
            if key in lookup:
                lookup[key].extend(diseases)
            else:
                lookup[key] = diseases
    for k in lookup:
        lookup[k] = "|".join(sorted(set(lookup[k]))).lower()
    return lookup


class GeminiLoader(object):
    """
    Object for creating and populating a gemini
    database and auxillary data files.
    """
    def __init__(self, args, buffer_size=10000, prepare_db=True):
        self.args = args
        self.seen_multi = False

        # create the gemini database
        # create a reader for the VCF file
        self.vcf_reader = self._get_vcf_reader()
        # load sample information
        expected = "consequence,codons,amino_acids,gene,symbol,feature,exon,polyphen,sift,protein_position,biotype,warning".split(",")

        if self.args.anno_type == "VEP":
            self._effect_fields = self._get_vep_csq(self.vcf_reader)
            # tuples of (db_column, CSQ name)
            self._extra_effect_fields = [("vep_%s" % x.lower(), x) for x in self._effect_fields if not x.lower() in expected]

        else:
            self._effect_fields = []
            self._extra_effect_fields = []
        if not prepare_db:
            return
        self._create_db([x[0] for x  in self._extra_effect_fields])

        if not self.args.no_genotypes and not self.args.no_load_genotypes:
            # load the sample info from the VCF file.
            self._prepare_samples()
            # initialize genotype counts for each sample
            self._init_sample_gt_counts()
            self.num_samples = len(self.samples)
        else:
            self.num_samples = 0

        self.clinvar_chrom_gene_lookup = load_clinvar(annotations.get_anno_files(self.args)['clinvar'])

        self.buffer_size = buffer_size
        self._get_anno_version()

        if not args.skip_gene_tables:
            self._get_gene_detailed()
            self._get_gene_summary()

    def store_vcf_header(self):
        """Store the raw VCF header.
        """
        database.insert_vcf_header(self.c, self.vcf_reader.raw_header)

    def store_resources(self):
        """Create table of annotation resources used in this gemini database.
        """
        database.insert_resources(self.c, annotations.get_resources(self.args))

    def store_version(self):
        """Create table documenting which gemini version was used for this db.
        """
        database.insert_version(self.c, version.__version__)

    def _get_vid(self):
        if hasattr(self.args, 'offset'):
            v_id = int(self.args.offset)
        else:
            v_id = 1
        return v_id

    def _multiple_alts_message(self):
        self.seen_multi = 1
        sys.stderr.write("\n")
        sys.stderr.write("warning: variant with multiple alternate alleles found.\n")
        sys.stderr.write("         in order to reduce the number of false negatives\n")
        sys.stderr.write("         we recommend to split multiple alts. see: \
                http://gemini.readthedocs.org/en/latest/content/preprocessing.html#preprocess\n")

    def populate_from_vcf(self):
        """
        """

        self.v_id = self._get_vid()
        self.counter = 0
        self.var_buffer = []
        self.var_impacts_buffer = []
        self.skipped = 0
        # need to keep the objects in memory since we just borrow it in python.
        obj_buffer = []
        reader = self.vcf_reader

        anno_keys = {}
        if self.args.anno_type in ("snpEff", "all"):
            if "ANN" in reader:
                desc = reader["ANN"]["Description"]
                parts = [x.strip("\"'") for x in re.split("\s*\|\s*", desc.split(":", 1)[1].strip('" '))]
                anno_keys["ANN"] = parts
            elif "EFF" in reader:
                parts = [x.strip(" [])'(\"") for x in re.split("\||\(", reader["EFF"]["Description"].split(":", 1)[1].strip())]
                anno_keys["EFF"] = parts
            else:
                print "snpEff header not found"
        if self.args.anno_type in ("VEP", "all"):
            if "CSQ" in reader:
                parts = [x.strip(" [])'(\"") for x in re.split("\||\(",
                                                               reader["CSQ"]["Description"].split(":", 1)[1].strip())]
                anno_keys["CSQ"] = parts


        # process and load each variant in the VCF file
        for var in self.vcf_reader:
            if not var.ALT or len(var.ALT) == 0:
                continue
            if len(var.ALT) > 1 and not self.seen_multi:
                self._multiple_alts_message()

            if self.args.passonly and (var.FILTER is not None and var.FILTER != "."):
                self.skipped += 1
                continue
            (variant, variant_impacts, extra_fields) = self._prepare_variation(var, anno_keys)
            variant.extend(extra_fields.get(e[0]) for e in self._extra_effect_fields)
            obj_buffer.append(var)
            # add the core variant info to the variant buffer
            self.var_buffer.append(variant)
            # add each of the impact for this variant (1 per gene/transcript)
            for var_impact in variant_impacts:
                self.var_impacts_buffer.append(var_impact)

            # buffer full - time to insert into DB
            if len(self.var_buffer) >= self.buffer_size:
                sys.stderr.write("pid " + str(os.getpid()) + ": " +
                                 str(self.counter) + " variants processed.\n")
                database.insert_variation(self.c, self.var_buffer)
                database.insert_variation_impacts(self.c,
                                                  self.var_impacts_buffer)
                # binary.genotypes.append(var_buffer)
                # reset for the next batch
                obj_buffer = []
                self.var_buffer = []
                self.var_impacts_buffer = []
            self.v_id += 1
            self.counter += 1
        # final load to the database
        self.v_id -= 1
        database.insert_variation(self.c, self.var_buffer)
        database.insert_variation_impacts(self.c, self.var_impacts_buffer)
        sys.stderr.write("pid " + str(os.getpid()) + ": " +
                         str(self.counter) + " variants processed.\n")
        if self.args.passonly:
            sys.stderr.write("pid " + str(os.getpid()) + ": " +
                             str(self.skipped) + " skipped due to having the "
                             "FILTER field set.\n")

    def _update_extra_headers(self, headers, cur_fields):
        """Update header information for extra fields.
        """
        for field, val in cur_fields.items():
            headers[field] = self._get_field_type(val, headers.get(field, "integer"))
        return headers

    def _get_field_type(self, val, cur_type):
        start_checking = False
        for name, check_fn in [("integer", int), ("float", float), ("text", str)]:
            if name == cur_type:
                start_checking = True
            if start_checking:
                try:
                    check_fn(val)
                    break
                except:
                    continue
        return name

    def build_indices_and_disconnect(self):
        """
        Create the db table indices and close up
        db connection
        """
        # index our tables for speed
        database.create_indices(self.c)
        # commit data and close up
        database.close_and_commit(self.c, self.conn)

    def _get_vcf_reader(self):
        return vcf.VCFReader(self.args.vcf)

    def _get_anno_version(self):
        """
        Extract the snpEff or VEP version used to annotate the VCF
        """
        # default to unknown version
        self.args.version = None

        if self.args.anno_type == "snpEff":
            try:
                version_string = self.vcf_reader['SnpEffVersion']['SnpEffVersion']
            except KeyError:
                error = ("\nWARNING: VCF is not annotated with snpEff, check documentation at:\n"\
                "http://gemini.readthedocs.org/en/latest/content/functional_annotation.html#stepwise-installation-and-usage-of-snpeff\n")
                sys.exit(error)

            # e.g., "SnpEff 3.0a (build 2012-07-08), by Pablo Cingolani"
            # or "3.3c (build XXXX), by Pablo Cingolani"

            version_string = version_string.replace('"', '')  # No quotes
            toks = version_string.split()

            if "SnpEff" in toks[0]:
                self.args.raw_version = toks[1]  # SnpEff *version*, etc
            else:
                self.args.raw_version = toks[0]  # *version*, etc
            # e.g., 3.0a -> 3
            self.args.maj_version = int(self.args.raw_version.split('.')[0])

        elif self.args.anno_type == "VEP":
            pass

    def _get_vep_csq(self, reader):
        """
        Test whether the VCF header meets expectations for
        proper execution of VEP for use with Gemini.
        """
        required = ["Consequence"]
        expected = "Consequence|Codons|Amino_acids|Gene|SYMBOL|Feature|EXON|PolyPhen|SIFT|Protein_position|BIOTYPE".upper()
        try:
            parts = reader["CSQ"]["Description"].strip().replace('"', '').split("Format: ")[-1].split("|")
            all_found = True
            for check in required:
                if check not in parts:
                    all_found = False
                    break
            if all_found:
                return parts
        except KeyError:
            # Did not find expected fields
            pass
        error = "\nERROR: Check gemini docs for the recommended VCF annotation with VEP"\
                "\nhttp://gemini.readthedocs.org/en/latest/content/functional_annotation.html#stepwise-installation-and-usage-of-vep"
        sys.exit(error)

    def _create_db(self, effect_fields=None):
        """
        private method to open a new DB
        and create the gemini schema.
        """
        # open up a new database
        db_path = self.args.db if not hasattr(self.args, 'tmp_db') else self.args.tmp_db
        if os.path.exists(db_path):
            os.remove(db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.text_factory = str
        self.conn.isolation_level = None
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA synchronous = OFF')
        self.c.execute('PRAGMA journal_mode=MEMORY')
        # create the gemini database tables for the new DB
        database.create_tables(self.c, effect_fields or [])
        database.create_sample_table(self.c, self.args)

    def _prepare_variation(self, var, anno_keys):
        """private method to collect metrics for a single variant (var) in a VCF file.

        Extracts variant information, variant impacts and extra fields for annotation.
        """
        extra_fields = {}
        # these metric require that genotypes are present in the file
        call_rate = None
        hwe_p_value = None
        pi_hat = None
        inbreeding_coeff = None
        hom_ref = het = hom_alt = unknown = None

        # only compute certain metrics if genoypes are available
        if not self.args.no_genotypes and not self.args.no_load_genotypes:
            hom_ref = var.num_hom_ref
            hom_alt = var.num_hom_alt
            het = var.num_het
            unknown = var.num_unknown
            call_rate = var.call_rate
            aaf = var.aaf
            hwe_p_value, inbreeding_coeff = \
                popgen.get_hwe_likelihood(hom_ref, het, hom_alt, aaf)
            pi_hat = var.nucl_diversity
        else:
            aaf = infotag.extract_aaf(var)
            if not isinstance(aaf, (float, int)):
                if aaf is not None:
                    aaf = max(aaf)

        ############################################################
        # collect annotations from gemini's custom annotation files
        # but only if the size of the variant is <= 50kb
        ############################################################
        if var.end - var.POS < 50000:
            pfam_domain = annotations.get_pfamA_domains(var)
            cyto_band = annotations.get_cyto_info(var)
            rs_ids = annotations.get_dbsnp_info(var)
            clinvar_info = annotations.get_clinvar_info(var)
            in_dbsnp = 0 if rs_ids is None else 1
            rmsk_hits = annotations.get_rmsk_info(var)
            in_cpg = annotations.get_cpg_island_info(var)
            in_segdup = annotations.get_segdup_info(var)
            is_conserved = annotations.get_conservation_info(var)
            esp = annotations.get_esp_info(var)
            thousandG = annotations.get_1000G_info(var)
            recomb_rate = annotations.get_recomb_info(var)
            gms = annotations.get_gms(var)
            grc = annotations.get_grc(var)
            in_cse = annotations.get_cse(var)
            encode_tfbs = annotations.get_encode_tfbs(var)
            encode_dnaseI = annotations.get_encode_dnase_clusters(var)
            encode_cons_seg = annotations.get_encode_consensus_segs(var)
            gerp_el = annotations.get_gerp_elements(var)
            vista_enhancers = annotations.get_vista_enhancers(var)
            cosmic_ids = annotations.get_cosmic_info(var)
            fitcons = annotations.get_fitcons(var)
            Exac = annotations.get_exac_info(var)

            #load CADD scores by default
            if self.args.skip_cadd is False:
                (cadd_raw, cadd_scaled) = annotations.get_cadd_scores(var)
            else:
                (cadd_raw, cadd_scaled) = (None, None)

            # load the GERP score for this variant by default.
            gerp_bp = None
            if self.args.skip_gerp_bp is False:
                gerp_bp = annotations.get_gerp_bp(var)
        # the variant is too big to annotate
        else:
            pfam_domain = None
            cyto_band = None
            rs_ids = None
            clinvar_info = annotations.ClinVarInfo()
            in_dbsnp = None
            rmsk_hits = None
            in_cpg = None
            in_segdup = None
            is_conserved = None
            esp = annotations.ESPInfo(None, None, None, None, None)
            thousandG = annotations.ThousandGInfo(None, None, None, None, None, None, None)
            Exac = annotations.ExacInfo(None, None, None, None, None, None,
                    None, None, None, None, None, None, None)
            recomb_rate = None
            gms = annotations.GmsTechs(None, None, None)
            grc = None
            in_cse = None
            encode_tfbs = None
            encode_dnaseI = annotations.ENCODEDnaseIClusters(None, None)
            encode_cons_seg = annotations.ENCODESegInfo(None, None, None, None, None, None)
            gerp_el = None
            vista_enhancers = None
            cosmic_ids = None
            fitcons = None
            cadd_raw = None
            cadd_scaled = None
            gerp_bp = None

        top_impact = empty
        if anno_keys == {}:
            impacts = []
        else:

            impacts = []
            if self.args.anno_type in ("all", "snpEff"):
                try:
                    if "EFF" in anno_keys:
                        impacts += [geneimpacts.OldSnpEff(e, anno_keys["EFF"]) for e in var.INFO["EFF"].split(",")]
                    elif "ANN" in anno_keys:
                        impacts += [geneimpacts.SnpEff(e, anno_keys["ANN"]) for e in var.INFO["ANN"].split(",")]
                except KeyError:
                    pass

            if self.args.anno_type in ("all", "VEP"):
                try:
                    impacts += [geneimpacts.VEP(e, anno_keys["CSQ"]) for e in var.INFO["CSQ"].split(",")]
                except KeyError:
                    pass

            for i, im in enumerate(impacts, start=1):
                im.anno_id = i
            if impacts != []:
                top_impact = geneimpacts.Effect.top_severity(impacts)
                if isinstance(top_impact, list):
                    top_impact = top_impact[0]

        filter = None
        if var.FILTER is not None and var.FILTER != ".":
            if isinstance(var.FILTER, list):
                filter = ";".join(var.FILTER)
            else:
                filter = var.FILTER

        vcf_id = None
        if var.ID is not None and var.ID != ".":
            vcf_id = var.ID
        chrom = var.CHROM if var.CHROM.startswith("chr") else "chr" + var.CHROM

        clinvar_gene_phenotype = None
        if top_impact.gene is not None:
            clinvar_gene_phenotype = self.clinvar_chrom_gene_lookup.get((chrom[3:], top_impact.gene))

        # build up numpy arrays for the genotype information.
        # these arrays will be pickled-to-binary, compressed,
        # and loaded as BLOB values (see compression.pack_blob)
        gt_phred_ll_homref = gt_phred_ll_het = gt_phred_ll_homalt = None

        if not self.args.no_genotypes and not self.args.no_load_genotypes:
            gt_bases = var.gt_bases
            gt_types = var.gt_types
            gt_phases = var.gt_phases
            gt_depths = var.gt_depths
            gt_ref_depths = var.gt_ref_depths
            gt_alt_depths = var.gt_alt_depths
            gt_quals = var.gt_quals
            #gt_copy_numbers = np.array(var.gt_copy_numbers, np.float32)  # 1.0 2.0 2.1 -1
            gt_copy_numbers = None
            gt_phred_ll_homref = var.gt_phred_ll_homref
            gt_phred_ll_het = var.gt_phred_ll_het
            gt_phred_ll_homalt = var.gt_phred_ll_homalt
            # tally the genotypes
            self._update_sample_gt_counts(gt_types)
        else:
            gt_bases = gt_types = gt_phases = gt_depths = gt_ref_depths = None
            gt_alt_depths = gt_quals = gt_copy_numbers = None

        if self.args.skip_info_string:
            info = None
        else:
            info = dict(var.INFO)

        # were functional impacts predicted by SnpEFF or VEP?
        # if so, build up a row for each of the impacts / transcript
        variant_impacts = []
        for idx, impact in enumerate(impacts or [], start=1):
            var_impact = [self.v_id, idx, impact.gene,
                          impact.transcript, impact.is_exonic,
                          impact.is_coding,
                          impact.is_splicing,
                          impact.is_lof,
                          impact.exon, impact.codon_change,
                          impact.aa_change, impact.aa_length,
                          impact.biotype, impact.top_consequence,
                          impact.so, impact.effect_severity,
                          impact.polyphen_pred, impact.polyphen_score,
                          impact.sift_pred, impact.sift_score]
            variant_impacts.append(var_impact)

        # extract structural variants
        sv = svs.StructuralVariant(var)
        ci_left = sv.get_ci_left()
        ci_right = sv.get_ci_right()

        if top_impact is not empty:
            for dbkey, infokey in self._extra_effect_fields:
                extra_fields[dbkey] = top_impact.effects[infokey]

        # construct the core variant record.
        # 1 row per variant to VARIANTS table
        variant = [chrom, var.start, var.end,
                   vcf_id, self.v_id, top_impact.anno_id, var.REF, ','.join([x or "" for x in var.ALT]),
                   var.QUAL, filter, var.var_type,
                   var.var_subtype, pack_blob(gt_bases), pack_blob(gt_types),
                   pack_blob(gt_phases), pack_blob(gt_depths),
                   pack_blob(gt_ref_depths), pack_blob(gt_alt_depths),
                   pack_blob(gt_quals), pack_blob(gt_copy_numbers),
                   pack_blob(gt_phred_ll_homref),
                   pack_blob(gt_phred_ll_het),
                   pack_blob(gt_phred_ll_homalt),
                   call_rate, in_dbsnp,
                   rs_ids,
                   ci_left[0],
                   ci_left[1],
                   ci_right[0],
                   ci_right[1],
                   sv.get_length(),
                   sv.is_precise(),
                   sv.get_sv_tool(),
                   sv.get_evidence_type(),
                   sv.get_event_id(),
                   sv.get_mate_id(),
                   sv.get_strand(),
                   clinvar_info.clinvar_in_omim,
                   clinvar_info.clinvar_sig,
                   clinvar_info.clinvar_disease_name,
                   clinvar_info.clinvar_dbsource,
                   clinvar_info.clinvar_dbsource_id,
                   clinvar_info.clinvar_origin,
                   clinvar_info.clinvar_dsdb,
                   clinvar_info.clinvar_dsdbid,
                   clinvar_info.clinvar_disease_acc,
                   clinvar_info.clinvar_in_locus_spec_db,
                   clinvar_info.clinvar_on_diag_assay,
                   clinvar_info.clinvar_causal_allele,
                   clinvar_gene_phenotype,
                   annotations.get_geno2mp_ct(var),
                   pfam_domain, cyto_band, rmsk_hits, in_cpg,
                   in_segdup, is_conserved, gerp_bp, gerp_el,
                   hom_ref, het, hom_alt, unknown,
                   aaf, hwe_p_value, inbreeding_coeff, pi_hat,
                   recomb_rate,
                   top_impact.gene,
                   top_impact.transcript,
                   top_impact.is_exonic,
                   top_impact.is_coding,
                   top_impact.is_splicing,
                   top_impact.is_lof,
                   top_impact.exon,
                   top_impact.codon_change,
                   top_impact.aa_change,
                   top_impact.aa_length,
                   top_impact.biotype,
                   top_impact.top_consequence,
                   top_impact.so,
                   top_impact.effect_severity,
                   top_impact.polyphen_pred,
                   top_impact.polyphen_score,
                   top_impact.sift_pred,
                   top_impact.sift_score,
                   infotag.get_ancestral_allele(var), infotag.get_rms_bq(var),
                   infotag.get_cigar(var),
                   infotag.get_depth(var), infotag.get_strand_bias(var),
                   infotag.get_rms_map_qual(var), infotag.get_homopol_run(var),
                   infotag.get_map_qual_zero(var),
                   infotag.get_num_of_alleles(var),
                   infotag.get_frac_dels(var),
                   infotag.get_haplotype_score(var),
                   infotag.get_quality_by_depth(var),
                   infotag.get_allele_count(var), infotag.get_allele_bal(var),
                   infotag.in_hm2(var), infotag.in_hm3(var),
                   infotag.is_somatic(var),
                   infotag.get_somatic_score(var),
                   esp.found, esp.aaf_EA,
                   esp.aaf_AA, esp.aaf_ALL,
                   esp.exome_chip, thousandG.found,
                   thousandG.aaf_AMR, thousandG.aaf_EAS, thousandG.aaf_SAS,
                   thousandG.aaf_AFR, thousandG.aaf_EUR,
                   thousandG.aaf_ALL, grc,
                   gms.illumina, gms.solid,
                   gms.iontorrent, in_cse,
                   encode_tfbs,
                   encode_dnaseI.cell_count,
                   encode_dnaseI.cell_list,
                   encode_cons_seg.gm12878,
                   encode_cons_seg.h1hesc,
                   encode_cons_seg.helas3,
                   encode_cons_seg.hepg2,
                   encode_cons_seg.huvec,
                   encode_cons_seg.k562,
                   vista_enhancers,
                   cosmic_ids,
                   pack_blob(info),
                   cadd_raw,
                   cadd_scaled,
                   fitcons,
                   Exac.found,
                   Exac.aaf_ALL,
                   Exac.adj_aaf_ALL,
                   Exac.aaf_AFR, Exac.aaf_AMR,
                   Exac.aaf_EAS, Exac.aaf_FIN,
                   Exac.aaf_NFE, Exac.aaf_OTH,
                   Exac.aaf_SAS,
                   Exac.num_het,
                   Exac.num_hom_alt,
                   Exac.num_chroms]

        return variant, variant_impacts, extra_fields

    def _prepare_samples(self):
        """
        private method to load sample information
        """
        if not self.args.no_genotypes:
            self.samples = self.vcf_reader.samples
            self.sample_to_id = {}
            for idx, sample in enumerate(self.samples):
                self.sample_to_id[sample] = idx + 1

        self.ped_hash = {}
        if self.args.ped_file is not None:
            self.ped_hash = load_ped_file(self.args.ped_file)

        sample_list = []
        for sample in self.samples:
            i = self.sample_to_id[sample]
            if sample in self.ped_hash:
                fields = self.ped_hash[sample]
                sample_list = [i] + fields
            elif len(self.ped_hash) > 0:
                sys.exit("EXITING: sample %s found in the VCF but "
                         "not in the PED file.\n" % (sample))
            else:
                # if there is no ped file given, just fill in the name and
                # sample_id and set the other required fields to None
                sample_list = [i, 0, sample, 0, 0, -9, -9]
            database.insert_sample(self.c, sample_list)

    def _get_gene_detailed(self):
        """
        define a gene detailed table
        """
        #unique identifier for each entry
        i = 0
        table_contents = detailed_list = []

        config = read_gemini_config(args=self.args)
        path_dirname = config["annotation_dir"]
        file_handle = os.path.join(path_dirname, 'detailed_gene_table_v75')

        for line in open(file_handle, 'r'):
            field = line.strip().split("\t")
            if not field[0].startswith("Chromosome"):
                i += 1
                table = gene_table.gene_detailed(field)
                detailed_list = [str(i),table.chrom,table.gene,table.is_hgnc,
                                 table.ensembl_gene_id,table.ensembl_trans_id,
                                 table.biotype,table.trans_status,table.ccds_id,
                                 table.hgnc_id,table.entrez,table.cds_length,table.protein_length,
                                 table.transcript_start,table.transcript_end,
                                 table.strand,table.synonym,table.rvis,table.mam_phenotype]
                table_contents.append(detailed_list)
        database.insert_gene_detailed(self.c, table_contents)

    def _get_gene_summary(self):
        """
        define a gene summary table
        """
        #unique identifier for each entry
        i = 0
        contents = summary_list = []

        config = read_gemini_config(args=self.args)
        path_dirname = config["annotation_dir"]
        file = os.path.join(path_dirname, 'summary_gene_table_v75')

        for line in open(file, 'r'):
            col = line.strip().split("\t")
            if not col[0].startswith("Chromosome"):
                i += 1
                table = gene_table.gene_summary(col)
                # defaul cosmic census to False
                cosmic_census = 0
                summary_list = [str(i),table.chrom,table.gene,table.is_hgnc,
                                table.ensembl_gene_id,table.hgnc_id,
                                table.transcript_min_start,
                                table.transcript_max_end,table.strand,
                                table.synonym,table.rvis,table.mam_phenotype,
                                cosmic_census]
                contents.append(summary_list)
        database.insert_gene_summary(self.c, contents)

    def update_gene_table(self):
        """
        """
        gene_table.update_cosmic_census_genes(self.c, self.args)

    def _init_sample_gt_counts(self):
        """
        Initialize a 2D array of counts for tabulating
        the count of each genotype type for eaxh sample.

        The first dimension is one bucket for each sample.
        The second dimension (size=4) is a count for each gt type.
           Index 0 == # of hom_ref genotypes for the sample
           Index 1 == # of het genotypes for the sample
           Index 2 == # of missing genotypes for the sample
           Index 3 == # of hom_alt genotypes for the sample
        """
        self.sample_gt_counts = np.array(np.zeros((len(self.samples), 4)),
                                         dtype='uint32')

    def _update_sample_gt_counts(self, gt_types):
        """
        Update the count of each gt type for each sample
        """
        for idx, gt_type in enumerate(gt_types):
            self.sample_gt_counts[idx][gt_type] += 1

    def store_sample_gt_counts(self):
        """
        Update the count of each gt type for each sample
        """
        self.c.execute("BEGIN TRANSACTION")
        for idx, gt_counts in enumerate(self.sample_gt_counts):
            self.c.execute("""insert into sample_genotype_counts values \
                            (?,?,?,?,?)""",
                           [idx,
                            int(gt_counts[HOM_REF]),  # hom_ref
                            int(gt_counts[HET]),  # het
                            int(gt_counts[HOM_ALT]),  # hom_alt
                            int(gt_counts[UNKNOWN])])  # missing
        self.c.execute("END")


def load(parser, args):
    if (args.db is None or args.vcf is None):
        parser.print_help()
        exit("ERROR: load needs both a VCF file and a database file\n")
    if args.anno_type not in ['snpEff', 'VEP', None, "all"]:
        parser.print_help()
        exit("\nERROR: Unsupported selection for -t\n")

    # collect of the the add'l annotation files
    annotations.load_annos(args)

    # create a new gemini loader and populate
    # the gemini db and files from the VCF
    for try_count in range(2):
        try:
            if try_count > 0:
                args.tmp_db = os.path.join(args.tempdir, "%s.db" % uuid.uuid4())

            gemini_loader = GeminiLoader(args)
            gemini_loader.store_resources()
            gemini_loader.store_version()
            gemini_loader.store_vcf_header()
            gemini_loader.populate_from_vcf()
            gemini_loader.update_gene_table()
            # gemini_loader.build_indices_and_disconnect()

            if not args.no_genotypes and not args.no_load_genotypes:
                gemini_loader.store_sample_gt_counts()

            if try_count > 0:
                shutil.move(args.tmp_db, args.db)
            break
        except sqlite3.OperationalError, e:
            sys.stderr.write("sqlite3.OperationalError: %s\n" % e)
    else:
        raise Exception(("Attempted workaround for SQLite locking issue on NFS "
            "drives has failed. One possible reason is that the temp directory "
            "%s is also on an NFS drive.") % args.tempdir)
