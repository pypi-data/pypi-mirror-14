#!/usr/bin/env python
import sys
# For debug, preference local install over all else
if "DEBUG" in sys.argv:
    sys.path.insert(0, "../")
    sys.path.insert(0, "../../") # For mvtest
    sys.path.insert(0, ".")
    sys.argv.remove("DEBUG")

from pygwas import bed_parser
from pygwas.boundary import BoundaryCheck
from pygwas.snp_boundary_check import SnpBoundaryCheck
from pygwas.data_parser import DataParser
from pygwas.pheno_covar import PhenoCovar
from meanvar import mv_esteq
import unittest
from pkg_resources import resource_filename
import pygwas.standardizer

class TestBase(unittest.TestCase):
    def setUp(self):
        self.missing = "bedfiles/analysis"
        self.missing_bed = resource_filename("tests.meanvar", "%s.bed" % (self.missing))
        self.missing_bim = resource_filename("tests.meanvar", "%s.bim" % (self.missing))
        self.missing_fam = resource_filename("tests.meanvar", "%s.fam" % (self.missing))
        self.genotypes = [
            [2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2],
            [1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1],
            [2, 0, 1, 1, 2, 2, 2, 0, 1, 1, 2, 2],
            [2, 1, 0, 1, 1, 2, 2, 1, 0, 1, 1, 2],
            [1, 0, 2, 1, 2, 2, 1, 0, 2, 1, 2, 2],
            [1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2]
        ]

        self.nonmissing = "bedfiles/analysis"
        self.nonmissing_bed = resource_filename("tests.meanvar", "%s.bed" % (self.nonmissing))
        self.nonmissing_bim = resource_filename("tests.meanvar", "%s.bim" % (self.nonmissing))
        self.nonmissing_fam = resource_filename("tests.meanvar", "%s.fam" % (self.nonmissing))
        self.genotypes_w_missing = [
            [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1],
            [1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1],
            [2, -1, 1, 1, 2, 2, 2, 0, 1, 1, 2, 2],
            [2, -1, 0, 1, 1, 2, 2, 1, 0, 1, 1, 2],
            [1, -1, 2, 1, 2, 2, 1, 0, 2, 1, 2, 2],
            [1, -1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2],
            [2, -1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2]
        ]
        self.chrom          = BoundaryCheck.chrom
        self.boundary       = DataParser.boundary
        self.min_maf        = DataParser.min_maf
        self.max_maf        = DataParser.max_maf
        self.snp_miss_tol   = DataParser.snp_miss_tol
        self.ind_miss_tol   = DataParser.ind_miss_tol
        self.sex_as_covar   = PhenoCovar.sex_as_covariate
        self.standardizer = pygwas.standardizer.get_standardizer()
        pygwas.standardizer.set_standardizer(pygwas.standardizer.NoStandardization)

        DataParser.boundary = BoundaryCheck()

    def tearDown(self):
        PhenoCovar.sex_as_covariate = self.sex_as_covar
        BoundaryCheck.chrom  = self.chrom
        DataParser.boundary  = self.boundary
        DataParser.min_maf   = self.min_maf
        DataParser.max_maf   = self.max_maf
        DataParser.snp_miss_tol  = self.snp_miss_tol
        DataParser.ind_miss_tol  = self.ind_miss_tol
        DataParser.ind_exclusions = []
        pygwas.standardizer.set_standardizer(self.standardizer)

