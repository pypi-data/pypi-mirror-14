from saml2 import config

from saml2.mdstore import MetadataStore
from saml2.attribute_converter import ac_factory

from pathutils import full_path

__author__ = 'roland'

sec_config = config.Config()

ATTRCONV = ac_factory(full_path("attributemaps"))

METADATACONF = {
    # "2": [{
    #     "class": "saml2.mdstore.MetaDataExtern",
    #     "metadata": [
    #         (
    #         'http://example-sp.carrierwave.com/wordpress/wp-content/plugins'
    #         '/saml-20-single-sign-on/saml/www/module.php/saml/sp/metadata.php'
    #         '/1',
    #         full_path("inc-md-cert.pem"))]
    # }],
    "10": [{
        "class": "saml2.mdstore.MetaDataExtern",
        "metadata": [
            ("http://md.incommon.org/InCommon/InCommon-metadata-export.xml",
             full_path("inc-md-cert.pem"))]
    }
    ]
}


# def test_cert_no_signature():
#     mds = MetadataStore(ATTRCONV, sec_config,
#                         disable_ssl_certificate_validation=True)
#
#     mds.imp(METADATACONF["2"])
#     assert len(mds.keys()) >= 1


def test_signature_no_cert():
    mds = MetadataStore(ATTRCONV, sec_config,
                        disable_ssl_certificate_validation=True)

    mds.imp(METADATACONF["10"])
    assert len(mds.keys()) > 1

