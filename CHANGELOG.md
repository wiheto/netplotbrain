# Changelog

## [0.3.1] - in development

## Added 
- Added cm_boundary for connectivity matrixes (wiheto) 
- Some new gallery examples for connectivity matrices (wiheto)

## Fixed
- cm_rotate now works when False (wiheto)
- added dpi to svg export for improved rasterized image resolution (wiheto)

## [0.3.0]

### Added 

- Changelog added. (wiheto)
- Preliminary BIDS operations that generate edge df from BIDS layout `edges_from_bids()` (wiheto)
- Connectivity matrix as view option (wiheto)
- Rotation of connectivity matrix (wiheto)
- cm_order for connectivity matrix (wiheto)
- Dual colours for positive and negative edges (wiheto)
- Allow dual colors for positive and negative edges (wiheto) 
- Some gallery examples (plot_dmn, connectivity matrix) (wiheto)

### Update
- Updated README with network neuroscience reference (wiheto)
- Removed matplotlib deprecated `matplotlib.cm.get_cmap` for `matplotlib.colormaps` (wiheto) 
- Rasterization for glass brains (and all template/cms) for faster svg rendering (wiheto)
- Example data is now packaged in ./netplotbrain/example_data to be included in package (wiheto)

### Fixed
- Renaming "legend_tick_fontsize" and "legend_title_fontsize" to be more consistent (wiheto)
- Renaming "highlightlevel" to "highlight_level" to be more consistent (wiheto)
- Correcting some kwarg names in documentation (wiheto)
- A bug with spring layout and node_color when only subset of nodes plotted (wiheto)