import numpy as np
import nibabel as nib
import os
import templateflow.api as tf
from scipy.ndimage import rotate, sobel
from scipy.ndimage.interpolation import spline_filter1d
from nibabel.processing import resample_to_output
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure


def _plot_template_style_cloudy(ax, data, azim, elev, edgethreshold):
    # If the viewpoint is not at 0,0, rotate the image so the edge thresholding occurs at approriate angle
    if azim != 0:
        data = rotate(data, -azim, axes=[0, 1], reshape=False)
    if elev != 0:
        data = rotate(data, -elev, axes=[0, 2], reshape=False)
    # Apply sobel filter to ax1 and ax2 (viewpoint will be relative to rorated ax0)
    sdata_ax1, sdata_ax2 = [sobel(data, axis=n) for n in range(1, 3)]
    # Interpolation
    # sdata_ax1 = interpolation.spline_filter(sdata_ax1)
    # sdata_ax2 = interpolation.spline_filter(sdata_ax2)
    # Combine edge thresholding
    sdata = np.hypot(sdata_ax1, sdata_ax2)
    sdata = spline_filter1d(sdata, axis=0)
    # Rotate back
    if elev != 0:
        sdata = rotate(sdata, elev, axes=[0, 2], reshape=False)
    if azim != 0:
        sdata = rotate(sdata, azim, axes=[0, 1], reshape=False)
    # Binarize sobel filter in relation to threshold
    bdata = np.abs(sdata) > np.max(np.abs(sdata)) * edgethreshold
    # Plot resulting edges as a scatter
    x, y, z = np.where(bdata == 1)
    # ax.voxels(bdata, alpha=0.2, edgecolor=None, facecolor='lightgray')
    ax.scatter(x, y, z, alpha=0.1, s=5, facecolor='lightgray',
               edgecolors=None, marker='s')


def _plot_template_style_filled(ax, data, alpha, templatecolor):
    ax.voxels(data, alpha=alpha, zorder=-100,
              facecolor=templatecolor, edgecolor=None, shade=False)


def _plot_template_style_surface(ax, data, alpha, templatecolor='gray', surface_resolution=2):
    verts, faces, _, _ = measure.marching_cubes(
        data, step_size=surface_resolution)
    mesh = Poly3DCollection(verts[faces])
    mesh.set_facecolor(templatecolor)
    mesh.set_alpha(alpha)
    ax.add_collection3d(mesh)
    ax.set_xlim(0, data.shape[0])
    ax.set_ylim(0, data.shape[1])
    ax.set_zlim(0, data.shape[2])


def _select_single_hemisphere_template(data, hemisphere):
    """
    Selects the left or right hemispehre by using the midway point on the x-axis.
    This assumes left hemispehre is orientated on the left.
    """
    midpoint = int(data.shape[0] / 2)
    if hemisphere == 'right' or hemisphere == 'R':
        data[:midpoint] = 0
    elif hemisphere == 'left' or hemisphere == 'L':
        data[midpoint:] = 0
    return data


def _plot_template(ax, style='filled', template='MNI152NLin2009cAsym', templatecolor='lightgray', alpha=0.2, voxsize=2, azim=0, elev=0, surface_resolution=2, edgethreshold=0.8, hemisphere='both'):
    if isinstance(template, str):
        if not os.path.exists(template):
            tf_kwargs = {}
            # Add kwargs to specify specific templates
            if 'MNI152' in template or 'OASIS' in template:
                tf_kwargs = {
                    'suffix': 'T1w',
                    'resolution': 1,
                }
            if 'WHS' in template:
                tf_kwargs = {
                    'resolution': 1,
                }
            template = tf.get(template=template, desc='brain',
                              extension='.nii.gz', **tf_kwargs)
            # If multiple templates still remain, take the first
            # This may lead to suboptimal performence for some templates
            if isinstance(template, list):
                template = template[0]
        img = nib.load(template)
    elif isinstance(template, (nib.Nifti1Image, nib.Nifti2Image)):
        img = template
    img = resample_to_output(img, [voxsize] * 3)
    data = img.get_fdata()
    data = _select_single_hemisphere_template(data, hemisphere)
    if style == 'filled':
        _plot_template_style_filled(ax, data, alpha, templatecolor)
    elif style == 'cloudy':
        _plot_template_style_cloudy(ax, data, azim, elev, edgethreshold)
    elif style == 'surface':
        _plot_template_style_surface(
            ax, data, alpha, templatecolor, surface_resolution)
    return img.affine
