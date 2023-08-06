import tempfile, csv

import mongoengine
import numpy as np
import pandas as pd


class TrialMetadata(mongoengine.EmbeddedDocument):
    session_number = mongoengine.IntField(required=True)
    location = mongoengine.StringField(required=True)
    terminal = mongoengine.IntField(required=True)


class SignalMetadata(mongoengine.EmbeddedDocument):
    session_number = mongoengine.IntField(required=True)
    location = mongoengine.StringField(required=True)
    terminal = mongoengine.IntField(required=True)


class Signal(mongoengine.Document):
    """
    A class to hold documents from the ``eim.signals`` collection in the
    Emotion in Motion database. Signals represent the psychophysiological
    signal recordings made for a single participant during one media
    excerpt.
    """
    meta = {
        'collection': 'signals'
    }

    data_file = mongoengine.FileField(collection_name='signals')
    derived_eda_data_file = mongoengine.FileField(collection_name='signals')
    derived_pox_data_file = mongoengine.FileField(collection_name='signals')
    trial = mongoengine.ReferenceField('Trial')
    label = mongoengine.StringField()
    metadata = mongoengine.EmbeddedDocumentField(SignalMetadata)

    def _base_dict(self):

        trial_id = str(self.trial.id) if self.trial is not None else None

        return {
            'data_file': str(self.data_file.grid_id),
            'derived_eda_data_file': str(self.derived_eda_data_file.grid_id),
            'derived_pox_data_file': str(self.derived_pox_data_file.grid_id),
            'trial': trial_id,
            'label': self.label,
            'location': self.metadata.location,
            'terminal': self.metadata.terminal,
            'session_number': self.metadata.session_number
        }

    def _signal_trial_dict(self):

        signal_trial_dict = {}

        if self.trial is not None:

            trial_signals_list = list(map(lambda x: x.id, self.trial.signals))

            if self.id in trial_signals_list:
                order = trial_signals_list.index(self.id)
                signal_trial_dict['order'] = order


                signal_trial_dict['most_enjoyed'] = \
                    order == self.trial.answers.most_enjoyed - 1
                signal_trial_dict['most_engaged'] = \
                    order == self.trial.answers.most_engaged - 1


                if self.trial.answers.ratings is not None:
                    for rating in self.trial.answers.ratings:

                        this_rating = np.nan
                        try:
                            this_rating = self.trial.answers.ratings[rating][order]
                        except:
                            pass

                        signal_trial_dict[rating] = this_rating

                if 'media' in self.trial.timestamps.keys():
                    time = None
                    try:
                        time = self.trial.timestamps['media'][order]
                    except:
                        pass
                    signal_trial_dict['time'] = time

        return signal_trial_dict


    def to_dataframe(self):
        base_dict = self._base_dict()
        signal_trial_dict = self._signal_trial_dict()

        combined_dict = base_dict.copy()
        combined_dict.update(signal_trial_dict)

        return pd.DataFrame(combined_dict, index=[str(self.id)])

    # TODO: Rethink this logic, and whether or not we should store all associated data files in a list
    def signal_file_as_dataframe(self, name):
        """
        Retrieve an associated signal file from GridFS and return it as a
        :py:class:`pandas.DataFrame`.

        Returns
        -------
        out : :py:class:`pandas.DataFrame`
            This :py:class:`pandas.DataFrame` contains each recorded
            signal/feature in its columns.

        Examples
        --------
        >>> import eim
        >>> eim.connect('eim', 'eim')
        >>> signal = Signal.objects(id='5410edbb08ad6ee3090e20be')[0]
        >>> data = signal.original_signals()
        >>> data.iloc[0:1]
           eda_filtered  eda_raw  eda_status      hr  hr_status  pox_raw  timestamps
        0        135.05      136           1  48.387          0        0           0
        """
        # Read the file that original_data_file references into a temp file
        # and extract lines
        try:
            gridfs_file = getattr(self, name)

            lines = None
            with tempfile.TemporaryFile(mode='w+') as csv_file:
                csv_file.write(gridfs_file.read().decode('utf-8'))
                csv_file.seek(0)

                reader = csv.reader(csv_file)
                lines = list(reader)

            # First line should be column names
            columns = lines[0]
            out_dict = {}
            for column in columns:
                out_dict[column] = []

            # Build lists for each column
            for line in lines[1:]:
                for i, column in enumerate(columns):
                    value = np.nan if line[i] == 'NA' else line[i]
                    out_dict[column].append(value)

            # Convert each column list to a numpy.ndarray
            for column in columns:
                out_dict[column] = np.asarray(
                    out_dict[column], dtype='float64'
                )

            # Return a pandas.DataFrame of the signals and cache them
            return pd.DataFrame(out_dict)

        except:
            return None


