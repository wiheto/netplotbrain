import nibabel as nib
import templateflow.api as tf
import numpy as np
import pandas as pd
from nibabel.processing import resample_to_output
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
from .plot_templates import _select_single_hemisphere_template
from ..utils import _colorarray_from_string, _rotate_data_to_viewingangle


def _get_nodes_from_nii(img, nodes=None, voxsize=None, template=None):
    """
    Returns xyz coordinates from node input.

    Parameters
    ------------------------
    img : str, nibabel image or dict
        If string, link to the image.
        If img, a nifti where each roi is its own number.
        If dict, templateflow dictionary to one single nifti image
    nodes : dataframe
        Node dataframe.
    voxsize : int
        if not, None, the size of voxels in cord system.

    Returns
    -----------------------
    nodes : dataframe with x,y,z cordinates of nodes
    img : loaded nifti image.
    """
    # Get templateflow image, if dict
    if isinstance(img, dict):
        # Add template to dict
        if template is not None and 'template' not in img:
            img['template'] = template
        # If extension not included in img, add it.
        # Could be some instances where this is not wanted
        if 'extension' not in img:
            img['extension'] = '.nii.gz'
        imgpath = tf.get(**img)
        img = nib.load(imgpath)
    # load image, if string
    if isinstance(img, str):
        img = img.load(str)

    # Resize img to desired output resolution
    # Will be same as template
    if voxsize is not None:
        img = resample_to_output(img, [voxsize] * 3, mode='nearest')

    # Get each roi
    imgdata = img.get_fdata(caching='unchanged')
    rois = np.unique(imgdata)
    # remove 0 roi (i.e. background)
    rois = rois[rois != 0]
    x_coord = []
    y_coord = []
    z_coord = []
    for r in rois:
        allcoords = np.where(imgdata == r)
        x_coord.append(np.median(allcoords[0]))
        y_coord.append(np.median(allcoords[1]))
        z_coord.append(np.median(allcoords[2]))

    # If nodes is None, define the dataframe
    if nodes is None:
        nodes = pd.DataFrame()

    # Add the median coordinates into dataframe
    # Origin is at 0,0,0, but scale affine diag for voxel spacing.
    # Scaling affine should be checked in future as general solution
    nodes['x'] = x_coord
    nodes['y'] = y_coord
    nodes['z'] = z_coord

    return nodes, img


def _plot_parcels(ax, img, cmap='Set2', hemisphere='both', **kwargs):
    """
    Plot each 3D parcels as a rendered surface.

    See plot for input arguments.
    """
    # get kwargs
    alpha = kwargs.get('nodealpha')
    surface_resolution = kwargs.get('surface_resolution')
    # Due to only being able to get data once, this leads to problems when LR hemi are specieid
    data = img.get_fdata(caching='unchanged').copy()
    # If single hemisphere, get only that side
    data = _select_single_hemisphere_template(data, hemisphere)
    # Get the number of nodes (subtract 1 for 0)
    nodelabels = np.unique(data)
    if 0 in nodelabels:
        nodelabels = nodelabels[1:]
    # Create a nnode length (or longer) array which repeats colormap
    if isinstance(cmap, str):
        colors = _colorarray_from_string(cmap, len(nodelabels))
    else:
        # If colors has already been defined prior to calling this function
        colors = cmap
    # loop through each node and plot verticies as different color
    # Possible improvement: could be made without for loop
    # And vals is used to plot color
    for ni, r in enumerate(nodelabels):
        dtmp = np.zeros(data.shape)
        dtmp[data == r] = 1
        verts, faces, _, _ = measure.marching_cubes(
            dtmp, step_size=surface_resolution)
        vertices = verts[faces]
        # for n in np.unique(vals):
        mesh = Poly3DCollection(vertices)
        mesh.set_facecolor(colors[ni])
        if isinstance(colors, str):
            mesh.set_alpha(alpha)
        elif colors.shape[1] != 4:
            mesh.set_alpha(alpha)
        ax.add_collection3d(mesh)

    ax.set_xlim(0, data.shape[0])
    ax.set_ylim(0, data.shape[1])
    ax.set_zlim(0, data.shape[2])


# def _plot_parcel_disks(ax, img, alpha, cmap='Set2', hemisphere='both', **kwargs):
#     """
#     Plot rendered surface as disk.

#     See netplotbrain.plot for input arguments.

#     Currently being tested and contains an angle bug
#     """
#     # get kwargs
#     surface_resolution = kwargs.get('surface_resolution')
#     # Due to only being able to get data once, this leads to problems when LR hemi are specieid
#     data = img.get_fdata(caching='unchanged').copy()
#     # If single hemisphere, get only that side
#     data = _select_single_hemisphere_template(data, hemisphere)
#     # Get the number of nodes (subtract 1 for 0)
#     nodelabels = np.unique(data)
#     if 0 in nodelabels:
#         nodelabels = nodelabels[1:]
#     # Create a nnode length (or longer) array which repeats colormap
#     if isinstance(cmap, str):
#         colors = _colorarray_from_string(cmap, len(nodelabels))
#     else:
#         # If colors has already been defined prior to calling this function
#         colors = cmap
#     # Rotate data
#     data = _rotate_data_to_viewingangle(data, kwargs['azim'], kwargs['elev'])
#     # loop through each node and plot verticies as different color
#     # Possible improvement: could be made without for loop
#     # And vals is used to plot color
#     for ni, r in enumerate(nodelabels):
#         dtmp = np.zeros(data.shape)
#         dtmp[data == r] = 1
#         verts, faces, _, _ = measure.marching_cubes(
#             dtmp, step_size=surface_resolution)
#         vertices = verts[faces]
#         # for n in np.unique(vals):
#         mesh = Poly3DCollection(vertices)
#         mesh.set_facecolor(colors[ni])
#         if isinstance(colors, str):
#             mesh.set_alpha(alpha)
#         elif colors.shape[1] != 4:
#             mesh.set_alpha(alpha)
#         ax.add_collection3d(mesh)

#     ax.set_xlim(0, data.shape[0])
#     ax.set_ylim(0, data.shape[1])
#     ax.set_zlim(0, data.shape[2])
