#  (C) Catchoom Technologies S.L.
#  Licensed under the MIT license.
#  https://github.com/catchoom/craftar-python/blob/master/LICENSE
#  All warranties and liabilities are disclaimed.

"Provides functions for accessing the CraftAR's management API."

from craftar._common import _get_object_list, _get_object, _create_object, \
    _create_object_multipart, _update_object, _update_object_multipart,  \
    _delete_object
from craftar import settings


def _get_object_uri(object_type, uuid):
    return "/api/%s/%s/%s/" % (settings.MANAGEMENT_API_VERSION,
                               object_type, uuid)


# Collections
def get_collection_list(api_key, limit, offset):
    "Return a list of collections, paginated by @limit and @offset"
    return _get_object_list(api_key, "collection", limit, offset, filter=None)


def get_collection(api_key, uuid):
    "Return a collection, identified by @uuid"
    return _get_object(api_key, "collection", uuid)


def create_collection(api_key, name, offline=False):
    "Create a collection with a given @name (must be unique)"
    data = {'name': name, 'offline': offline}
    return _create_object(api_key, "collection", data)


def update_collection(api_key, uuid, name=None):
    "Update the collection name, identified by @uuid"
    data = {}
    if name is not None:
        data["name"] = name
    return _update_object(api_key, "collection", uuid, data)


def delete_collection(api_key, uuid):
    "Delete a collection, identified by @uuid"
    return _delete_object(api_key, "collection", uuid)


# Items
def get_item_list(api_key, limit, offset, collection=None):
    """Return a list of items, paginated by @limit and @offset
    Filter by @collection"""
    return _get_object_list(api_key, "item", limit, offset, filter=collection)


def get_item(api_key, uuid):
    "Return an item, identified by @uuid"
    return _get_object(api_key, "item", uuid)


def create_item(api_key, collection, name, url=None, custom=None,
                trackable=None, content=None, tags=None):
    """Create a collection with a given @name, belonging to @collection.
    The fields @url, @custom, @trackable and @content are optional."""
    data = {
        'collection': _get_object_uri('collection', collection),
        'name': name,
    }
    if url is not None:
        data['url'] = url
    if custom is not None:
        data['custom'] = custom
    if trackable is not None:
        data['trackable'] = trackable
    if content is not None:
        data['content'] = content
    if tags is not None:
        data['tags'] = map(lambda uuid: _get_object_uri('tag', uuid), tags)

    return _create_object(api_key, "item", data)


def update_item(api_key, uuid, name=None, url=None, custom=None,
                trackable=None, content=None, tags=None):
    "Update an item, identified by @uuid"
    data = {}
    if name is not None:
        data["name"] = name
    if url is not None:
        data["url"] = url
    if custom is not None:
        data["custom"] = custom
    if trackable is not None:
        data['trackable'] = trackable
    if content is not None:
        data['content'] = content
    if tags is not None:
        data['tags'] = map(lambda uuid: _get_object_uri('tag', uuid), tags)

    return _update_object(api_key, "item", uuid, data)


def delete_item(api_key, uuid):
    "Delete an item, identified by @uuid"
    return _delete_object(api_key, "item", uuid)


# Images
def get_image_list(api_key, limit, offset, item=None):
    """Return a list of images, paginated by @limit and @offset
    Filter by @item"""
    return _get_object_list(api_key, "image", limit, offset, filter=item)


def get_image(api_key, uuid):
    "Return an image, identified by @uuid"
    return _get_object(api_key, "image", uuid)


def create_image(api_key, item, filename):
    "Create an image from a @filename, belongs to @item"
    files = {'file': open(filename, 'rb')}
    data = {'item': _get_object_uri('item', item)}

    return _create_object_multipart(api_key, "image", files, data)


def update_image(api_key, uuid, filename):
    "Update the image file, identified by @uuid"
    files = {'file': open(filename, 'rb')}
    return _update_object_multipart(api_key, "image", uuid, files, None)


