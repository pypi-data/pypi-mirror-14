==============
Access Control
==============

Text Content
------------

Text content access control is handled slightly differently than
endpoint, type, and attribute access. Unlike those, text content
sections are only restricted if, and only if, they have AT LEAST ONE
docorator, in which case the user must have access to the specified
access group. For example, given the following two paragraphs:

.. code:: text

  Lorem ipsum dolor sit amet, consectetur adipiscing elit.

  @BETA: Sed sit amet metus aliquet. Scelerisque augue quis, auctor
  eros. Sed ut arcu semper, suscipit sem eu.

The first paragraph will be visible to *everyone*, but the second
paragraph will only be visible to members that have access to "@BETA"
docorators.
