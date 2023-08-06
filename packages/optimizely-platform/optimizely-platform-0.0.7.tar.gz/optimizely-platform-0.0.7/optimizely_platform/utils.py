from itertools import islice


def chunkify(items, chunk_size):
  """Breaks items into evenly-sized chunks.

  Args:
    items: a list of items of any data type
    chunk_size: the number of items to yield as a chunk
  """
  items = iter(items)
  chunk = list(islice(items, chunk_size))

  while chunk:
    yield chunk
    chunk = list(islice(items, chunk_size))
