import luigi
import sciluigi
import pickle
import os.path

from pyannote_workflows.tasks.tvd_dataset import Audio
from pyannote_workflows.tasks.tvd_dataset import Subtitles
from pyannote_workflows.tasks.tvd_dataset import SubtitlesSpeechNonSpeech
from pyannote_workflows.tasks.tvd_dataset import Speaker
from pyannote_workflows.tasks.tvd_dataset import SpeechNonSpeech
from pyannote_workflows.tasks.features.audio import MFCC

from pyannote_workflows.tasks.segmentation import TrainResegmentation
from pyannote_workflows.tasks.segmentation import ApplyResegmentation
from pyannote_workflows.tasks.evaluation import SpeechActivityDetection

from pyannote_workflows.utils import Hyperopt


class SADFromSubtitles(sciluigi.WorkflowTask):

    workdir = luigi.Parameter(default='/work')

    series = luigi.Parameter(default='GameOfThrones')
    season = luigi.IntParameter(default=1)
    episode = luigi.IntParameter(default=1)
    language = luigi.Parameter(default='en')

    mfcc__e = luigi.BoolParameter(default=False)
    mfcc__De = luigi.BoolParameter(default=True)
    mfcc__DDe = luigi.BoolParameter(default=False)
    mfcc__coefs = luigi.IntParameter(default=11)
    mfcc__D = luigi.BoolParameter(default=True)
    mfcc__DD = luigi.BoolParameter(default=False)

    resegmentation__n_components = luigi.IntParameter(default=1024)
    resegmentation__covariance_type = luigi.Parameter(default='diag')
    resegmentation__calibration = luigi.IntParameter(default='isotonic')
    resegmentation__equal_priors = luigi.BoolParameter(default=False)
    resegmentation__min_duration = luigi.FloatParameter(default=0.0)

    hyperopt = luigi.Parameter(default=None)

    def workflow(self):

        # feature extraction

        audioFile = self.new_task(
            'audioFile', Audio,
            series=self.series,
            season=self.season,
            episode=self.episode,
            language=self.language)

        mfcc = self.new_task(
            'mfcc', MFCC,
            workdir=self.workdir,
            e=self.mfcc__e, De=self.mfcc__De, DDe=self.mfcc__DDe,
            coefs=self.mfcc__coefs, D=self.mfcc__D, DD=self.mfcc__DD)

        mfcc.in_audio = audioFile.out_put

        # initialization

        subtitles = self.new_task(
            'subtitles', Subtitles,
            workdir=self.workdir,
            series=self.series,
            season=self.season,
            episode=self.episode,
            language=self.language)

        subtitlesSpeechNonSpeech = self.new_task(
            'subtitlesSpeechNonSpeech', SubtitlesSpeechNonSpeech,
            workdir=self.workdir)

        subtitlesSpeechNonSpeech.in_wav = audioFile.out_put
        subtitlesSpeechNonSpeech.in_subtitles = subtitles.out_put

        # resegmentation

        trainResegmentation = self.new_task(
            'trainResegmentation', TrainResegmentation,
            workdir=self.workdir,
            n_components=self.resegmentation__n_components,
            covariance_type=self.resegmentation__covariance_type,
            calibration=self.resegmentation__calibration,
            equal_priors=self.resegmentation__equal_priors)

        trainResegmentation.in_segmentation = subtitlesSpeechNonSpeech.out_put
        trainResegmentation.in_features = mfcc.out_put

        applyResegmentation = self.new_task(
            'applyResegmentation', ApplyResegmentation,
            workdir=self.workdir,
            min_duration=self.resegmentation__min_duration)

        applyResegmentation.in_model = trainResegmentation.out_put
        applyResegmentation.in_features = mfcc.out_put

        # evaluation

        speaker = self.new_task(
            'speaker', Speaker,
            workdir=self.workdir,
            series=self.series,
            season=self.season,
            episode=self.episode)

        reference = self.new_task('reference', SpeechNonSpeech,
            workdir=self.workdir)

        reference.in_wav = audioFile.out_put
        reference.in_speaker = speaker.out_put

        evaluation = self.new_task(
            'evaluation', SpeechActivityDetection,
            workdir=self.workdir)

        evaluation.in_reference = reference.out_put
        evaluation.in_hypothesis = applyResegmentation.out_put

        if self.hyperopt is not None:
            hyperopt = self.new_task(
                'hyperopt', Hyperopt, temp=self.hyperopt)
            hyperopt.in_evaluation = evaluation.out_put
            return hyperopt

        return evaluation


if __name__ == '__main__':
    sciluigi.run_local(main_task_cls=SubtitleSAD)
