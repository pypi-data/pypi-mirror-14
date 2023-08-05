__author__ = 'roland'

from saml2.extension import mdui

display_name = mdui.DisplayName(text="example.com")
description = mdui.Description(text="Example.com")

uiinfo = mdui.UIInfo(display_name=display_name, description=description)
uiinfo.register_prefix({"mdui": mdui.NAMESPACE})

print(uiinfo)
