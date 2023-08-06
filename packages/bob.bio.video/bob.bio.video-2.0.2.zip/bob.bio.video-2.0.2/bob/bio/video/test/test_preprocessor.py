import os
import numpy
import bob.io.base
import bob.io.image
import bob.io.video
import bob.bio.base
import bob.bio.video
import bob.db.verification.utils

from nose.plugins.skip import SkipTest
import pkg_resources

regenerate_refs = False

def test_annotations():
  # use annotations to grep
  image_files = [pkg_resources.resource_filename("bob.bio.face.test", "data/testimage.jpg")]
  annotations = {os.path.basename(image_files[0]) : bob.db.verification.utils.read_annotation_file(pkg_resources.resource_filename("bob.bio.face.test", "data/testimage.pos"), 'named')}

  # video preprocessor using a face crop preprocessor
  frame_selector = bob.bio.video.FrameSelector(selection_style="all")
  preprocessor = bob.bio.video.preprocessor.Wrapper('face-crop-eyes', frame_selector, compressed_io=False)

  # read original data
  original = preprocessor.read_original_data(image_files)
  assert isinstance(original, bob.bio.video.FrameContainer)
  assert len(original) == 1
  assert original[0][0] == os.path.basename(image_files[0])

  # preprocess data including annotations
  preprocessed = preprocessor(original, annotations)
  assert isinstance(preprocessed, bob.bio.video.FrameContainer)
  assert len(preprocessed) == 1
  assert preprocessed[0][0] == os.path.basename(image_files[0])
  assert preprocessed[0][2] is None
  assert numpy.allclose(preprocessed[0][1], bob.io.base.load(pkg_resources.resource_filename("bob.bio.face.test", "data/cropped.hdf5")))


def test_detect():
  # load test video
  video_file = pkg_resources.resource_filename("bob.bio.video.test", "data/testvideo.avi")
  frame_selector = bob.bio.video.FrameSelector(max_number_of_frames=3, selection_style="spread")

  preprocessor = bob.bio.video.preprocessor.Wrapper('face-detect', frame_selector, compressed_io=False)
  video = preprocessor.read_original_data(video_file)
  assert isinstance(video, bob.bio.video.FrameContainer)

  preprocessed_video = preprocessor(video)
  assert isinstance(preprocessed_video, bob.bio.video.FrameContainer)

  reference_file = pkg_resources.resource_filename("bob.bio.video.test", "data/preprocessed.hdf5")
  if regenerate_refs:
    preprocessed_video.save(bob.io.base.HDF5File(reference_file, 'w'))
  reference_data = bob.bio.video.FrameContainer(bob.io.base.HDF5File(reference_file, 'r'))

  assert preprocessed_video.is_similar_to(reference_data)


def test_flandmark():

  video_file = pkg_resources.resource_filename("bob.bio.video.test", "data/testvideo.avi")
  frame_selector = bob.bio.video.FrameSelector(max_number_of_frames=3, selection_style="spread")

  preprocessor = bob.bio.video.preprocessor.Wrapper('landmark-detect', frame_selector, compressed_io=False)
  video = preprocessor.read_original_data(video_file)
  assert isinstance(video, bob.bio.video.FrameContainer)

  preprocessed_video = preprocessor(video)
  assert isinstance(preprocessed_video, bob.bio.video.FrameContainer)

  reference_file = pkg_resources.resource_filename("bob.bio.video.test", "data/preprocessed-flandmark.hdf5")
  if regenerate_refs:
    preprocessed_video.save(bob.io.base.HDF5File(reference_file, 'w'))
  reference_data = bob.bio.video.FrameContainer(bob.io.base.HDF5File(reference_file, 'r'))

  assert preprocessed_video.is_similar_to(reference_data)
