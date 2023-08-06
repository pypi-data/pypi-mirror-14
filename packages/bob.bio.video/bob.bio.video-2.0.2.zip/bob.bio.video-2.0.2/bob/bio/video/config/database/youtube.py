#!/usr/bin/env python

import bob.db.youtube
import bob.bio.base

youtube_directory = "[YOUR_YOUTUBE_DIRECTORY]"

database = bob.bio.base.database.DatabaseBob(
    database = bob.db.youtube.Database(
        original_directory = youtube_directory,
    ),
    name = "youtube",
    protocol = 'fold1',
    models_depend_on_protocol = True,
    training_depends_on_protocol = True,

    all_files_options = {'subworld' : 'fivefolds'},
    extractor_training_options = {'subworld' : 'fivefolds'},
    projector_training_options = {'subworld' : 'fivefolds'},
    enroller_training_options = {'subworld' : 'fivefolds'},
)
