import struct

import numpy
import transposed_pedigree_parser
from data_parser import DataParser
from parsed_locus import ParsedLocus
from . import Exit
from . import BuildReportLine

__copyright__ = "Eric Torstenson"
__license__ = "GPL3.0"
#     This file is part of pyGWAS.
#
#     pyGWAS is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     pyGWAS is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with MVtest.  If not, see <http://www.gnu.org/licenses/>.


class Parser(transposed_pedigree_parser.Parser):


    def __init__(self, fam, bim, bed):
        """Parse PLINK's binary pedigree files.

        Genotype conversion is as follows (taken from
        http://pngu.mgh.harvard.edu/~purcell/plink/binary.shtml)::

           01101100
           HGFEDCBA

                 AB   00  -- homozygote (first)
               CD     11  -- other homozygote (second)
             EF       01  -- heterozygote (third)
           GH         10  -- missing genotype (fourth)

        AWe map those to:
            * 00  -- 0
            * 11  -- 2
            * 01  -- 1
            * 10  -- -1 (or whatever the missing_storage is)
        """

        #: Filename associated with the pedigree data (first 6 columns from
        #: standard pedigree: fid, iid, fid, mid, sex, pheno)
        self.fam_file = fam

        #: filename for marker info in PLINK .bim format
        self.bim_file = bim

        #: Filename associated with the binary allele information (in variant
        #: major format only)
        self.bed_file = bed

        #: Pedigree information for reporting
        self.families = []

        #: Actual pedigree file being parsed (file object)
        self.genotype_file = None

        #: Valid loci to be used for analysis
        self.markers = None

        #: Alleles for each locus
        self.alleles = []

        #: Number of valid individuals
        self.ind_count = 0

        #: Mask indicating valid samples
        self.ind_mask = None

        #: Genotype conversion
        self.geno_conversions = {
                0:2,
                3:0,
                2:1,
                1:DataParser.missing_storage
        }

    def ReportConfiguration(self, file):
        """ Report configuration for logging purposes.

        :param file: Destination for report details
        :return: None
        """

        print >> file, BuildReportLine("BED_FILE", self.bed_file)
        print >> file, BuildReportLine("BIM_FILE", self.bim_file)
        print >> file, BuildReportLine("FAMFILE", self.fam_file)

    def load_fam(self, pheno_covar):
        """Load contents from the .fam file, updating the pheno_covar with \
            family ids found.

        :param pheno_covar: Phenotype/covariate object
        :return: None
        """

        pheno_col = 5
        if not DataParser.has_sex:
            pheno_col -= 1
        if not DataParser.has_parents:
            pheno_col -= 2
        if not DataParser.has_fid:
            pheno_col -= 1

        sex_col = pheno_col - 1
        mask_components = []
        for line in open(self.fam_file):
            words = line.strip().split()
            if len(words) > 1:
                indid = ":".join(words[0:2])
                if DataParser.valid_indid(indid):
                    mask_components.append(0)

                    sex = None
                    pheno = None
                    if DataParser.has_sex:
                        sex = int(words[sex_col])
                    if DataParser.has_pheno:
                        pheno = float(words[pheno_col])
                    pheno_covar.add_subject(indid, sex, pheno)
                    if len(words) > 0:
                        self.families.append(words)
                else:
                    mask_components.append(1)
        mask_components = numpy.array(mask_components)
        self.ind_mask = numpy.zeros(len(mask_components), dtype=numpy.int8)
        self.ind_mask = mask_components
        self.ind_count = self.ind_mask.shape[0]
        pheno_covar.freeze_subjects()

    def load_bim(self, map3=False):
        """Basic marker details loading.

            (chr, rsid, gen. dist, pos, allelel 1, allele2)

        :param map3: When true, ignore the genetic distance column
        :return: None
        """

        cols = [0, 1, 3, 4, 5]
        if map3:
            cols = [0, 1, 2, 3, 4]
        markers = numpy.loadtxt(self.bim_file, dtype=str, usecols=cols)

        if DataParser.boundary.NoExclusions():
            self.markers = numpy.zeros((markers.shape[0], 2), dtype=int)
            self.markers[:, 0] = markers[:, 0].astype(int)
            self.markers[:, 1] = markers[:, 2].astype(int)
            self.rsids = markers[:, 1]
            self.alleles = markers[:, 3:]
        else:
            self.markers = []
            self.rsids = []
            self.alleles = []

            for locus in markers:
                self.markers.append([locus[0], locus[2]])
                self.rsids.append(locus[1])
                self.alleles.append(locus[3:])
            self.markers = numpy.array(self.markers, dtype=numpy.int)
            self.rsids = numpy.array(self.rsids)
            self.alleles = numpy.array(self.alleles)
        self.locus_count = self.markers.shape[0]

    def init_genotype_file(self):
        """Resets the bed file and preps it for starting at the start of the \
            genotype data

        Returns to beginning of file and reads the version so that it points \
        to first marker's info

        :return: None
        """
        self.genotype_file.seek(0)

        buff = self.genotype_file.read(3)
        version = 0
        magic, data_format = buff.unpack("HB", version)
        return magic, data_format

    def extract_genotypes(self, bytes):
        """Extracts encoded genotype data from binary formatted file.

        :param bytes: array of bytes pulled from the .bed file

        :return: standard python list containing the genotype data

        Only ind_count genotypes will be returned (even if there are
        a handful of extra pairs present).

        """
        genotypes = []
        for b in bytes:
            for i in range(0, 4):
                v = ((b>>(i*2)) & 3)
                genotypes.append(self.geno_conversions[v])
        return genotypes[0:self.ind_count]


    def filter_missing(self):
        """Filter out individuals and SNPs that have too many missing to be \
            considered

        :return: None

        This must be run prior to actually parsing the genotypes because it
        initializes the following instance members:
            * ind_mask
            * total_locus_count
            * locus_count
            * data_parser.boundary (adds loci with too much missingness)
        """
        missing             = None
        locus_count         = 0

        # Filter out individuals according to missingness
        self.genotype_file.seek(0)
        magic, data_format = struct.unpack("<HB", self.genotype_file.read(3))

        if data_format != 1:
            Exit(("MVTEST is currently unable to read data formatted as " +
                 "individual major. You must regenerate your data in SNP major"+
                 " format. "))

        self.bytes_per_read = self.ind_count / 4
        if self.ind_count % 4 > 0:
            self.bytes_per_read += 1
        self.fmt_string = "<" + "B"*self.bytes_per_read

        for index in range(self.locus_count):
            buffer = struct.unpack(self.fmt_string,
                                   self.genotype_file.read(self.bytes_per_read))

            chr, pos = self.markers[index]
            rsid = self.rsids[index]

            if DataParser.boundary.TestBoundary(chr, pos, rsid):
                genotypes = numpy.array(self.extract_genotypes(buffer),
                                        dtype=numpy.int8)
                locus_count += 1

                if missing is None:
                    missing = numpy.zeros(genotypes.shape[0], dtype='int8')
                missing +=  0+(genotypes==DataParser.missing_storage)

        max_missing = DataParser.ind_miss_tol * locus_count
        dropped_individuals = 0+(max_missing<missing)

        self.ind_mask = self.ind_mask|dropped_individuals

        valid_individuals = numpy.sum(self.ind_mask==0)
        max_missing = DataParser.snp_miss_tol * valid_individuals

        # We can't merge these two iterations since we need to know which
        # individuals to consider for filtering on MAF
        dropped_snps = []
        self.genotype_file.seek(0)
        self.genotype_file.read(3)
        self.total_locus_count = self.locus_count
        self.locus_count = 0
        for index in range(self.total_locus_count):
            buffer = struct.unpack(self.fmt_string,
                                   self.genotype_file.read(self.bytes_per_read))

            genotypes = numpy.ma.MaskedArray(self.extract_genotypes(buffer),
                                             self.ind_mask).compressed()
            chr, pos = self.markers[index]
            rsid = self.rsids[index]
            if DataParser.boundary.TestBoundary(chr, pos, rsid):
                missing = numpy.sum(0+(genotypes==DataParser.missing_storage))
                if missing > max_missing:
                    DataParser.boundary.dropped_snps[int(chr)].add(int(pos))
                    dropped_snps.append(rsid)
                else:
                    self.locus_count += 1


    def load_genotypes(self):
        """Prepares the file for genotype parsing.

        :return: None
        """

        self.genotype_file = open(self.bed_file, "rb")
        self.filter_missing()

    def populate_iteration(self, iteration):
        """Parse genotypes from the file and iteration with relevant marker \
            details.

        :param iteration: ParseLocus object which is returned per iteration
        :return: True indicates current locus is valid.

        StopIteration is thrown if the marker reaches the end of the file or
        the valid genomic region for analysis.
        """

        cur_idx = iteration.cur_idx

        if cur_idx < self.total_locus_count:
            buffer = struct.unpack(self.fmt_string,
                                   self.genotype_file.read(self.bytes_per_read))
            genotypes = numpy.ma.MaskedArray(self.extract_genotypes(buffer),
                                             self.ind_mask).compressed()

            iteration.chr, iteration.pos = self.markers[cur_idx]
            iteration.rsid = self.rsids[cur_idx]


            if DataParser.boundary.TestBoundary(iteration.chr,
                                                iteration.pos,
                                                iteration.rsid):
                hz_count = numpy.sum(genotypes==1)
                allele_count1 = numpy.sum(genotypes==0)*2 + hz_count
                allele_count2 = numpy.sum(genotypes==2)*2 + hz_count
                iteration.minor_allele, \
                    iteration.major_allele = self.alleles[cur_idx]

                if allele_count2 > allele_count1:
                    iteration.maj_allele_count = allele_count2
                    iteration.min_allele_count = allele_count1
                else:
                    iteration.maj_allele_count = allele_count1
                    iteration.min_allele_count = allele_count2
                iteration.allele_count2 = allele_count2
                iteration.genotype_data = genotypes
                return iteration.maf >= DataParser.min_maf and \
                       iteration.maf <= DataParser.max_maf
        else:
            raise StopIteration
        return False

    def __iter__(self):
        """Use itself as the iterator, starting back at beginning of the \
            genotypic data

        :return: ParsedLocus representing the first locus.
        """


        self.genotype_file.seek(0)
        self.genotype_file.read(3)

        return ParsedLocus(self)



