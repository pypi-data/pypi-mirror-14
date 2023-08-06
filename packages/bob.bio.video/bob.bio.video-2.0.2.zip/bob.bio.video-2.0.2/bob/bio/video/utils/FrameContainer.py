import bob.bio.base
import numpy

import logging
logger = logging.getLogger("bob.bio.video")

class FrameContainer:
  """A class for reading, manipulating and saving video content.
  """

  def __init__(self, hdf5 = None, load_function = bob.bio.base.load):
    self._frames = []
    if hdf5 is not None:
      self.load(hdf5, load_function)

  def __len__(self):
    return len(self._frames)

  def __iter__(self):
    """Generator that returns the 3-tuple (frame_id, data, quality) for each frame."""
    # don't sort
    for frame in self._frames:
      yield frame

  def __getitem__(self, i):
    """Indexer (mostly used in tests)."""
    return self._frames[i]

  def add(self, frame_id, frame, quality = None):
    """Adds the frame with the given id and the given quality."""
    self._frames.append((str(frame_id), frame, quality))

  def load(self, hdf5, load_function = bob.bio.base.load):
    self._frames = []
    # Read content (frames) from HDF5File
    for path in hdf5.sub_groups(relative=True, recursive=False):
      # extract frame_id
      if path[:6] == 'Frame_':
        frame_id = str(path[6:])
        hdf5.cd(path)
        # Read data
        data = load_function(hdf5)

        # read quality, if present
        quality = hdf5.read("FrameQuality") if hdf5.has_key("FrameQuality") else None
        self.add(frame_id, data, quality)
        hdf5.cd("..")
    if not len(self):
      raise IOError("Could not load data as a Frame Container from file %s" % hdf5.filename)

  def save(self, hdf5, save_function = bob.bio.base.save):
    """ Save the content to the given HDF5 File.
    The contained data will be written using the given save_function."""
    if not len(self):
      logger.warn("Saving empty FrameContainer '%s'", hdf5.filename)
    for frame_id, data, quality in self:
      hdf5.create_group("Frame_%s" % frame_id)
      hdf5.cd("Frame_%s" % frame_id)
      save_function(data, hdf5)
      if quality is not None:
        hdf5.set("FrameQuality", quality)
      hdf5.cd("..")

  def is_similar_to(self, other):
    if len(self) != len(other): return False
    for a,b in zip(self, other):
      if a[0] != b[0]: return False
      if abs(a[2] - b[2]) > 1e-8: return False
      if not numpy.allclose(a[1], b[1]): return False
    return True

def save_compressed(frame_container, filename, save_function, create_link=True):
  hdf5 = bob.bio.base.open_compressed(filename, 'w')
  frame_container.save(hdf5, save_function)
  bob.bio.base.close_compressed(filename, hdf5, create_link=create_link)
  del hdf5

def load_compressed(filename, load_function):
  hdf5 = bob.bio.base.open_compressed(filename, 'r')
  fc = FrameContainer(hdf5, load_function)
  bob.bio.base.close_compressed(filename, hdf5)
  del hdf5
  return fc
