from netplotbrain import plot as npbplot
import pytest

# Plot only cloudy template
@pytest.mark.mpl_image_compare
def test_cloudytemplate():
    fig, ax = npbplot(template='MNI152NLin2009cAsym',
                      templatestyle='cloudy',
                      view='SIP',
                      templatevoxsize=2)
    return fig

# Plot only filled template
@pytest.mark.mpl_image_compare
def test_filledtemplate():
    fig, ax = npbplot(template='MNI152NLin2009cAsym',
                      templatestyle='filled',
                      view='L',
                      templatevoxsize=5)
    return fig
