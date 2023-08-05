"""
This module implements a set of
:class:`~revscoring.Datasource`
processors that represent the input data for extracting
:class:`~revscoring.Feature` values.  Just like
:class:`~revscoring.Feature` and other
:class:'~revscoring.dependencies.Dependent' processors,
:class:`~revscoring.Datasource` processors are tended to
be :func:`~revscoring.dependencies.solve` as dependencies. The
provided datasources are split conceptually into a set of modules:

* :mod:`revscoring.datasources.diff`
* :mod:`revscoring.datasources.page_creation`
* :mod:`revscoring.datasources.parent_revision`
* :mod:`revscoring.datasources.previous_user_revision`
* :mod:`revscoring.datasources.revision`
* :mod:`revscoring.datasources.site`
* :mod:`revscoring.datasources.user`

diff
++++
.. automodule:: revscoring.datasources.diff
    :members:

page_creation
+++++++++++++
.. automodule:: revscoring.datasources.page_creation
    :members:

parent_revision
+++++++++++++++
.. automodule:: revscoring.datasources.parent_revision
    :members:

parent_user_revision
++++++++++++++++++++
.. automodule:: revscoring.datasources.previous_user_revision
    :members:

revision
++++++++
.. automodule:: revscoring.datasources.revision
    :members:

site
++++
.. automodule:: revscoring.datasources.site
    :members:

user
++++
.. automodule:: revscoring.datasources.user
    :members:

datasource
++++++++++
.. automodule:: revscoring.datasources.datasource

types
+++++
.. automodule:: revscoring.datasources.types


"""
from .datasource import Datasource
from .types import RevisionMetadata, UserInfo

__all__ = [Datasource, RevisionMetadata, UserInfo]
