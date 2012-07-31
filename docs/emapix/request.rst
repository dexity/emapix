.. _request:

Photo Request
=============

Photo Request Methods
---------------------

Make Request View
~~~~~~~~~~~~~~~~~

Make request view.

.. list-table::
   :widths: 30 10 10 10
   :header-rows: 1

   * - Endpoint
     - HTTP Method
     - Authentication
     - HTTPS
   * - ``/request/make``
     - GET
     - no
     - no

Request Form
~~~~~~~~~~~~

Photo request form.

.. list-table::
   :widths: 30 10 10 10
   :header-rows: 1

   * - Endpoint
     - HTTP Method
     - Authentication
     - HTTPS
   * - ``/request/add``
     - GET,POST
     - yes
     - yes

**Parameters:**

.. list-table::
   :widths: 10 10 30
   :header-rows: 1

   * - Parameter
     - Required
     - Description
   * - lat
     - yes
     - Latitude
   * - lon
     - yes
     - Longitude
   * - description
     - no
     - Request description
  
..  
    **Example:**
    Parameters::
    Request URL::
        https://HOSTNAME/services/user/service/add
    Request Body::