def delete_image(api_key, uuid):
    "Delete an image, identified by @uuid"
    return _delete_object(api_key, "image", uuid)


# Tokens
def get_token_list(api_key, limit, offset, collection=None):
    """Return a list of tokens, paginated by @limit and @offset.
    Filter by @collection"""
    return _get_object_list(api_key, "token", limit, offset,
                            filter=collection)


def create_token(api_key, collection):
    "Create a token, belongs to @collection"
    data = {'collection': _get_object_uri('collection', collection)}

    return _create_object(api_key, "token", data)


def delete_token(api_key, token):
    "Delete a token, identified by @token"
    return _delete_object(api_key, "token", token)


# Media objects
def get_media_list(api_key, limit, offset):
    """Return a list of media objects, paginated by @limit and @offset"""
    return _get_object_list(api_key, "media", limit, offset)


def get_media(api_key, uuid):
    "Return a media object, identified by @uuid"
    return _get_object(api_key, "image", uuid)


def create_media(api_key, filename):
    "Create a media object from a @filename, belongs to @item"
    files = {'file': open(filename, 'rb')}

    return _create_object_multipart(api_key, "image", files)


def delete_media(api_key, uuid):
    "Delete an image, identified by @uuid"
    return _delete_object(api_key, "image", uuid)


# Tags
def get_tag_list(api_key, limit, offset, collection=None):
    """Return a list of tags, paginated by @limit and @offset
    Filter by @collection"""
    return _get_object_list(api_key, "tag", limit, offset, filter=collection)


def get_tag(api_key, uuid):
    "Return an item, identified by @uuid"
    return _get_object(api_key, "tag", uuid)


def create_tag(api_key, collection, name):
    """Create a tag with a given @name, belonging to @collection."""
    data = {
        'collection': _get_object_uri('collection', collection),
        'name': name,
    }

    return _create_object(api_key, "tag", data)


def delete_tag(api_key, uuid):
    "Delete a tag, identified by @uuid"
    return _delete_object(api_key, "tag", uuid)


# Applications
def get_app_list(api_key, limit, offset):
    """Return a list of applications, paginated by @limit and @offset
    Filter by @collection"""
    return _get_object_list(api_key, "app", limit, offset)


def get_app(api_key, uuid):
    "Return an application, identified by @uuid"
    return _get_object(api_key, "app", uuid)


def create_app(api_key, collection, name):
    """Create an application with a given @name, belonging to @collection."""
    data = {
        'collection': _get_object_uri('collection', collection),
        'name': name,
    }

    return _create_object(api_key, "app", data)


def delete_app(api_key, uuid):
    "Delete an application, identified by @uuid"
    return _delete_object(api_key, "app", uuid)


# SDK Versions
def get_version_list(api_key, limit, offset):
    """Return a list of SDK versions, paginated by @limit and @offset
    Filter by @collection"""
    return _get_object_list(api_key, "version", limit, offset)


def get_version(api_key, uuid):
    "Return an SDK Version, identified by @uuid"
    return _get_object(api_key, "version", uuid)


# Collection Bundles
def get_bundle_list(api_key, limit, offset):
    """Return a list of bundles, paginated by @limit and @offset
    Filter by @collection"""
    return _get_object_list(api_key, "collectionbundle", limit, offset)


def get_bundle(api_key, uuid):
    "Return a bundle, identified by @uuid"
    return _get_object(api_key, "collectionbundle", uuid)


def create_bundle(api_key, collection, app, version, tag=None):
    """Create a bundle with a given @name, belonging to @collection."""
    data = {
        "collection": collection,
        "version": version,
        "app": app,
    }
    if tag:
        data["tag"] = tag

    for object_type, uuid in data.items():
        data[object_type] = _get_object_uri(object_type, uuid)

    return _create_object(api_key, "collectionbundle", data)


def delete_bundle(api_key, uuid):
    "Delete a bundle, identified by @uuid"
    return _delete_object(api_key, "collectionbundle", uuid)
