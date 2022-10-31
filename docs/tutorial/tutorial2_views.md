
# Tutorial 2: Visualization 

### Views

The view is the angle which the brain is viewed from in the plot.
You can specify it as a string:

| Argument | View | 
| :-------------:  | :----------: | 
|  'L'     | Left  |
|  'R'     | Right  |
|  'A'     | Anterior  |
|  'P'     | Posterior  |
|  'S'     | Superior  |
|  'I'     | Inferior  |
|  's'     | Spring Layout  |


Sequences of views are possible.
So, setting view = 'LSR' will generate 3 subplots with left, superior, and right views.

If you specify a list (e.g., `['LR', 'AP']`) then two different rows will be generated.
The first from left to right. The second from anterior to posterior.

```python
import netplotbrain
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='surface',
                  view=['LSR', 'AIP'])
plt.show()
```

You can also specify the specific rotation (tuple): (xy-rotation, xz-rotation) in degrees. The R view is (0, 0).

### Rotated sequences with frames

You can also generate a sequence of rotated images.

If the view is two letters (e.g., `'LR'`), then a sequence will be generated from the L-view to the R-view.

The parameter `frames` will control how many images are generated.
Images will then be displayed along a single row.

```python
import netplotbrain
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='surface',
                  view=['AP'],
                  frames=5)
```

### 360 degrees 

It is also possible to specify the `view="360"`to get a fully rotated brain. The frames argument dictates how many snapshots will be generated.

```python
import netplotbrain
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  template_style='glass',
                  view='360',
                  frames=8)
```

### Preset views 

There are a number of preset views which specify combinations of different viewws. See [here](../../preset/) for preset examples. 
