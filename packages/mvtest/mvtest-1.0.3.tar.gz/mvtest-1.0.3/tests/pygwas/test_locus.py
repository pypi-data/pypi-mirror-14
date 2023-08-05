import test_transped_parser
from pygwas.data_parser import DataParser
from pygwas.pheno_covar import PhenoCovar
from pygwas.transposed_pedigree_parser import Parser as TransposedPedigreeParser

class TestLocusBasics(test_transped_parser.TestBase):
    # Test to make sure we can load everything
    def testAllelesIteration(self):
        pc = PhenoCovar()
        ped_parser = TransposedPedigreeParser(self.tfam_filename, self.tped_filename)
        ped_parser.load_tfam(pc)
        ped_parser.load_genotypes()


        index = 0
        for snp in ped_parser:
            self.assertEqual(self.tped1_alleles[index][1], snp.minor_allele)
            self.assertEqual(self.tped1_alleles[index][0], snp.major_allele)

            index += 1
        self.assertEqual(7, index)

    # There was an error where the alleles array is updated despite the attempt at storing actual copies of the
    # Loci in the locus vector. This reflects that error.
    def testAllelesInLoci(self):
        pc = PhenoCovar()
        ped_parser = TransposedPedigreeParser(self.tfam_filename, self.tped_filename)
        ped_parser.load_tfam(pc)
        ped_parser.load_genotypes()


        index = 0
        for snp in ped_parser.get_loci():
            self.assertEqual(self.tped1_alleles[index][1], snp.minor_allele)
            self.assertEqual(self.tped1_alleles[index][0], snp.major_allele)

            index += 1
        self.assertEqual(7, index)
