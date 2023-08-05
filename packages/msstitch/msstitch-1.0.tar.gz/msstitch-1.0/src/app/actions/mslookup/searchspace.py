from Bio import SeqIO


def create_searchspace(lookup, fastafn, proline_cut=False,
                       reverse_seqs=True, do_trypsinize=True):
    """Given a FASTA database, proteins are trypsinized and resulting peptides
    stored in a database or dict for lookups"""
    allpeps = []
    protindex = SeqIO.index(fastafn, 'fasta')
    for acc in protindex:
        if do_trypsinize:
            pepseqs = trypsinize(protindex[acc].seq, proline_cut)
        else:
            pepseqs = [protindex[acc].seq]
        # Exchange all leucines to isoleucines because MS can't differ
        pepseqs = [(str(pep).replace('L', 'I'),) for pep in pepseqs]
        allpeps.extend(pepseqs)
        if len(allpeps) > 1000000:  # more than x peps, write to SQLite
            lookup.write_peps(allpeps, reverse_seqs)
            allpeps = []
    # write remaining peps to sqlite
    lookup.write_peps(allpeps, reverse_seqs)
    lookup.index_peps()
    lookup.close_connection()


def trypsinize(proseq, proline_cut=False):
    # TODO add cysteine to non cut options, use enums
    """Trypsinize a protein sequence. Returns a list of peptides.
    Peptides include both cut and non-cut when P is behind a tryptic
    residue. Multiple consequent tryptic residues are treated as follows:
    PEPKKKTIDE - [PEPK, PEPKK, PEPKKK, KKTIDE, KTIDE, TIDE, K, K, KK ]
    """
    outpeps = []
    currentpeps = ['']
    trypres = set(['K', 'R'])
    noncutters = set()
    if not proline_cut:
        noncutters.add('P')
    for i, aa in enumerate(proseq):
        currentpeps = ['{0}{1}'.format(x, aa) for x in currentpeps]
        if i == len(proseq) - 1:
            continue
        if aa in trypres and proseq[i + 1] not in noncutters:
            outpeps.extend(currentpeps)  # do actual cut by storing peptides
            if proseq[i + 1] in trypres.union('P'):
                # add new peptide to list if we are also to run on
                currentpeps.append('')
            elif trypres.issuperset(currentpeps[-1]):
                currentpeps = [x for x in currentpeps if trypres.issuperset(x)]
                currentpeps.append('')
            else:
                currentpeps = ['']

    if currentpeps != ['']:
        outpeps.extend(currentpeps)
    return outpeps
