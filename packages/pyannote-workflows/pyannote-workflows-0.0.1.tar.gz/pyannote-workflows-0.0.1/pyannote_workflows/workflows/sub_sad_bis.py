import luigi
import sciluigi
import pickle
import os.path

from pyannote_workflows.tasks.tvd_dataset import Audio
from pyannote_workflows.tasks.tvd_dataset import Subtitles
from pyannote_workflows.tasks.tvd_dataset import Speaker
from pyannote_workflows.tasks.tvd_dataset import SpeechNonSpeech
from pyannote_workflows.tasks.features.audio import MFCC
from pyannote_workflows.tasks.segmentation import Resegmentation
from pyannote_workflows.tasks.utils import Subtitle2SpeechNonSpeech
from pyannote_workflows.tasks.evaluation import SpeechActivityDetection


class SubtitleSAD(sciluigi.WorkflowTask):

    workdir = luigi.Parameter(default='/work', significant=False)

    series = luigi.Parameter(default='GameOfThrones')
    season = luigi.IntParameter(default=1)
    episode = luigi.IntParameter(default=1)
    language = luigi.Parameter(default='en')

    mfcc__e = luigi.BoolParameter(default=False)
    mfcc__De = luigi.BoolParameter(default=True)
    mfcc__DDe = luigi.BoolParameter(default=False)
    mfcc__coefs = luigi.IntParameter(default=11)
    mfcc__D = luigi.BoolParameter(default=False)
    mfcc__DD = luigi.BoolParameter(default=False)

    resegmentation__n_components = luigi.IntParameter(default=64)
    resegmentation__covariance_type = luigi.Parameter(default='diag')
    resegmentation__calibration = luigi.IntParameter(default='isotonic')
    resegmentation__equal_priors = luigi.BoolParameter(default=True)
    resegmentation__min_duration = luigi.FloatParameter(default=0.0)

    def workflow(self):

        # feature extraction

        audio = self.new_task(
            'audio', Audio,
            series=self.series,
            season=self.season,
            episode=self.episode,
            language=self.language)

        mfcc = self.new_task(
            'mfcc', MFCC,
            workdir=self.workdir,
            e=self.mfcc__e, De=self.mfcc__De, DDe=self.mfcc__DDe,
            coefs=self.mfcc__coefs, D=self.mfcc__D, DD=self.mfcc__DD)

        mfcc.in_audio = audio.out_put

        # initialization

        subtitles = self.new_task(
            'subtitles', Subtitles,
            series=self.series,
            season=self.season,
            episode=self.episode,
            language=self.language)

        speech_nonspeech = self.new_task(
            'speech_nonspeech', Subtitle2SpeechNonSpeech,
            workdir=self.workdir)

        speech_nonspeech.in_wav = audio.out_put
        speech_nonspeech.in_subtitles = subtitles.out_put

        # resegmentation

        resegmentation = self.new_task(
            'resegmentation', Resegmentation,
            workdir=self.workdir,
            n_components=self.resegmentation__n_components,
            covariance_type=self.resegmentation__covariance_type,
            calibration=self.resegmentation__calibration,
            equal_priors=self.resegmentation__equal_priors,
            min_duration=self.resegmentation__min_duration)

        resegmentation.in_segmentation = speech_nonspeech.out_put
        resegmentation.in_features = mfcc.out_put

        # evaluation

        speaker = self.new_task(
            'speaker', Speaker,
            workdir=self.workdir,
            series=self.series,
            season=self.season,
            episode=self.episode)

        reference = self.new_task(
            'reference', SpeechNonSpeech, workdir=self.workdir)

        reference.in_wav = audio.out_put
        reference.in_speaker = speaker.out_put

        evaluation = self.new_task(
            'evaluation', SpeechActivityDetection,
            workdir=self.workdir)

        evaluation.in_reference = reference.out_put
        evaluation.in_hypothesis = resegmentation.out_put

        return evaluation


if __name__ == '__main__':
    sciluigi.run_local(main_task_cls=SubtitleSAD)