class Media(mongoengine.Document):
    """
    A class to describe media excerpts used in the Emotion in Motion
    experiments.

    Attributes
    ----------
    type : :py:class:`mongoengine.StringField`
        The type of the media excerpt. Acceptable values are `'audio'` or
        `'video'`.
    artist : :py:class:`mongoengine.StringField`
        The artist/author of the media excerpt (required).
    title : :py:class:`mongoengine.StringField`
        The title of the media excerpt (required).
    label : :py:class:`mongoengine.StringField`
        A string label used throughout a number of Emotion in Motion
        experiments to uniquely identify a media excerpt.
    has_lyrics : :py:class:`mongoengine.StringField`
        An indicator of whether or not the media excerpt has lyrical (spoken)
        content.
    comments : :py:class:`mongoengine.StringField`
        General comments about the media excerpt.
    year : :py:class:`mongoengine.DateTimeField`
        The year the media excerpt was published/released.
    excerpt_start_time : :py:class:`mongoengine.FloatField`
        If the media excerpt is indeed an excerpt, the start time of the
        excerpt with respect to the original recording, in seconds.
    excerpt_end_time : :py:class:`mongoengine.FloatField`
        If the media excerpt is indeed an excerpt, the end time of the
        excerpt with respect to the original recording, in seconds.
    bpm : :py:class:`mongoengine.FloatField`
        For musical media excerpts, the tempo of the excerpt in beats per
        minute.
    source : :py:class:`mongoengine.StringField`
        This attribute is for indicating the original source of an excerpt. For
        example, as some songs are recorded by an artist many times, this
        field should be used to indicate the actual source of the recording
        used in the experiment.
    key : :py:class:`mongoengine.StringField`
        For musical media excerpts, the key signature of the excerpt.
    file : :py:class:`mongoengine.FileField`
        The actual media file for the excerpt.

    Examples
    --------
    >>> import eim
    >>> eim.connect('eim', 'eim')
    >>> media = Media.objects(id='537e53b3df872bb71e4df264')[0]
    >>> media.type
    'audio'

    >>> media.artist
    'The Verve'

    >>> media.title
    'Bittersweet Symphony'

    >>> media.label
    'R004'

    >>> media.has_lyrics
    True

    >>> media.comments == None
    True

    >>> media.year
    datetime.datetime(1997, 1, 1, 0, 0)

    >>> media.excerpt_start_time
    0.0

    >>> media.excerpt_end_time
    95.63

    >>> media.bpm
    173.83

    >>> media.source == None
    True

    >>> media.key
    'a_major'

    >>> media.file.grid_id
    ObjectId('537e4b62a754dfd806fa8763')
    """
    meta = {
        'collection': 'media',
        'strict': False
    }

    # TODO: Add emotion_tags field when that we have a class emotion_tags
    # TODO: Add genres field when we have a class for genres

    type = mongoengine.StringField(choices=['audio', 'video'])
    artist = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    label = mongoengine.StringField()
    has_lyrics = mongoengine.BooleanField()
    comments = mongoengine.StringField()
    year = mongoengine.DateTimeField()
    excerpt_start_time = mongoengine.FloatField()
    excerpt_end_time = mongoengine.FloatField()
    bpm = mongoengine.FloatField()
    source = mongoengine.StringField()
    key = mongoengine.StringField()
    file = mongoengine.FileField(collection_name='media')


class Researcher(mongoengine.Document):
    meta = {
        'collection': 'researchers'
    }
    last_name = mongoengine.StringField(required=True)
    first_name = mongoengine.StringField(required=True)
    email_address = mongoengine.StringField(required=True)
    institution = mongoengine.StringField()


class MediaPool(mongoengine.Document):
    meta = {
        'collection': 'media_pools'
    }
    media = mongoengine.ListField(mongoengine.ReferenceField(Media),
                                  required=True)


class Experiment(mongoengine.Document):
    """
    A class to hold documents from the ``eim.experiments`` collection in the
    Emotion in Motion database.

    Attributes
    ----------
    """
    meta = {
        'collection': 'experiments'
    }
    description = mongoengine.StringField(required=True)
    version = mongoengine.IntField(required=True)
    name = mongoengine.StringField(required=True)
    researchers = mongoengine.ListField(mongoengine.ReferenceField(Researcher))
    location = mongoengine.StringField(required=True)
    terminals = mongoengine.ListField(mongoengine.IntField())
    start_date = mongoengine.DateTimeField()
    end_date = mongoengine.DateTimeField()
    media_pool = mongoengine.ListField(mongoengine.ReferenceField(MediaPool))


