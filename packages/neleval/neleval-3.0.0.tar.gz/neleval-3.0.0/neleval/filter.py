from __future__ import print_function
import io
import re
import itertools

from .data import Reader, Writer, Mention
from .utils import log

# TODO: something with char encodings


def _read_aux(f, delim='\t'):
    # generates a list of lines per doc
    lines = []
    for l in f:
        if l.startswith('-DOCSTART-') or l.startswith('-X-'):
            if lines:
                yield lines
                lines = []
            continue
        l = l.strip()
        if not l:
            continue
        l = l.split(delim)
        lines.append(l)
    if lines:
        yield lines


class FilterMentions(object):
    """Limit annotated mentions to those matching a criterion

    This either matches a regular expression against the mention text, or
    accepts an auxiliary file, such as the CoNLL 2003 NER-annotated training
    data. Only system mentions whose metadata matches the expression will be
    output, along with all tokens.

    For example, to retain only mentions containing china, use:
        %(prog)s China my-data.linked

    To retain any mentions in one input that are mentions in another, use:
        # field 4 is link prediction; . means match any non-empty text
        %(prog)s '.' --field 4 --aux other-data.linked my-data.linked

    To retain only LOC entity mentions in the input, use:
        # field 3 is NER IOB tag, but CoNLL delimits by space
        %(prog)s LOC --field 3 --delim ' ' --aux neleval/tags.eng my-data.linked

    All tokens in the auxiliary file must align with the input, with documents
    delimited by lines beginning '-DOCSTART-' or '-X-'. Other lines have fields
    delimited by tabs.
    """

    def __init__(self, system, expr, aux=None, field=None, delim='\t', ignore_case=False, show_text=False):
        if aux is None and field is not None:
            raise ValueError('--field requires --aux to be set')
        self.system = system
        self.expr = expr
        self.aux = aux
        self.field = field
        self.delim = delim
        self.ignore_case = ignore_case
        self.show_text = show_text

    def __call__(self):
        out_file = io.BytesIO()
        writer = Writer(out_file)
        string_matches = re.compile(self.expr).search
        if self.aux is not None:
            aux_reader = _read_aux(open(self.aux), self.delim)

            if self.field is None:
                field_slice = slice(None, None)
            else:
                field_slice = slice(self.field - 1, self.field)
        else:
            aux_reader = None
            aux_doc = None
            field_slice = None

        n_mentions_in = n_mentions_out = 0

        for doc in Reader(open(self.system)):
            if aux_reader:
                aux_doc = next(aux_reader)
                assert len(aux_doc) == doc.n_tokens, 'Expected same number of tokens, got {} in aux and {} in input'.format(len(aux_doc), doc.n_tokens)

            n_mentions_in += doc.n_mentions
            for sent, ment in self.filter_mentions(string_matches, doc,
                                                   aux_doc, field_slice):
                sent.explode_mention(ment)
            n_mentions_out += doc.n_mentions

            writer.write(doc)
        log.info('{} of {} mentions match {!r}'.format(n_mentions_out, n_mentions_in, self.expr))
        return out_file.getvalue()

    def filter_mentions(self, string_matches, doc, aux_doc=None, field_slice=None):
        """Generates mentions that don't match the criterion"""
        for sentence in doc.sentences:
            for span in sentence.spans:
                if not isinstance(span, Mention):
                    continue
                mention = span
                if aux_doc is None:
                    text = mention.text
                else:
                    aux_mention = aux_doc[mention.start:mention.end]
                    transposed = list(itertools.izip_longest(*aux_mention))[field_slice]
                    text = '\n'.join(' '.join(x or '' for x in tup)
                                     for tup in transposed)
                # Debatably, this could be done using log.debug, but controlling the level using argparse is a pain.
                if self.show_text:
                    log.info(u'{}\t{}'.format(mention, repr(text)))

                if not string_matches(text):
                    yield sentence, mention

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('expr', help='A PCRE regular expression to match against mention metadata')
        p.add_argument('system', metavar='FILE')
        p.add_argument('--aux', help='Aligned text to match within')
        p.add_argument('--show-text', action='store_true', default=False, help='Show text being matched against on stderr')
        p.add_argument('-f', '--field', type=int, default=None,
                       help='field in the auxiliary file to match against (default: any)')
        p.add_argument('-d', '--delim', default='\t',
                       help='delimiter between fields in the auxiliary file (default: tab)')
        p.add_argument('-i', '--ignore-case', action='store_true', default=False)
        p.set_defaults(cls=cls)
        return p
