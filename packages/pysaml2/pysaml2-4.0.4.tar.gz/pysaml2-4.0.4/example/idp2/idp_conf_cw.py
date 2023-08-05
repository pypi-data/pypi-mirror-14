#!/usr/bin/env python
# -*- coding: utf-8 -*-
from saml2 import BINDING_HTTP_REDIRECT
from saml2 import BINDING_SOAP
from saml2.saml import NAME_FORMAT_URI
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NAMEID_FORMAT_PERSISTENT
import os.path

try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None

if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary(["/opt/local/bin"])
else:
    xmlsec_path = '/usr/bin/xmlsec1'

BASEDIR = os.path.dirname(os.path.dirname(__file__))


def full_path(local_file):
    return os.path.join(BASEDIR, local_file)

# HOST = "staging.sso-simple.org"
# PORT = 80

HOST = "localhost"
PORT = 5000

BASE = "http://%s:%s" % (HOST, PORT)
# BASE = "http://%s" % HOST


CONFIG = {
    "entityid": "%s/metadata.xml" % BASE,
    "description": "CarrierWave IDP",
    "valid_for": 168,
    "service": {
        "idp": {
            "name": "CarrierWave IdP",
            "endpoints": {
                "single_sign_on_service": [
                    ("%s/sso/redirect/" % BASE, BINDING_HTTP_REDIRECT)
                ],
                "single_logout_service": [
                    ("%s/slo/soap/" % BASE, BINDING_SOAP),
                ]
            },
            "policy": {
                "default": {
                    "lifetime": {"minutes": 15},
                    "attribute_restrictions": None,
                    "name_format": NAME_FORMAT_URI,
                    "entity_categories": ["swamid", "edugain"]
                },
            },
            "subject_data": "./idp.subject",
            "name_id_format": [NAMEID_FORMAT_TRANSIENT, NAMEID_FORMAT_PERSISTENT]
        },
    },
    "debug": 1,
    "key_file": full_path("idp2/pki/mykey.pem"),
    "cert_file": full_path("idp2/pki/mycert.pem"),
    "metadata": {
        "remote": [{
            'url': 'http://example-sp.carrierwave.com/wordpress/wp-content/plugins/saml-20-single-sign-on/saml/www/module.php/saml/sp/metadata.php/1'
        }]
    },
    "organization": {
        "display_name": "CarrierWave",
        "name": "CarrierWave",
        "url": "http://www.carrierwave.com",
    },
    "contact_person": [{
        "contact_type": "technical",
        "given_name": "Russel",
        "sur_name": "Mahmud",
        "email_address": "russel_1237@hotmail.com"
    }, {
        "contact_type": "support",
        "given_name": "Support",
        "email_address": "adrian@carrierwave.com"
    }],
    "xmlsec_binary": xmlsec_path
}