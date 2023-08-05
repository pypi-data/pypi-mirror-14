#!/usr/bin/env python

import sys
# For debug, preference local install over all else
if "DEBUG" in sys.argv:
    sys.path.insert(0, "../")
    sys.path.insert(0, "../../") # For mvtest
    sys.path.insert(0, ".")
    sys.argv.remove("DEBUG")
import os

import mvtest
import unittest
from pygwas.boundary import BoundaryCheck
from pygwas.pheno_covar import PhenoCovar

class TestCmdlinePhenoCovar(unittest.TestCase):
    def setUp(self):
        super(TestCmdlinePhenoCovar, self).setUp()
        self.sex_as_covar = PhenoCovar.sex_as_covariate
        self.ped_filename = "__testfile.ped"
        with open(self.ped_filename, "w") as f:
            f.write("""1 1 0 0 1 0.1 A A G T A A G G C T G T T T
2 2 0 0 1 0.4 A C G T G G C G T T G G C T
3 3 0 0 1 1.0 A A G G A G C C C C G T C T
4 4 0 0 1 0.5 A A G G A G C G C T G G T T
5 5 0 0 1 0.9 A C G G A A C G C C G G T T
6 6 0 0 1 1.0 A A G T A A G G C C G G T T
7 7 0 0 1 0.1 A A G T A A G G C T G G T T
8 8 0 0 1 0.4 A C G T G G C G T T G G C T
9 9 0 0 1 1.0 A A G G A G C C C C G T C T
10 10 0 0 1 0.5 A A G G A G C G C T G G T T
11 11 0 0 1 0.9 A C G G A A C G C C G G T T
12 12 0 0 1 1.0 A A G T A A G G C C G G T T""")
        self.genotypes = [
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
            [0, 2, 1, 1, 0, 0, 0, 2, 1, 1, 0, 0],
            [0, 1, 2, 1, 1, 0, 0, 1, 2, 1, 1, 0],
            [1, 2, 0, 1, 0, 0, 1, 2, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        ]

        self.dummy_pheno = [ 0.1, 0.4, 1.0, 0.5, 0.9, 1.0, 0.1, 0.4, 1.0, 0.5, 0.9, 1.0]


        self.map_filename = "__testfile.map"
        with open(self.map_filename, "w") as f:
            f.write("""1 rs0001 0 500
1 rs0002 0 10000
1 rs0003 0 25000
1 rs0004 0 45000
2 rs0005 0 750
2 rs0006 0 10000
2 rs0007 0 25000
""")

        self.pheno_covar = "__phenocovar.txt"
        with open(self.pheno_covar, "w") as file:
            file.write("""FID\tIID\tSEX\tAGE\tBMI
1\t1\t1\t30\t28.54
2\t2\t1\t33\t30.10
3\t3\t2\t28\t24.00
4\t4\t2\t40\t29.21
5\t5\t1\t50\t31.23
6\t6\t1\t30\t29.54
7\t7\t1\t33\t33.10
8\t8\t2\t28\t27.00
9\t9\t2\t40\t27.21
10\t10\t1\t50\t30.23
11\t11\t2\t28\t24.00
12\t12\t2\t40\t29.21
""")

        self.phenotype_data =  [28.54, 30.10, 24, 29.21, 31.23, 29.54, 33.10, 27.00, 27.21, 30.23, 24.00, 29.21]
        self.covariate_data = [[1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 2.0],
                               [30,  33,  28,  40,  50,  30,  33,  28,  40,  50,  28,  40]]





    def tearDown(self):
        super(TestCmdlinePhenoCovar, self).tearDown()
        os.remove(self.ped_filename)
        os.remove(self.map_filename)
        os.remove(self.pheno_covar)
        PhenoCovar.sex_as_covariate = self.sex_as_covar


    def testCmdLinePhenoWithNames(self):
        cmds = "--file %s --pheno %s --pheno-names=BMI --covar %s --covar-names SEX,AGE" % (self.ped_filename.split(".")[0], self.pheno_covar, self.pheno_covar)
        app = mvtest.MVTestApplication()
        ped_parser,pc = app.LoadCmdLine(cmds.split(" "))

        mapdata = [x.strip().split() for x in open(self.map_filename).readlines()]

        c = pc.covariate_data
        y = pc.phenotype_data

        self.assertEqual(["SEX", "AGE"], pc.covariate_labels)
        self.assertEqual(["BMI"], pc.phenotype_names)

        for i in range(0, len(y[0])):
            self.assertAlmostEqual(self.phenotype_data[i], y[0][i])
            self.assertAlmostEqual(self.covariate_data[0][i], c[0][i])
            self.assertAlmostEqual(self.covariate_data[1][i], c[1][i])



    def testCmdLinePhenoWithIndices(self):
        cmds = "--file %s --pheno %s --mphenos=3 --covar %s --covar-numbers 1,2" % (self.ped_filename.split(".")[0], self.pheno_covar, self.pheno_covar)
        app = mvtest.MVTestApplication()
        ped_parser,pc = app.LoadCmdLine(cmds.split(" "))

        mapdata = [x.strip().split() for x in open(self.map_filename).readlines()]

        c = pc.covariate_data
        y = pc.phenotype_data

        self.assertEqual(["SEX", "AGE"], pc.covariate_labels)
        self.assertEqual(["BMI"], pc.phenotype_names)

        for i in range(0, len(y[0])):
            self.assertAlmostEqual(self.phenotype_data[i], y[0][i])
            self.assertAlmostEqual(self.covariate_data[0][i], c[0][i])
            self.assertAlmostEqual(self.covariate_data[1][i], c[1][i])


    def testCmdLineNoExternalVars(self):
        cmds = "--file %s --sex" % (self.ped_filename.split(".")[0])
        app = mvtest.MVTestApplication()
        ped_parser,pc = app.LoadCmdLine(cmds.split(" "))

        mapdata = [x.strip().split() for x in open(self.map_filename).readlines()]

        c = pc.covariate_data
        y = pc.phenotype_data

        self.assertEqual(["SEX"], pc.covariate_labels)
        self.assertEqual(["Pheno-1"], pc.phenotype_names)

        for i in range(0, len(y[0])):
            self.assertAlmostEqual(self.dummy_pheno[i], y[0][i])
            self.assertAlmostEqual(1, c[0][i])

if __name__ == "__main__":
    unittest.main()
