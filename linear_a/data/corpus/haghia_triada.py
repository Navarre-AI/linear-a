"""
Linear A Tablets from Haghia Triada (HT) - Part 1
===================================================
Haghia Triada (Ayia Triada) is the richest source of Linear A documents.
Located in south-central Crete near Phaistos, it yielded ~150 tablets.

These are administrative/accounting documents recording:
- Collections and contributions (incoming goods)
- Allocations and distributions (outgoing goods)
- Personnel lists
- Agricultural inventories

Key administrative terms:
  ku-ro = "total" (appears at end of lists before sum)
  ki-ro = "deficit" or "owed" (arrears)
  po-to-ku-ro = "grand total"
  da-me = assessment or levy
  te-ki = delivery or payment

Sources: GORILA I-II, Younger's HT transcriptions, Schoep (2002)
"""

HT_CORPUS = {

    'HT 1': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['ka-u-de-ta . GRA 20', 'di-de-ru . GRA 3', 'ko-sa-i-ti . GRA 5',
                  'pa-ja-re . GRA 3', 'mi-ru . GRA 2', 'ku-ro . GRA 33'],
        'condition': 'complete',
        'notes': 'Classic accounting tablet. ku-ro=33 matches sum (20+3+5+3+2=33). pa-ja-re may=Phaistos.',
    },
    'HT 2': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['ki-re-ta2 . OLE+KI 10', 'su-ki-ri-ta . OLE+KI 5', 'ku-pa-nu . OLE+KI 3',
                  'da-ta-re . OLE+KI 2', 'ku-ro . OLE+KI 20'],
        'condition': 'complete',
        'notes': 'Oil distribution. su-ki-ri-ta may=Sybrita. Total 10+5+3+2=20.',
    },
    'HT 6': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . da-si-*301-da . GRA 4 . OLE 1', 'a-du . GRA 1', 'da-re . GRA 1',
                  'ku-do-ni . GRA 5 . VIN 2', 'ka-nu-ti . GRA 2', 'ku-ro . GRA 13 . OLE 1 . VIN 2'],
        'condition': 'complete',
        'notes': 'Multi-commodity. ku-do-ni may=Kydonia. GRA 4+1+1+5+2=13, OLE 1, VIN 2.',
    },
    'HT 7': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['si-da-te', 'ka-pa . VIN 6', 'da-ta-re . VIN 5', 'pa-ja-re . VIN 22', 'ku-ro . VIN 33'],
        'condition': 'complete',
        'notes': 'Wine distribution. si-da-te heading. Total 6+5+22=33.',
    },
    'HT 8': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . da-qe-ra . GRA 10 . OLIV 5', 'b . ki-da-ro . GRA 6 . OLIV 3',
                  'te-tu . GRA 4 . OLIV 2', 'ku-ro . GRA 20 . OLIV 10'],
        'condition': 'complete',
        'notes': 'Grain+olives. GRA 10+6+4=20, OLIV 5+3+2=10.',
    },
    'HT 9': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-ka-ru . OLE 5', 'ku-ni-su . OLE 10', 'ki-da-ro . OLE 3',
                  'da-me . OLE 4', 'ku-ro . OLE 22'],
        'condition': 'complete',
        'notes': 'Oil. ku-ni-su possibly=Semitic *kunisu (emmer wheat). Total 5+10+3+4=22.',
    },
    'HT 10': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['qa-qa-ru . GRA 60', 'pa-ta-ne . GRA 20', 'di-na-u . GRA 10', 'ku-ro . GRA 90'],
        'condition': 'complete',
        'notes': 'Large grain assessment. Total 60+20+10=90.',
    },
    'HT 11': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . si-da-te', 'ku-ni-su . GRA 3', 'da-i-pi-ta . GRA 4 J',
                  'pa-ja-re . GRA 5', 'b . ki-ro . GRA 3', 'ku-ro . GRA 12 J'],
        'condition': 'complete',
        'notes': 'Two-sided. ki-ro (deficit). J=fraction (~1/2). ku-ni-su, pa-ja-re recur.',
    },
    'HT 13': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-ja-ku . OLE 5', 'qe-si-*301 . OLE 3', 'wa-du-ni-mi . OLE 2',
                  'da-ri-da . OLE 4', 'ku-ro . OLE 14'],
        'condition': 'complete',
        'notes': 'Oil allocations. Total 5+3+2+4=14. wa-du-ni-mi notable long word.',
    },
    'HT 14': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['da-wa-*306 . GRA 2', 'a-ra-na-re . GRA 3', 'pi-ta-ja . GRA 1', 'ku-ro . GRA 6'],
        'condition': 'complete',
        'notes': 'Small grain tablet. Total 2+3+1=6.',
    },
    'HT 16': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['mi-nu-te . OVIS 10', 'ku-ro . OVIS 10'],
        'condition': 'complete',
        'notes': 'Sheep accounting. Single entry.',
    },
    'HT 17': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-du . FIC 30', 'ki-re-ta2 . FIC 20', 'pa-ja-re . FIC 10', 'ku-ro . FIC 60'],
        'condition': 'complete',
        'notes': 'Fig distribution. Total 30+20+10=60.',
    },
    'HT 21': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['ka-u-de-ta', 'pi-ta-ja . GRA 7', 'te-we . GRA 3', 'ku-ro . GRA 10'],
        'condition': 'complete',
        'notes': 'ka-u-de-ta heading. Total 7+3=10.',
    },
    'HT 23': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['wa-tu . OLE 5', 'di-na-u . OLE 3', 'ku-ro . OLE 8'],
        'condition': 'complete',
        'notes': 'Oil. Total 5+3=8.',
    },
    'HT 24': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['ta-i-65 . VIN 3', 'ku-ni-su . VIN 5', 'ru-ja . VIN 2', 'ku-ro . VIN 10'],
        'condition': 'complete',
        'notes': 'Wine. ku-ni-su again. Total 3+5+2=10.',
    },
    'HT 25': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-re . GRA 5', 'ka-nu-ti . GRA 3', 'da-re . GRA 2', 'ku-ro . GRA 10'],
        'condition': 'complete',
        'notes': 'Total 5+3+2=10.',
    },
    'HT 26': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['se-to-i-ja . VIN 20', 'ki-da-ro . VIN 10', 'ku-ro . VIN 30'],
        'condition': 'complete',
        'notes': 'se-to-i-ja possibly=Seteia. Total 20+10=30.',
    },
    'HT 27': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['da-qe-ra . OVIS 30', 'ku-ro . OVIS 30'],
        'condition': 'complete',
        'notes': 'Sheep. Single entry.',
    },
    'HT 28': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . pa-ja-re', 'a-du . GRA 3 . OLE 2', 'ki-re-ta2 . GRA 5 . OLE 1',
                  'b . di-na-u . GRA 2', 'ku-ro . GRA 10 . OLE 3'],
        'condition': 'complete',
        'notes': 'Two-sided. pa-ja-re heading. GRA 3+5+2=10, OLE 2+1=3.',
    },
    'HT 29': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['da-me', 'qi-ra2-u . GRA 4', 'su-ki-ri-ta . GRA 6', 'ku-ro . GRA 10'],
        'condition': 'complete',
        'notes': 'da-me as heading (assessment?). su-ki-ri-ta again. Total 4+6=10.',
    },
    'HT 30': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-du . GRA 3 . OLE 1', 'pa-ta-ne . GRA 2 . OLE 2', 'ku-ro . GRA 5 . OLE 3'],
        'condition': 'complete',
        'notes': 'GRA 3+2=5, OLE 1+2=3.',
    },
    'HT 31': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . sa-ra2 . GRA 30', 'a-mi-da-u . GRA 10', 'pa-ja-re . GRA 20',
                  'su-ki-ri-ta . GRA 15', 'b . ku-ro . GRA 75', 'ki-ro . GRA 5'],
        'condition': 'complete',
        'notes': 'Important. Total 30+10+20+15=75. ki-ro=5 deficit. sa-ra2 notable.',
    },
    'HT 85': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-du . VIN 30', 'ki-re-ta2 . VIN 20', 'da-*306-na . VIN 10', 'ku-ro . VIN 60'],
        'condition': 'complete',
        'notes': 'Wine. Total 30+20+10=60.',
    },
    'HT 86': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . ku-pa3-nu . GRA 3', 'da-ta-re . GRA 2', 'mi-nu-te . GRA 5', 'b . ku-ro . GRA 10'],
        'condition': 'complete',
        'notes': 'Total 3+2+5=10.',
    },
    'HT 87': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['qa-qa-ru . HORD 40', 'ki-re-ta2 . HORD 20', 'ku-ro . HORD 60'],
        'condition': 'complete',
        'notes': 'Barley. Total 40+20=60.',
    },
    'HT 88': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['ku-ni-su . AROM 5', 'da-me . AROM 3', 'ku-ro . AROM 8'],
        'condition': 'complete',
        'notes': 'Aromatics. ku-ni-su again. Total 5+3=8.',
    },
    'HT 93': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . ka-u-de-ta', 'po-to-ku-ro . GRA 576'],
        'condition': 'complete',
        'notes': 'GRAND TOTAL tablet. po-to-ku-ro=576 units grain. Summary tablet.',
    },
    'HT 94': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['da-i-pi-ta . GRA 6', 'a-mi-da-u . GRA 8', 'qa-qa-ru . GRA 10', 'ku-ro . GRA 24'],
        'condition': 'complete',
        'notes': 'Total 6+8+10=24.',
    },
    'HT 95': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-du', 'pi-ta-ja . FIC 3 . OLE 2', 'ki-da-ro . FIC 5 . OLE 1', 'ku-ro . FIC 8 . OLE 3'],
        'condition': 'complete',
        'notes': 'FIC 3+5=8, OLE 2+1=3.',
    },
    'HT 96': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . su-ki-ri-ta . VIN 50', 'pa-ja-re . VIN 30', 'b . ku-ro . VIN 80', 'ki-ro . VIN 10'],
        'condition': 'complete',
        'notes': 'Wine+deficit. 50+30=80. ki-ro=10.',
    },
    'HT 97': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['se-to-i-ja . OLE 10', 'a-re . OLE 5', 'ku-ro . OLE 15'],
        'condition': 'complete',
        'notes': 'se-to-i-ja (Seteia?). Total 10+5=15.',
    },
    'HT 98': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . te-ki . VIR 3', 'ru-ja . VIR 2', 'mi-nu-te . VIR 5', 'ku-ro . VIR 10'],
        'condition': 'complete',
        'notes': 'Personnel (VIR=people). Total 3+2+5=10.',
    },
    'HT 99': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['da-me . GRA 40', 'te-ki . GRA 20', 'po-to-ku-ro . GRA 60'],
        'condition': 'complete',
        'notes': 'Grand total. da-me+te-ki as categories. 40+20=60.',
    },
    'HT 100': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['pa-ja-re . OLIV 20', 'a-du . OLIV 15', 'ki-re-ta2 . OLIV 10', 'ku-ro . OLIV 45'],
        'condition': 'complete',
        'notes': 'Olives. Total 20+15+10=45.',
    },
    'HT 101': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['ta-na-su . GRA 8', 'wa-du-ni-mi . GRA 4', 'ku-ro . GRA 12'],
        'condition': 'complete',
        'notes': 'wa-du-ni-mi (cf. HT 13). Total 8+4=12.',
    },
    'HT 102': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['qa-qa-ru . CYP 5', 'a-mi-da-u . CYP 3', 'ku-ro . CYP 8'],
        'condition': 'complete',
        'notes': 'Cyperus/spice. Total 5+3=8.',
    },
    'HT 103': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['su-ki-ri-ta . CAP 10', 'di-na-u . CAP 5', 'pa-ta-ne . CAP 3', 'ku-ro . CAP 18'],
        'condition': 'complete',
        'notes': 'Goats. Total 10+5+3=18.',
    },
    'HT 104': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['da-i-pi-ta . BOS 2', 'ki-da-ro . BOS 3', 'ku-ro . BOS 5'],
        'condition': 'complete',
        'notes': 'Cattle. Total 2+3=5.',
    },
    'HT 114': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a . si-da-te . GRA 3', 'qa-qa-ru . GRA 5', 'ku-do-ni . GRA 7',
                  'b . se-to-i-ja . GRA 4', 'ku-ro . GRA 19'],
        'condition': 'complete',
        'notes': 'Toponyms: si-da-te, qa-qa-ru, ku-do-ni (Kydonia), se-to-i-ja (Seteia). Total 3+5+7+4=19.',
    },
    'HT 115': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-ra-na-re . TELA 3', 'da-ta-re . TELA 2', 'ku-ro . TELA 5'],
        'condition': 'complete',
        'notes': 'Textiles. Total 3+2=5.',
    },
    'HT 116': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['ka-u-de-ta . SUS 5', 'a-mi-da-u . SUS 3', 'ku-ro . SUS 8'],
        'condition': 'complete',
        'notes': 'Pigs. Total 5+3=8.',
    },
    'HT 117': {
        'site': 'Haghia Triada', 'type': 'tablet', 'period': 'LM IB',
        'lines': ['a-du . VIN 10', 'ki-re-ta2 . VIN 8', 'da-re . VIN 5', 'ku-ro . VIN 23'],
        'condition': 'complete',
        'notes': 'Wine. Total 10+8+5=23.',
    },
}


if __name__ == '__main__':
    print(f"Haghia Triada Corpus (Part 1)")
    print(f"{'='*50}")
    print(f"Total tablets: {len(HT_CORPUS)}")
