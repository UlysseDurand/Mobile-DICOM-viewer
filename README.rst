Mobile medical patient review
----------------------------------------

A mobile web application for doctors to review DICOM images


Installation
----------------------------------------

This application is not published on PyPI and depends on local editable
checkouts (see below), so it must be installed from a local clone.

.. code-block:: console

    git clone <this repository>
    cd mobile-medical-patient-review

The application requires Python 3.12 (or <=3.13): ``slicer-core`` does not
ship wheels for newer Python versions.

Local dependency checkouts (``file://`` paths in ``pyproject.toml``) must
exist at:

* ``/home/ulysse-durand/git/trame-rca``
* ``/home/ulysse-durand/git/vtk-fixed``

Run the application

.. code-block:: console

    mobile-medical-patient-review

Then open ``http://localhost:8080/`` in a browser.

Development setup
----------------------------------------

We recommend using uv for setting up and managing a virtual environment for your development.

.. code-block:: console

    # Create venv and install all dependencies (MUST pin Python 3.12)
    uv sync --all-extras --dev --python 3.12

    # Activate environment
    source .venv/bin/activate


Build and install the Vue components

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

This is only needed when you modify the ``vue-components/`` sources or
package the application (the app itself runs fine without the Vue build).


Docker
----------------------------------------

.. code-block:: console

    docker build -t mobile-medical-patient-review -f ./examples/docker/Dockerfile .
    docker run -it --rm -p 8080:80 mobile-medical-patient-review


Sample data
----------------------------------------

Sample DICOM volumes are in ``volumes/`` (``ct_chest_dcm/``, ``mr_head_dcm/``)
and are stored with git LFS (see ``.gitattributes``).


Professional Support
----------------------------------------

* `Training <https://www.kitware.com/courses/trame/>`_: Learn how to efficiently use trame from the expert developers at Kitware.
* `Support <https://www.kitware.com/trame/support/>`_: Our experts can assist your team as you build your web application and establish in-house expertise.
* `Custom Development <https://www.kitware.com/trame/support/>`_: Leverage Kitware’s 25+ years of experience to quickly build your web application.
