from PIL import Image

def analyseImage(path):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    """
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def FullscreenGifFrames(path, resize_to=None):
    im = Image.open(path)

    if not resize_to:
        resize_to = (im.size[0] // 2, im.size[1] // 2)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    try:
        while True:
            # print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            #if mode == 'partial':
            new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            #new_frame = new_frame.resize(resize_to, Image.ANTIALIAS)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

        all_frames = list(map(lambda x: x.resize(resize_to, Image.ANTIALIAS), all_frames))

    return all_frames