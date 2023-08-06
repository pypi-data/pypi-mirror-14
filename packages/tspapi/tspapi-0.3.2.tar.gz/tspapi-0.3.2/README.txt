

BMC TRUESIGHT PULSE API FOR PYTHON


TrueSight Pulse API for Python provides bindings for the python language

Visit http://boundary.github.io/pulse-api-python for installation and
usage instructions.

[Build Status]

© Copyright 2005-2016 BMC Software, Inc. Use of this software signifies
your acceptance of BMC's Terms of Use, Privacy Policy and Cookie Notice.
BMC, BMC Software, the BMC logos, and other BMC marks are trademarks or
registered trademarks of BMC Software, Inc. in the U.S. and/or certain
other countries.


Examples

Create a Metric

Create a Measurement

    import tspapi

    # The following assumes the following environment variables are set
    # export TSP_EMAIL='joe@example.com'
    # export TSP_API_TOKEN=<your api token>
    api = tspapi.API()

    metric = api.measurement_create(metric='MY_METRIC', source='MySource', value=3.14)
