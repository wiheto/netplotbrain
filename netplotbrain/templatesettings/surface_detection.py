
def _get_surface_level_for_template(template):
    """
    Default values for different templates.

    Only templates that differ from default (average between min/max value) need to be specified.
    And these can generally be 1.
    An important part in the surface detectoin is what the 0 values are.
    print(template in templates_with_one_surfacedetect)
    print(template)
    print(templates_with_one_surfacedetect)
    If they are 0, then this value can generally be 1.

    This can be fine tuned more!
    Perhaps it can be automated as well in order to not have to constantly curate.

    """

    surface_detection = None

    templates_with_one_surfacedetect = [
        'OASIS30ANTs'
    ]

    if template in templates_with_one_surfacedetect:
        surface_detection = 1

    return surface_detection