class TrialRatings(mongoengine.DynamicEmbeddedDocument):
    activity = mongoengine.ListField(mongoengine.FloatField())
    chills = mongoengine.ListField(mongoengine.FloatField())
    chillsshiversthrills = mongoengine.ListField(mongoengine.FloatField())
    engagement = mongoengine.ListField(mongoengine.FloatField())
    familiarity = mongoengine.ListField(mongoengine.FloatField())
    goosebumps = mongoengine.ListField(mongoengine.FloatField())
    inspired = mongoengine.ListField(mongoengine.FloatField())
    joyfulactivation = mongoengine.ListField(mongoengine.FloatField())
    like_dislike = mongoengine.ListField(mongoengine.FloatField())
    nostalgia = mongoengine.ListField(mongoengine.FloatField())
    overwhelmed = mongoengine.ListField(mongoengine.FloatField())
    peacefulness = mongoengine.ListField(mongoengine.FloatField())
    positivity = mongoengine.ListField(mongoengine.FloatField())
    power = mongoengine.ListField(mongoengine.FloatField())
    sadness = mongoengine.ListField(mongoengine.FloatField())
    shivers = mongoengine.ListField(mongoengine.FloatField())
    spirituality = mongoengine.ListField(mongoengine.FloatField())
    tenderness = mongoengine.ListField(mongoengine.FloatField())
    tension = mongoengine.ListField(mongoengine.FloatField())
    thrills = mongoengine.ListField(mongoengine.FloatField())
    transcendence = mongoengine.ListField(mongoengine.FloatField())
    wonder = mongoengine.ListField(mongoengine.FloatField())


class TrialAnswers(mongoengine.DynamicEmbeddedDocument):
    age = mongoengine.IntField()
    dob = mongoengine.DateTimeField()
    emotion_indices = mongoengine.ListField(mongoengine.FloatField())
    hearing_impairments = mongoengine.BooleanField()
    most_engaged = mongoengine.IntField()
    most_enjoyed = mongoengine.IntField()
    music_styles = mongoengine.ListField(mongoengine.StringField())
    musical_background = mongoengine.BooleanField()
    musical_expertise = mongoengine.IntField()
    nationality = mongoengine.StringField()
    ratings = mongoengine.EmbeddedDocumentField(TrialRatings)
    sex = mongoengine.StringField(choices=['male', 'female'])
    visual_impairments = mongoengine.BooleanField()


class Trial(mongoengine.Document):
    """
    A class to hold documents from the ``eim.trials`` collection in the
    Emotion in Motion database.

    Attributes
    ----------
    signals : :py:class:`mongoengine.fields.ListField` of :py:class:`Signal`
        A list of the signals (as :py:class:`Signal` instances) in the order
        in which they were recorded during the trial
    media : :py:class:`mongoengine.fields.ListField` of :py:class:`Media`
        A list of the media excerpts (as :py:class:`Media` instances) in the
        order  in which they were presented during the trial
    """
    meta = {
        'collection': 'trials'
    }
    random = mongoengine.FloatField()
    timestamps = mongoengine.DictField()
    valid = mongoengine.BooleanField()
    invalid_reason = mongoengine.StringField()

    answers = mongoengine.EmbeddedDocumentField(TrialAnswers)

    signals = mongoengine.ListField(mongoengine.ReferenceField('Signal'))
    media = mongoengine.ListField(mongoengine.ReferenceField(Media))

    experiment = mongoengine.ReferenceField(Experiment)
    metadata = mongoengine.EmbeddedDocumentField(TrialMetadata)
    date = mongoengine.DateTimeField()


    def to_dataframe(self):

        trial_dict = {
            'date': self.date,
            'experiment': str(self.experiment.id),
            'location': self.metadata.location,
            'terminal': self.metadata.terminal,
            'session_number': self.metadata.session_number,
            'age': self.answers.age,
            'hearing_impairments': self.answers.hearing_impairments,
            'visual_impairments': self.answers.visual_impairments,
            'musical_background': self.answers.musical_background,
            'musical_expertise': self.answers.musical_expertise,
            'gender': self.answers.sex,
            'nationality': self.answers.nationality
        }

        return pd.DataFrame(trial_dict, index=[str(self.id)])

