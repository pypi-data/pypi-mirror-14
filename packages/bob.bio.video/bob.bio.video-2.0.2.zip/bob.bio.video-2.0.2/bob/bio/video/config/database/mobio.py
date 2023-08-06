#!/usr/bin/env python

import bob.db.mobio
import bob.bio.base

mobio_video_directory = "[YOUR_MOBIO_VIDEO_DIRECTORY]"

database = bob.bio.base.database.DatabaseBobZT(
    database = bob.db.mobio.Database(
        original_directory = mobio_video_directory,
        original_extension = '.mp4',
    ),
    name = "mobio",
    protocol = 'male',
    models_depend_on_protocol = True,

    all_files_options = {'subworld' : 'twothirds-subsampled'},
    extractor_training_options = {'subworld' : 'twothirds-subsampled'},
    projector_training_options = {'subworld' : 'twothirds-subsampled'},
    enroller_training_options = {'subworld' : 'twothirds-subsampled'},
)
