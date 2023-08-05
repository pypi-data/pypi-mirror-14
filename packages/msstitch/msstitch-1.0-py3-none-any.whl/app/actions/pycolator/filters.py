import re
from app.lookups.sqlite import searchspace as sqlite
from app.readers import pycolator as reader
from app.readers import xmlformatting as formatting


def get_either_seq(seqtype, element, ns):
    get_seq_map = {'psm': reader.get_psm_seq,
                   'pep': reader.get_peptide_seq,
                   }
    return get_seq_map[seqtype](element, ns)


def filter_peptide_length(features, elementtype, ns, minlen=0, maxlen=None):
    minlen = int(minlen)
    if maxlen is None:
        maxlen = float('inf')
    else:
        maxlen = int(maxlen)
    for feat in features:
        seq = get_either_seq(elementtype, feat, ns)
        seq = strip_modifications(seq)
        if len(seq) > minlen and len(seq) < maxlen:
            yield formatting.string_and_clear(feat, ns)
        else:
            formatting.clear_el(feat)


def strip_modifications(seq):
    return re.sub('\[UNIMOD:\d*\]', '', seq)


def filter_known_searchspace(elements, seqtype, lookup, ns, ntermwildcards):
    """Yields peptides from generator as long as their sequence is not found in
    known search space dict. Useful for excluding peptides that are found in
    e.g. ENSEMBL or similar"""
    for element in elements:
        seq = get_either_seq(seqtype, element, ns)
        seq = strip_modifications(seq)
        # Exchange leucines for isoleucines since MS can't differ and we
        # don't want to find 'novel' peptides which only have a difference
        # in this amino acid
        seq = seq.replace('L', 'I')
        if not lookup.check_seq_exists(seq, ntermwildcards):
            yield formatting.string_and_clear(element, ns)
        else:
            formatting.clear_el(element)


def filter_unique_peptides(peptides, score, ns):
    """ Filters unique peptides from multiple Percolator output XML files.
        Takes a dir with a set of XMLs, a score to filter on and a namespace.
        Outputs an ElementTree.
    """
    scores = {'q': 'q_value',
              'pep': 'pep',
              'p': 'p_value',
              'svm': 'svm_score'}
    highest = {}
    for el in peptides:
        featscore = float(el.xpath('xmlns:%s' % scores[score],
                                   namespaces=ns)[0].text)
        seq = reader.get_peptide_seq(el, ns)

        if seq not in highest:
            highest[seq] = {
                'pep_el': formatting.stringify_strip_namespace_declaration(
                    el, ns), 'score': featscore}
        if score == 'svm':  # greater than score is accepted
            if featscore > highest[seq]['score']:
                highest[seq] = {
                    'pep_el':
                    formatting.stringify_strip_namespace_declaration(el, ns),
                    'score': featscore}
        else:  # lower than score is accepted
            if featscore < highest[seq]['score']:
                highest[seq] = {
                    'pep_el':
                    formatting.stringify_strip_namespace_declaration(el, ns),
                    'score': featscore}
        formatting.clear_el(el)

    for pep in list(highest.values()):
        yield pep['pep_el']
