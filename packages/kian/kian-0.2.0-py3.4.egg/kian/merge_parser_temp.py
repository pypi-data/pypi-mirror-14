from collections import defaultdict
from fuzzywuzzy import fuzz
import random
try:
    basestring
except NameError:
    import urllib.request as urllib2
    import pymysql as MySQLdb
else:
    import urllib2
    import MySQLdb


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


class MergeParser(object):

    """docstring for MergeParser"""

    def __init__(self, langa, langb):
        super(MergeParser, self).__init__()
        self.langa = langa
        self.langb = langb

    def extract_features(self, articles, cnf_file='~/replica.my.cnf', host='labsdb'):
        batcha = [i[0].replace(' ', '_').replace('\'', '\\\'') for i in articles]
        batchb = [i[1].replace(' ', '_').replace('\'', '\\\'') for i in articles]
        membersa_query = 'SELECT pp_value, cl_to, cl_type from categorylinks ' \
            'left join page_props on cl_from = pp_page where pp_propname = ' \
            '\'wikibase_item\' and cl_to in (\'' + "','".join(batcha) + '\');'
        parents_query = 'SELECT pp_value, fromP.page_title, cl_type from ' \
            'categorylinks join page as toP on cl_to = toP.page_title join ' \
            'page as fromP on cl_from = fromP.page_id join page_props on ' \
            'toP.page_id = pp_page where pp_propname = \'wikibase_item\' ' \
            'and fromP.page_namespace = 14 ' \
            'and fromP.page_title in (\'' + "','".join(batcha) + '\');'
        membersb_query = 'SELECT pp_value, cl_to, cl_type from categorylinks ' \
            'left join page_props on cl_from = pp_page where pp_propname = ' \
            '\'wikibase_item\' and cl_to in (\'' + "','".join(batchb) + '\');'

        membersa = self.query(self.langa, host, cnf_file, membersa_query)
        membersb = self.query(self.langb, host, cnf_file, membersb_query)

        #cursor.execute(parents_query)
        #parentsa = list(cursor.fetchall())

        langa = {'page': defaultdict(list), 'subcat': defaultdict(list)}
        langb = {'page': defaultdict(list), 'subcat': defaultdict(list)}
        for row in membersa:
            row = [i.decode('utf-8') for i in row]
            langa[row[2]][row[1]].append(row[0])
        for row in membersb:
            row = [i.decode('utf-8') for i in row]
            langb[row[2]][row[1]].append(row[0])

        real_data = {}
        for i in range(len(articles)):
            pagesa = set(langa['page'][articles[i][0].replace(' ', '_').replace('\'', '\\\'')])
            pagesb = set(langb['page'][articles[i][1].replace(' ', '_').replace('\'', '\\\'')])
            subcatsa = set(langa['subcat'][articles[i][0].replace(' ', '_').replace('\'', '\\\'')])
            subcatsb = set(langb['subcat'][articles[i][1].replace(' ', '_').replace('\'', '\\\'')])
            common_pages = len(pagesa & pagesb)
            common_subcats = len(subcatsa & subcatsb)
            real_data[i] = [
                float(common_pages) / max([1, len(pagesa)]),
                float(common_pages) / max([1, len(pagesb)]),
                float(common_subcats) / max([1, len(subcatsa)]),
                float(common_subcats) / max([1, len(subcatsb)]),
                fuzz.ratio(articles[i][0], articles[i][1]) / 100.0
                ]
        return real_data
    @staticmethod
    def query(lang, host, cnf_file, query):
        conn = MySQLdb.connect(
            '%s.%s' % (lang + 'wiki', host),
            db='%s_p' % (lang + 'wiki'),
            read_default_file=cnf_file,
            charset='utf8',
            use_unicode=True)
        cursor = conn.cursor()
        print('Executing the query')
        cursor.execute(query)
        return list(cursor.fetchall())
parser = MergeParser('de', 'fr')
with open('pywikibot-core/true_cases.txt', 'r') as f:
    tr_set = eval(f.read())
false_training_set = []
for i in range(len(tr_set)):
    new_tr_set = tr_set[:i] + tr_set[i + 1:]
    false_training_set.append([tr_set[i], random.sample(new_tr_set, 1)[0]])
res = []
for chunk in chunks(tr_set, 500)
    chunk_res = parser.extract_features(chunk)
    for i in range(len(chunk)):
        res.append(chunk_res[i] + [1])
for chunk in chunks(false_training_set, 500)
    chunk_res = parser.extract_features(chunk)
    for i in range(len(chunk)):
        res.append(chunk_res[i] + [0])
with open('tr_set.txt', 'w') as f:
    f.write(str(res))
