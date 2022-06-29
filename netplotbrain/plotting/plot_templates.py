import numpy as np
import nibabel as nib
import os
import templateflow.api as tf
from scipy.ndimage import rotate, sobel
from scipy.ndimage.interpolation import spline_filter1d
from nibabel.processing import resample_to_output
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure, segmentation
from ..templatesettings import _get_surface_level_for_template


def _plot_template_style_cloudy(ax, data, azim, elev, **kwargs):
    # Get kewyowrd argments relevant for function
    alpha = kwargs.get('templatealpha')
    edgethreshold = kwargs.get('templateedgethreshold')
    templatecolor = kwargs.get('templatecolor')
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
    ax.scatter(x, y, z, s=5, facecolor=templatecolor,
               edgecolors=None, marker='s', alpha=alpha, rasterized=True)



def _plot_template_style_glass(ax, data, **kwargs):
    """
    This style plots the borders after a quick segmentation resulting in a glass or smokey brain

    Relevant kwargs

    template_glass_compactness : float
        Default 0.3. Going lower will increase the detail. >1 will break the figure.
    temlate_glass_nsegments : int
        Approx number of segments. 3 seems to work well.
        Increase if not enough detail, reduce if too much detail.
    template_glass_maxalpha : float
        Default is 0.01. To make the smokey effect the alpha is relative to template intensity value.
        This value sets the alpha scalar factor.
        The value will be the largest possible alpha value, where all other values scale between 0 and template_glass_max_alpha.
    templatecolor : string
        Color of image.

    """
    #Get kwargs
    template_glass_compactness = kwargs.get('template_glass_compactness')
    template_glass_nsegments = kwargs.get('template_glass_nsegments')
    template_glass_maxalpha = kwargs.get('template_glass_maxalpha')
    templatecolor= kwargs.get('templatecolor')

    # perform segmentation.
    segments = segmentation.slic(data, template_glass_nsegments,
                                 compactness=template_glass_compactness,
                                 enforce_connectivity=False,
                                 start_label=1,
                                 channel_axis=None)
    borders = segmentation.find_boundaries(segments, mode='thick')

    # Scale the alpha of the border values based on template intensity
    data[~borders] = 0
    points = np.where(data!=0)
    border_vals = data[points[0], points[1], points[2]]
    alpha_per_point = (border_vals - border_vals.min()) / (border_vals.max() - border_vals.min())

    ax.scatter(points[0], points[1], points[2], s=0.2, alpha=alpha_per_point * template_glass_maxalpha, color=templatecolor)



def _plot_template_style_filled(ax, data, **kwargs):
    alpha = kwargs.get('templatealpha')
    templatecolor = kwargs.get('templatecolor')
    ax.voxels(data, alpha=alpha, zorder=-100,
              facecolor=templatecolor, edgecolor=None, shade=False, rasterized=True)


def _plot_template_style_surface(ax, data, template, **kwargs):
    """Uses the function skimage.measure.marching_cubes to identify a surface.

    Relevant kwargs
    ----------------

    surface_resolution : int
        The resolution of the surface (see argument step_size in marching_cubes)
    surface_detection : float
        The value used to detect the surface boundrary (see argument level in marching_cubes).
        Some default choices are made for various templates
    """
    # get kwargs
    alpha = kwargs.get('templatealpha')
    templatecolor = kwargs.get('templatecolor')
    surface_detection = kwargs.get('surface_detection')
    surface_resolution = kwargs.get('surface_resolution')
    if surface_detection is None:
        surface_detection = _get_surface_level_for_template(template)
    # detect surface using skimage's marching cubes
    verts, faces, _, _ = measure.marching_cubes(
        data, level=surface_detection, step_size=surface_resolution)
    mesh = Poly3DCollection(verts[faces], rasterized=True)
    mesh.set_facecolor(templatecolor)
    mesh.set_alpha(alpha)
    ax.add_collection3d(mesh)


def _select_single_hemisphere_template(data, hemisphere):
    """Selects the left or right hemispehre by using the midway point on the x-axis.

    This assumes left hemispehre is orientated on the left.
    """
    midpoint = int(data.shape[0] / 2)
    if hemisphere == 'right' or hemisphere == 'R':
        data[:midpoint] = 0
    elif hemisphere == 'left' or hemisphere == 'L':
        data[midpoint:] = 0
    return data


def _plot_template(ax, style='filled', template='MNI152NLin2009cAsym',
                   voxsize=None, azim=0, elev=0, hemisphere='both', **kwargs):
    if isinstance(template, dict):
        template = tf.get(**template)

    if isinstance(template, str):
        if not os.path.exists(template):
            tf_kwargs = {'resolution': 1}
            # Add kwargs to specify specific templates
            if 'MNI152' in template or 'OASIS' in template:
                tf_kwargs['suffix'] = 'T1w'
            # If cohort is in the name as template=templateame_cohort-X, split to template=tempaltename, and 'cohort' is in tf_kwargs  
            if '_cohort-' in template:
                cohort = template.split('cohort-')[1]
                tf_kwargs['cohort'] = cohort
                template = template.split('_')[0]

            template = tf.get(template=template, desc='brain',
                              extension='.nii.gz', **tf_kwargs)
          
    # If template is now a list then templateflow found multiple entries.
    if isinstance(template, list):
        print('More than 1 template found. Please provide more arguments to specify the template you want.')
        for t in template:
            print(t.name)
        raise ValueError('More than one template found')

    img = nib.load(template)

    if voxsize is not None:
        img = resample_to_output(img, [voxsize] * 3)
    data = img.get_fdata()
    data = _select_single_hemisphere_template(data, hemisphere)
    if style == 'filled':
        _plot_template_style_filled(ax, data, **kwargs)
    elif style == 'cloudy':
        _plot_template_style_cloudy(
            ax, data, azim, elev, **kwargs)
    elif style == 'surface':
        _plot_template_style_surface(
            ax, data, template, **kwargs)
    elif style == 'glass':
        _plot_template_style_glass(ax, data, **kwargs)
    # Set xyz lim (for regardless of templatestyle)
    ax.set_xlim(0, data.shape[0])
    ax.set_ylim(0, data.shape[1])
    ax.set_zlim(0, data.shape[2])
    return img.affine
