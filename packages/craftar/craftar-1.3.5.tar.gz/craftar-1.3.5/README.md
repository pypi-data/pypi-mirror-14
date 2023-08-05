# CraftAR Python Library

## Description

The CraftAR Service for [Augmented Reality and Image Recognition](http://catchoom.com/product/craftar/augmented-reality-and-image-recognition/) is a  service
that allows you to build a wide range of __Image Recognition__ and __Augmented Reality__ applications
and services.

With CraftAR, you can create amazing apps that provide digital content
for real-life objects like printed media, packaging among others. You
can use our online web panel or APIs, to upload images to be recognized and set
content to display upon recognition in your CraftAR-powered app.

This client library provides access to CraftAR APIs:
- [CraftAR Image Recognition API]
(http://catchoom.com/documentation/api/recognition/)
  allows image recognition against one of your _collections_ of _reference images_ specified using the collection _token_.
- [CraftAR Management API]
(http://catchoom.com/documentation/api/management/)
  allows upload and management of _collections_ of _reference images_, and associated meta-data such as _Augmented Reality experiences_ and their content.
  All requests must be authenticated using your _Management API key_.

The library also provides tools for performing batch operations:
- [craftar_search](bin/craftar_search), for Image Recognition.
- [craftar_upload](bin/craftar_upload), for batch upload of images.


## Installation

If you already have [Python](http://www.python.org/) and [pip](http://www.pip-installer.org/) on your system you can install the library simply by running:

    pip install craftar

In case you first need to install Python or pip, please follow specific instructions for your operating system.

### Windows

On Windows we recommend using the library within [Cygwin](http://www.cygwin.com), which provides a Linux look and feel environment:

1. Download [Cywin installer from the official page](http://cygwin.com/install.html).
2. In the installer wizard, select all python packages, and libmpfr-devel (under libs category).
3. Open the Cygwin shell and execute the following commands:
<pre><code>easy_install pip
pip install craftar
</code></pre>

### Mac OS X

Python comes pre-installed on Mac OS X, so typically you only need to add pip:

    easy_install pip
    pip install craftar

## Dependencies

- [Requests](https://github.com/kennethreitz/requests)
- [Pillow](https://github.com/python-imaging/Pillow)


## Quick Start

Follow these steps to create a _collection_ with one _item_ and perform
an image recognition request against that collection.  A _collection_ is a set
of _items_ representing entities that you want to recognize. Examples of _items_ 
are logos, physical objects, or a drawings, among others.
You can do it directly from your python interpreter.

1. Get [your management api_key](https://my.craftar.net/api_access/).
This is needed to authenticate your requests to the Management API.
    
    ```python
    import craftar
    
    # use your own api_key!
    api_key = "35d5919334816e239bba08637e6aa457e8ca92c8"
    ```
    
2. Create a new _collection_.
    
    ```python
    name = "My cool colection" # use your own collection name
    collection = craftar.create_collection(api_key, name)
    ```

3. Keep the _token_ of that _collection_, you will need it later for
the recognition:

    ```python
    token_list = craftar.get_token_list(api_key, limit=1, offset=0,
                                        collection=collection["uuid"])
    token = token_list[0]["token"] # first token on the list
    ```

4. Create an empty _item_ in your _collection_:

    ```python
    name = "My cool item" # use your own item name
    url = "http://example.com" # and your own url
    custom = "This is my custom data" # and your own custom data
    item = craftar.create_item(api_key, collection["uuid"], name, url, custom)
    ```

5. Upload an _image_ representing your _item_.
  - Every _item_ can be represented by one or more reference _images_.
    This is useful for _items_ that have different faces, e.g. cereal boxes.
  - Before performing a successful recognition, the corresponding reference
    _image_ needs to be fully indexed by the server. Normally it takes
    less than one second after uploading.

    ```python
    filename = "reference.jpg" # use your own image
    image = craftar.create_image(api_key, item["uuid"], filename)
    ```

6. Now you are ready to perform the image recognition request against your collection.
  - You will also need the _token_ you saved in step 3 and the image to be recognized.

    ```python
    # remember that you set _token_ in step 3
    filename = "query.jpg" # use your own query image
    result_list = craftar.search(token, filename)
    ```

7. Done! You can print the result:

    ```python
    print result_list
    ```
   - Each returned reference _image_ has an associated _score_,
     indicating its relevancy to the query image.


## Scripts

The scripts under [/bin](bin) allow batch operations against the APIs:
- [craftar_search](bin/craftar_search) sends one or several Image Recognition
  requests against the CraftAR Service.
  Specifically, it performs visual scans against the _collection_
  (specified by the _token_) using every image in the provided directory.
- [craftar_upload](bin/craftar_upload) uploads a set of reference _images_
  to the CraftAR Service. It iterates over the contents of
  the specified directory and uploads all the images (and, if provided,
  also their associated metadata) to a new or an existing _collection_.


## Examples

In order to see reference implementations demonstrating the most common
operations that can be performed with our APIs check the scripts
under the [examples](examples) folder:
- [example_list_paginated_items](examples/example_list_paginated_items.py):
  Lists all your _items_. If required, the listed _items_ can be limited
  to a specific _collection_.
- [example_management](examples/example_management.py): Demonstrates listing,
  creation, updating and deletion of every type of object (i.e. _collection_,
  _item_, _image_, _token_).

For the reference implementation of the recognition operation see
the script [craftar_search](bin/craftar_search) script under [/bin](bin).

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file
them [here](https://github.com/Catchoom/craftar-python/issues) or contact us
at [support@catchoom.com](mailto:support@catchoom.com).
