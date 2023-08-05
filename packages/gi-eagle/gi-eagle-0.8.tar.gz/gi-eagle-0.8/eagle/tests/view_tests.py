from flask.ext.testing import TestCase
from nose.tools import nottest
from testconfig import config
from eagle.tests.common import get_random_sample, get_random_group



class TestViews(TestCase):
    def post_and_assert_200(self, url, data):
        print("POST: %s" % url)
        for datum in data.items():
            print("%s:\t%s" % datum)
        self.assert_200(self.client.post(url, data=data))

    def get_and_assert_200(self, url):
        print("GET: %s" % url)
        self.assert_200(self.client.get(url))

    def create_app(self):
        from eagle.application import app
        if not "conf" in config.keys():
            config['conf'] = 'config.cfg'
        app._readconfig_(config['conf'])
        import eagle.views
        import eagle.filters as filters
        for view in eagle.views.__all__:
            __import__("eagle.views.%s" % view)
        return app

    @nottest
    def test_files(self):
        # I have no bam files, so I don't know if that works
        self.get_and_assert_200("/bam/%s" % get_random_sample())

    def test_gender_check(self):
        self.get_and_assert_200("/gender_check")

    def test_index(self):
        self.get_and_assert_200("/")

    def test_purity(self):
        testdata = { "case": [get_random_sample(), get_random_sample()],
                     "control": [get_random_sample(), get_random_sample()]}
        self.post_and_assert_200("/purity_estimation", testdata)

    def test_recessive(self):
        from eagle.core.effectenum import EffectNames, exon_effects
        testdata = { "sample": get_random_sample(),
                     "parent1": get_random_sample(),
                     "parent2": get_random_sample(),
                     "effects": [EffectNames[effect] for effect in exon_effects],
                     "minquality": 50
                   }
        self.post_and_assert_200("/recessive", testdata)

    def test_snp(self):
        from eagle.core.effectenum import EffectNames, exon_effects
        testdata = { "case": [get_random_sample()],
#                     "case_group": [get_random_group()],
                     "control": [get_random_sample()],
#                     "control_group": [get_random_group()],
                     "search_all": True,
                     "genes": "ARID1AARID1BARID2SMARCA2SMARCA4SMARCB1++++",
                     "samplespergene": 1,
                     "samplespervariant": 1,
                     "variantspergene": 1,
                     "effects": [EffectNames[effect] for effect in exon_effects],
                     "ignore_heterozygosity": True,
                     "minquality": 50
                   }
        self.post_and_assert_200("/snp", testdata)

    def test_statistics(self):
        self.get_and_assert_200("/statistics")

    def test_variant_detail(self):
        from eagle.views.common import sample_filename
        from eagle.core.wrap.sample import Sample
        import random
        sample = get_random_sample()
        chrom = random.choice(list(Sample(sample_filename(sample)).f["variants"]))
        pos = -1
        typ = "None"
        self.get_and_assert_200("/variant_detail/%s/%s/%s/%s" % (chrom, pos, typ, sample))

    def test_variant_search(self):
        assert False

    def test_variant_overlap(self):
        testdata = { "samples": [get_random_sample() for i in range(3)] }
        self.post_and_assert_200("/variant_overlap", testdata)
