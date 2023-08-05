from indicoio.utils.api import api_handler
from indicoio.utils.decorators import detect_batch_decorator


@detect_batch_decorator
def named_entities(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns named entities (proper nouns) found in the text

    Example usage:

    .. code-block:: python

       >>> text = "London Underground's boss Mike Brown warned that the strike ..."
       >>> entities = indicoio.named_entities(text)
       {u'London Underground': {u'categories': {u'location': 0.583755654607989,
          u'organization': 0.07460487821791033,
          u'person': 0.07304850776658672,
          u'unknown': 0.2685909594075139},
         u'confidence': 0.846188063604044},
        u'Mike Brown': {u'categories': {u'location': 0.025813884950623898,
          u'organization': 0.06661470013014613,
          u'person': 0.08723850624560824,
          u'unknown': 0.8203329086736217},
         u'confidence': 0.8951793008234012}}

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of named entity probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(text, cloud=cloud, api="namedentities", url_params=url_params, **kwargs)


@detect_batch_decorator
def people(text, cloud=None, batch=None, api_key=None, version=None, **kwargs):
    """
    Given input text, returns references to specific persons found in the text

    Example usage:

    .. code-block:: python

       >>> text = "London Underground's boss Mike Brown warned that the strike ..."
       >>> entities = indicoio.people(text)
        [
          {
            u'text': "Mike Brown",
            u'confidence': 0.09470917284488678,
            u'position': [26, 36]
          },
          ...
        ]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(text, cloud=cloud, api="people", url_params=url_params, **kwargs)


@detect_batch_decorator
def places(text, cloud=None, batch=None, api_key=None, version=None, **kwargs):
    """
    Given input text, returns references to specific places found in the text

    Example usage:

    .. code-block:: python

       >>> text = "London Underground's boss Mike Brown warned that the strike ..."
       >>> entities = indicoio.places(text)
        [
          {
            u'text': "London",
            u'confidence': 0.18549786508083344,
            u'position': [0, 6]
          },
          ...
        ]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(text, cloud=cloud, api="places", url_params=url_params, **kwargs)



@detect_batch_decorator
def organizations(text, cloud=None, batch=None, api_key=None, version=None, **kwargs):
    """
    Given input text, returns references to specific organizations found in the text

    Example usage:

    .. code-block:: python

       >>> text = "London Underground's boss Mike Brown warned that the strike ..."
       >>> entities = indicoio.organizations(text)
        [
          {
            u'text': "London Underground",
            u'confidence': 0.8643872141838074,
            u'position': [0, 18]
          }
        ]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(text, cloud=cloud, api="organizations", url_params=url_params, **kwargs)
