"""
Annalist user record

A user is represented in a collectionm by:
- an ID (slug)
- a URI (currently a mailto: URI)
- a label (full name)
- a description
- a list of permissions applicable to the collection
- ...

The ID and URI must be matched by the authenticated issuer of an HTTP request for the
permissionms to be applied.  Other fields are cosmetic.
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os
import os.path
import urlparse
import shutil

import logging
log = logging.getLogger(__name__)

from django.conf import settings

from annalist                   import layout
from annalist.exceptions        import Annalist_Error
from annalist.identifiers       import ANNAL
from annalist                   import util
from annalist.models.entity     import Entity
from annalist.models.entitydata import EntityData

class AnnalistUser(EntityData):

    _entitytype     = ANNAL.CURIE.User
    _entitytypeid   = "_user"
    _entityview     = layout.COLL_USER_VIEW
    _entitypath     = layout.COLL_USER_PATH
    _entityfile     = layout.USER_META_FILE
    _entityref      = layout.META_USER_REF
    _contextref     = layout.USER_CONTEXT_FILE

    def __init__(self, parent, type_id):
        """
        Initialize a new AnnalistUser object, without metadata (yet).

        parent      is the parent entity from which the type is descended.
        type_id     the local identifier for the record type
        altparent   is a site object to search for this new entity,
                    allowing site-wide AnnalistUser values to be found.
        """
        super(AnnalistUser, self).__init__(parent, type_id)
        # log.debug("AnnalistUser %s: dir %s"%(type_id, self._entitydir))
        # log.debug("AnnalistUser %s: url %s, viewurl %s"%(type_id, self._entityurl, self._entityviewurl))
        return

# End.
