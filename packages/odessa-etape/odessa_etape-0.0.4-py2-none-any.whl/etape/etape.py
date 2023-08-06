import os.path as op
import pyannote.parser
import pyannote.metrics.diarization


class Etape(object):
    """

    Parameters
    ----------
    wav_dir : string, optional
        Path to ETAPE audio files.

    Usage
    -----
    >>> etape = Etape(wav_dir="/path/to/wav_dir/")
    >>> for wav, annotated, annotation in etape.train_iter():
    ...     pass

    """

    def __init__(self, wav_dir=None):
        super(Etape, self).__init__()
        if wav_dir is None:
            wav_dir = op.join(op.dirname(op.realpath(__file__)), 'data/wav')
        self.wav_dir = wav_dir

    def _subset_iter(self, subset):

        # load training file
        mdtm_path = op.join(
            op.dirname(op.realpath(__file__)),
            'data/mdtm/{subset}.mdtm'.format(subset=subset))

        # load evaluation maps
        path = op.join(
            op.dirname(op.realpath(__file__)),
            'data/uem/{subset}.uem'.format(subset=subset))
        uems = pyannote.parser.UEMParser().read(path)

        # load reference
        path = op.join(
            op.dirname(op.realpath(__file__)),
            'data/mdtm/{subset}.mdtm'.format(subset=subset))
        mdtms = pyannote.parser.MDTMParser().read(path)

        for uri in uems.uris:
            annotated = uems(uri)
            annotation = mdtms(uri)
            wav = op.join(self.wav_dir, '{uri}.wav'.format(uri=uri))
            yield wav, annotated, annotation

    def train_iter(self):
        return self._subset_iter('elda-trn')

    def dev_iter(self):
        return self._subset_iter('elda-dev')

    def test_iter(self):
        return self._subset_iter('eval')
