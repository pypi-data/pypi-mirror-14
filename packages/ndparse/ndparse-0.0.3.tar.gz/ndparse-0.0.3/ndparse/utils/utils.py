import numpy as np


def compute_centroids(data):

    centroids = 5

    return centroids


def concatenate_files(files, outf):
    with open(outf, "a") as fout:
        [fout.write(line) for f in files for line in open(f)]
    pass


def plt(im1, im2=None, cmap1='gray', cmap2='jet', slice=0, alpha=1):
    """
    Convenience function to handle plotting of neurodata arrays.
    Mostly tested with 8-bit image and 32-bit annos, but lots of
    things should work.  Mimics (and uses) matplotlib, but transparently
    deals with RAMON objects, transposes, and overlays.  Slices 3D arrays
    and allows for different blending when using overlays.  We require
    (but verify) that dimensions are the same when overlaying.

    Arguments:
        im1 (array): RAMONObject or numpy array
        im2 (array) [None]:  RAMONObject or numpy array
        cmap1 (string ['gray']): Colormap for base image
        cmap2 (string ['jet']): Colormap for overlay image
        slice (int) [0]: Used to choose slice from 3D array
        alpha (float) [1]: Used to set blending option between 0-1

    Returns:
        None.

    """

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    # get im1_proc as 2D array

    base_image = False
    im1_proc = None

    if hasattr(im1, 'cutout') and im1.cutout is not None:
        im1_proc = im1.cutout
    elif im1 is not None:
        im1_proc = im1

    if im1_proc is not None and len(np.shape(im1_proc)) == 3:
        im1_proc = im1_proc[:, :, slice]

    if im1_proc is not None:
        base_image = True

    # get im2_proc as 2D array if exists
    overlay_image = False
    im2_proc = None

    if im2 is not None:

        if hasattr(im2, 'cutout') and im2.cutout is not None:
            im2_proc = im2.cutout
        elif im2 is not None:
            im2_proc = im2

        if im2_proc is not None and len(np.shape(im2_proc)) == 3:
            im2_proc = im2_proc[:, :, slice]

    if im2_proc is not None and np.shape(im1_proc) == np.shape(im2_proc):
        overlay_image = True

    if base_image:

        ax = plt.axes([0, 0, 1, 1])
        plt.axis('off')
        fig = plt.imshow(im1_proc.T, cmap=cmap1, interpolation='bilinear')

    if base_image and overlay_image and alpha == 1:

        im2_proc = np.ma.masked_where(im2_proc == 0, im2_proc)
        fig = plt.imshow(im2_proc.T, cmap=cmap2, interpolation='nearest')

    elif base_image and overlay_image and alpha < 1:

        plt.hold(True)
        im2_proc = np.asarray(im2_proc, dtype='float')  # TODO better way
        im2_proc[im2_proc == 0] = np.nan  # zero out bg
        fig = plt.imshow(im2_proc.T, cmap=cmap2,
                         alpha=alpha, interpolation='nearest')

    plt.show()


def save_gif():
    print 'coming soon!'
