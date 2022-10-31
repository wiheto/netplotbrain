from netplotbrain import plot as npbplot
import pytest

# Plot only cloudy template
@pytest.mark.mpl_image_compare
def test_cloudytemplate():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='cloudy',
                      view='SIP',
                      template_voxelsize=2)
    return fig

# Plot only filled template
@pytest.mark.mpl_image_compare
def test_filledtemplate():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                      template_style='filled',
                      view='L',
                      template_voxelsize=5)
    return fig


# Plot only filled template
@pytest.mark.mpl_image_compare
def test_glasstemplate():
    fig, _ = npbplot(template='MNI152NLin2009cAsym',
                     template_style='glass',
                     view=['AP', 'SL'])
    return fig