# We aren't testing the actual application. Just the analysis portion
class TestAnalysisBed(TestBase):
    def testBedAnalysis(self):
        # We'll start with the correct phenotype with the genotypes, so we'll use
        # a boundary to restrict us to only use the first SNP
        BoundaryCheck.chrom = 1
        DataParser.boundary = BoundaryCheck()
        pheno = PhenoCovar()
        ped_parser = bed_parser.Parser(self.nonmissing_fam, self.nonmissing_bim, self.nonmissing_bed)
        ped_parser.load_fam(pheno)
        ped_parser.load_bim(map3=False)
        ped_parser.load_genotypes()

        results = [x for x in mv_esteq.RunAnalysis(ped_parser, pheno)]


        self.assertAlmostEqual(0.00347562, results[0].p_mvtest, places=6)
        self.assertAlmostEqual(0.00085539, results[0].lmpv, places=6)
        self.assertAlmostEqual(0.5777812, results[1].p_mvtest, places=6)
        self.assertAlmostEqual(0.42212155, results[1].lmpv, places=6)
        self.assertAlmostEqual(0.44661276, results[2].p_mvtest, places=6)
        self.assertAlmostEqual(0.61386344, results[2].lmpv, places=6)
        self.assertAlmostEqual(0.13555597, results[3].p_mvtest, places=6)
        self.assertAlmostEqual(0.59682217, results[3].lmpv, places=6)
        self.assertAlmostEqual(0.54029842, results[4].p_mvtest, places=6)
        self.assertAlmostEqual(0.60475964, results[4].lmpv, places=6)
        self.assertAlmostEqual(0.03547514, results[5].p_mvtest, places=6)
        self.assertAlmostEqual(0.86663730, results[5].lmpv, places=6)
        self.assertAlmostEqual(0.79249216, results[6].p_mvtest, places=6)
        self.assertAlmostEqual(0.67678089, results[6].lmpv, places=6)
        self.assertAlmostEqual(0.20973300, results[7].p_mvtest, places=6)
        self.assertAlmostEqual(0.14431260, results[7].lmpv, places=6)
        self.assertAlmostEqual(0.81471528, results[8].p_mvtest, places=6)
        self.assertAlmostEqual(0.56378497, results[8].lmpv, places=6)

    def testBedBounded(self):
        BoundaryCheck.chrom = 1
        DataParser.boundary = BoundaryCheck(bp=[2000,3000])
        pheno = PhenoCovar()
        ped_parser = bed_parser.Parser(self.nonmissing_fam, self.nonmissing_bim, self.nonmissing_bed)
        ped_parser.load_fam(pheno)
        ped_parser.load_bim(map3=False)
        ped_parser.load_genotypes()

        results = [x for x in mv_esteq.RunAnalysis(ped_parser, pheno)]

        self.assertEqual(1, results[0].chr)
        self.assertEqual(2000, results[0].pos)
        self.assertAlmostEqual(0.5777811, results[0].p_mvtest, places=6)
        self.assertAlmostEqual(0.4221215, results[0].lmpv, places=6)
        self.assertAlmostEqual(0.4466128, results[1].p_mvtest, places=6)
        self.assertAlmostEqual(0.6138634, results[1].lmpv, places=6)


    def testBedSnpBounded(self):
        BoundaryCheck.chrom = 1
        DataParser.boundary = SnpBoundaryCheck(snps=["rs1000-rs3000"])
        pheno = PhenoCovar()
        ped_parser = bed_parser.Parser(self.nonmissing_fam, self.nonmissing_bim, self.nonmissing_bed)
        ped_parser.load_fam(pheno)
        ped_parser.load_bim(map3=False)
        ped_parser.load_genotypes()

        results = [x for x in mv_esteq.RunAnalysis(ped_parser, pheno)]

        self.assertEqual(1, results[0].chr)
        self.assertEqual(1000, results[0].pos)
        self.assertAlmostEqual(0.00347562, results[0].p_mvtest, places=6)
        self.assertAlmostEqual(0.00085539, results[0].lmpv, places=6)
        self.assertAlmostEqual(0.5777812, results[1].p_mvtest, places=6)
        self.assertAlmostEqual(0.42212155, results[1].lmpv, places=6)
        self.assertAlmostEqual(0.44661276, results[2].p_mvtest, places=6)
        self.assertAlmostEqual(0.61386344, results[2].lmpv, places=6)

class TestAnalysisABedWithCovariates(TestBase):
    def testBedAnalysisCov(self):
        PhenoCovar.sex_as_covariate = True
        DataParser.boundary = BoundaryCheck()
        pheno = PhenoCovar()
        ped_parser = bed_parser.Parser(self.nonmissing_fam, self.nonmissing_bim, self.nonmissing_bed)
        ped_parser.load_fam(pheno)
        ped_parser.load_bim(map3=False)
        ped_parser.load_genotypes()

        results = [x for x in mv_esteq.RunAnalysis(ped_parser, pheno)]

        self.assertAlmostEqual(0.0034238, results[0].p_mvtest, places=6)
        self.assertAlmostEqual(0.0143949, results[0].lmpv, places=6)
        self.assertAlmostEqual(0.58495059, results[1].p_mvtest, places=6)
        self.assertAlmostEqual(0.65786, results[1].lmpv, places=5)
        self.assertAlmostEqual(0.45178985, results[2].p_mvtest, places=6)
        self.assertAlmostEqual(0.83956, results[2].lmpv, places=5)
        self.assertAlmostEqual(0.133661, results[3].p_mvtest, places=6)
        self.assertAlmostEqual(0.82169, results[3].lmpv, places=5)
        self.assertAlmostEqual(0.541391, results[4].p_mvtest, places=6)
        self.assertAlmostEqual(0.83595, results[4].lmpv, places=5)
        self.assertAlmostEqual(0.035665, results[5].p_mvtest, places=6)
        self.assertAlmostEqual(0.94900, results[5].lmpv, places=5)
        self.assertAlmostEqual(0.784660, results[6].p_mvtest, places=6)
        self.assertAlmostEqual(0.59324, results[6].lmpv, places=5)
        self.assertAlmostEqual(0.2137434, results[7].p_mvtest, places=6)
        self.assertAlmostEqual(0.18069, results[7].lmpv, places=5)
        self.assertAlmostEqual(0.8160148, results[8].p_mvtest, places=6)
        self.assertAlmostEqual(0.79734, results[8].lmpv, places=5)


if __name__ == "__main__":
    unittest.main()
