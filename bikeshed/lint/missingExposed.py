from .. import h, messages as m


def missingExposed(doc):
    """
    Checks that every IDL interface or namespace has an [Exposed] attribute.
    Specifically:
    * Any namespace
    * Any non-callback interface without [NoInterfaceObject]
    * Any callback interface that has constants in it.

    Partials never need to declare [Exposed], I think?
    """
    if not doc.md.complainAbout["missing-exposed"]:
        return

    for construct in doc.widl.constructs:
        if construct.extended_attributes is None:
            extendedAttrs = []
        else:
            extendedAttrs = construct.extended_attributes
        if construct.idl_type == "namespace":
            good = False
            for attr in extendedAttrs:
                if attr.name == "Exposed":
                    good = True
                    break
            if not good:
                m.warn(
                    f"The '{construct.name}' namespace is missing an [Exposed] extended attribute. Does it need [Exposed=Window], or something more?"
                )
        elif construct.idl_type == "interface":
            good = False
            for attr in extendedAttrs:
                if attr.name == "Exposed":
                    good = True
                    break
                if attr.name == "NoInterfaceObject":
                    good = True
                    break
            if not good:
                m.warn(
                    f"The '{construct.name}' interface is missing an [Exposed] extended attribute. Does it need [Exposed=Window], or something more?"
                )
        elif construct.idl_type == "callback":
            if not h.hasAttr(construct, "interface"):
                # Just a callback function, it's fine
                continue
            for _ in construct.interface.members:
                pass
