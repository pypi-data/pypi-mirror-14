"""Provides objects used as part of the formal interface between add-on package code and the rest of Optimizely."""


class AudienceConditionOption(object):
  """Class containing the details of an option for an audience condition provided by a third party."""

  def __init__(self, value, text, child_options=None):
    if child_options:
      for option in child_options:
        if type(option) is not AudienceConditionOption:
          raise ValueError('Each provided child option must be an instance of AudienceConditionOption.')

    # Represents the option's value
    self.value = value
    # Represents the option's display text
    self.text = text
    self.child_options = child_options

  def __str__(self):
    return '%s : %s' % (self.text, self.value)

  def __eq__(self, other):
    # TODO(tjones): look at child_options comparison?
    return self.value == other.value and self.text == other.text

  def to_dict(self):
    if self.child_options:
      child_options = [option.to_dict() for option in self.child_options]
    else:
      child_options = None

    return {'value': self.value,
            'text': self.text,
            'child_options': child_options}


class AudienceCondition(object):
  """Class containing the details of an audience condition provided by a third party."""

  # TODO(jon): Strictly enforce that the system_name matches a field in the integration's config.yaml.

  def __init__(self, system_name, options):
    for option in options:
      if type(option) is not AudienceConditionOption:
        raise ValueError('Each provided option must be an instance of AudienceConditionOption.')

    self.system_name = system_name
    self.options = options

  def __str__(self):
    return '%s : [%s]' % (self.system_name, ','.join([str(option) for option in self.options]))

  def __eq__(self, other):
    return self.system_name == other.system_name and self.options == other.options


class VisitorSet(object):
  """Class containing visitor information."""

  def __init__(self, id_type, id_key, ids):
    """Creates the VisitorSet.

    Args:
      id_type: the type of id (see below).
      id_key: unique key used to identify the visitor set.
      ids: a list of ids.

    A valid instantiation might look something like:
      VisitorSet('cookie', '_mkto_trk', {'abc', 'efg', 'xyz'})
    """
    SUPPORTED_ID_TYPES = ['cookie']

    if id_type not in SUPPORTED_ID_TYPES:
      raise ValueError('Invalid id_type specified!')

    self.id_type = id_type
    self.id_key = id_key
    self.ids = ids

  def __eq__(self, other):
    return self.id_type == other.id_type and self.id_key == other.id_key and self.ids == other.ids
