#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
from importlib import import_module
path_root = os.path.dirname(os.path.abspath(__file__))
path_fonts = os.path.join(path_root, 'fonts')
path_img = os.path.join(path_root, 'images')
waveshare_lib = 'drivers'
path_lib = os.path.join(path_root, waveshare_lib)
assert os.path.isdir(path_lib), ('WaveShare E-Ink libraries path missing, check "%s"' % path_lib)
#sys.path.append(path_lib)

import logging
from time import sleep
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import traceback

logging.basicConfig(level=logging.DEBUG)

def image_convert_mono(pil_imgobj, **options):
    layer = options.get('layer', 1)
    primary_threshold = options.get('primary', None)
    secondary_threshold = options.get('secondary', (150, 200))
    contrast_level = options.get('contrast', 0)
    sharpness_level = options.get('sharpness', 0) # increase sharpness

    if contrast_level == 1:
        black_min, white_max = pil_imgobj.convert('L').getextrema()
        primary_threshold = int(white_max / 3)
        secondary_threshold = (primary_threshold, primary_threshold * 2)
    elif contrast_level > 1:
        pil_imgobj = ImageEnhance.Contrast(pil_imgobj).enhance(contrast_level)
    else:
        pass
    
    if sharpness_level > 0:
        pil_imgobj = ImageEnhance.Sharpness(pil_imgobj).enhance(sharpness + 1)
    else:
        pass

    assert (primary_threshold is not None or secondary_threshold is not None), 'Invalid layer'
    if layer == 1:
        # ~128 (greyscale 50% light) lower to increase shade? blackness?
        exposure_threshold = 128 if primary_threshold > 250 else primary_threshold
        color_filter = lambda x: 0 if x <= exposure_threshold else 255
    else:
        # ~150~200 (greyscale 65~80% light) lower to decrease exposure? lightness?
        thres_start, thresh_end = secondary_threshold
        color_filter = lambda x: 0 if thres_start < x < thresh_end else 255
    return pil_imgobj.convert('L').point(color_filter, mode='1')

def image_resize_fit(pil_imgobj, **options):
    img_w, img_h = pil_imgobj.size
    fit_w, fit_h = options.get('size', (104, 212))
    img_ratio = img_w / float(img_h)
    fit_ratio = fit_w / float(fit_h)
    invert_mode = options.get('mode', 0)
    print ('DEBUG-0: %s [%s] / %sx%s' % (pil_imgobj.size, img_ratio, fit_w, fit_h))
    # if image in landscape mode, rotate it counter-clockwise 90 degrees to portrait mode which is the only mode the driver support
    if img_ratio > 1:
        pil_imgobj = pil_imgobj.rotate(90, Image.NEAREST, expand=1)
        #pil_imgobj.save('/tmp/x-90.png', 'PNG')
        img_w, img_h = pil_imgobj.size
        img_ratio = img_w / float(img_h)
    else:
        pass
    print ('DEBUG-1: %s [%s] / %sx%s [Counter Clockwise 90?]' % (pil_imgobj.size, img_ratio, fit_w, fit_h))

    if invert_mode == 1:
        pil_imgobj = ImageOps.mirror(pil_imgobj)
    elif invert_mode == 2:
        pil_imgobj = ImageOps.flip(pil_imgobj)
    elif invert_mode == 3:
        pil_imgobj = ImageOps.flip(ImageOps.mirror(pil_imgobj))
    else:
        pass
    print ('DEBUG-2: %s / %sx%s [Invert Mode %s]' % (pil_imgobj.size, fit_w, fit_h, invert_mode))
    
    # same height, image_w > screen_w => crop_w
    if fit_ratio < img_ratio:
        #delta_ratio = fit_h / float(img_h)
        #new_w = int(delta_ratio * img_w)
        #delta_w = int( (new_w - fit_w) * delta_ratio )
        #print ('XXX ', delta_ratio, new_w, fit_w, delta_w)
        new_w = int(fit_ratio * img_h)
        delta_w = int((img_w - new_w) / 2)
        crop_box = (delta_w, 0, img_w - delta_w, img_h)
        pil_imgobj = pil_imgobj.crop(crop_box)
        print ('DEBUG-3: %s / %s [Crop W %s]' % (img_ratio, fit_ratio, crop_box))
    elif fit_ratio > img_ratio:
        #delta_ratio = fit_w / float(img_w)
        #new_h = int(delta_ratio * img_h)
        #delta_h = int( (new_h - fit_h) * delta_ratio )
        new_h = int(img_w * fit_ratio)
        delta_h = int((img_h - delta_h) / 2 )
        crop_box = (0, delta_h, img_w, img_h - delta_h)
        pil_imgobj = pil_imgobj.crop(crop_box)
        print ('DEBUG-3: %s / %s [Crop H %s]' % (img_ratio, fit_ratio, crop_box))
    else:
        pass

    #pil_imgobj.save('/tmp/x-crop.png', 'PNG')
    print ('DEBUG-4: %s Ratio %s/%s [Pre-Return]' % (pil_imgobj.size, (pil_imgobj.size[0] / float(pil_imgobj.size[1])), fit_ratio))
    return pil_imgobj.resize((fit_w, fit_h), Image.NEAREST)

if __name__ == '__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    script_name =  '.'.join(os.path.basename(__file__).split('.')[:-1]).strip()
    parser = argparse.ArgumentParser(description='Draw images to e-ink display',
        argument_default=argparse.SUPPRESS, formatter_class=RawTextHelpFormatter)
    parser.add_argument('images', nargs='*', default=[],
        help='Images for the accumulator.')
    parser.add_argument('--threshold', dest='thresh_values', nargs='?', default='128:128:192',
        help='Set the threshold range for monochrome conversion, primary:secondary:white')
    parser.add_argument('-w', '--wait', dest='display_wait', nargs='?', type=int, default=9,
        help='Wait n seconds between draws.')
    parser.add_argument('-m', '--mode', dest='display_mode', nargs='?', type=int, default=0,
        help='Displaymode, 0=auto(default), 1=invert-x, 2=invert-y, 3=invert-x+y')
    parser.add_argument('--contrast', dest='img_contrast', nargs='?', type=int, default=0,
        help='Increase image contrast level, 0(do nothing), 1(no contrast change but guess threshold instead), > 1(increase contrast manual threshold)')
    parser.add_argument('--sharpness', dest='img_sharpness', nargs='?', type=int, default=0,
        help='Increase image sharpness')
    parser.add_argument('--debug', dest='img_debug', nargs='?', default=None,
        help='Export converted image for debug purpose, accept dir path, /tmp is a good choice')
    parser.add_argument('--color', dest='display_color', nargs='?', type=int, default=0,
        help='Set display color, 0(default)=both, 1=primary(black), 2=secondary(red/yellow)')
    parser.set_defaults(display_black=False)
    parser.add_argument('-c', '--clear', dest='display_clear', action='store_true', 
        help='Clear display on exit')
    parser.set_defaults(display_clear=False)
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument('--driver', dest='display_driver', nargs='?', default=None,
        help='Set e-ink module driver see "%s" for available drivers, ex: epd2in13b_V3' % waveshare_lib, required=True)
    console_args = parser.parse_args()
    color_threshold = console_args.thresh_values.split(':')
    # generate color threshold values
    if len(color_threshold) == 1:
        thresh_primary = int(color_threshold[0])
        thresh_secondary, thresh_white = (thresh_primary, min([thresh_primary * 2, 255]))
    elif len(color_threshold) == 2:
        thresh_primary = int(color_threshold[0])
        thresh_secondary = int(color_threshold[1]) if int(color_threshold[1]) >= thresh_primary else thresh_primary
        thresh_white = int((255 - thresh_primary) / 2)
    elif len(color_threshold) >= 3:
        thresh_primary, thresh_secondary, thresh_white = (int(x) for x in color_threshold)
    else:
        thresh_primary, thresh_secondary, thresh_white = (128, 128, 192)
    if max([thresh_primary, thresh_secondary, thresh_white]) > 255:
        thresh_primary, thresh_secondary, thresh_white = (128, 128, 192)
    else:
        pass
    #print(main_opts)
    #assert len(console_args.images) > 0, 'Nothing to do'
    save_debug = (console_args.img_debug is not None and os.path.isdir(console_args.img_debug))
    try:
        # https://stackoverflow.com/questions/6677424/how-do-i-import-variable-packages-in-python-like-using-variable-variables-i#:~:text=Python%20doesn%27t%20have%20a,can%20use%20the%20eval%20function.&text=However%2C%20this%20can%27t%20be,to%20import%20using%20a%20variable.
        #waveshare_driver = getattr(__import__(waveshare_lib, fromlist=[console_args.display_driver]), console_args.display_driver)
        # same as: from waveshare_libs import epd2in13b_V3 as waveshare_driver
        waveshare_driver = import_module('{folder}.{script}'.format(folder=waveshare_lib, script=console_args.display_driver))
        logging.info("1. Initiate [%s] driver" % console_args.display_driver)
        eink_sheet = waveshare_driver.EPD()
        sheet_w = eink_sheet.width 
        sheet_h = eink_sheet.height
        logging.info("2. Init and Clear display: [{w}x{h} px]".format(w=sheet_w, h=sheet_h))
        for x, image_file in enumerate(console_args.images):
            if os.path.isfile(image_file):
                eink_sheet.init()
                eink_sheet.Clear()
                sleep(1)
                logging.info('3-%s. Read "%s" in mode [%s]' % (x, image_file, console_args.display_mode))
                image_obj = Image.open(image_file)
                # (104, 212) ???
                image_disp = image_resize_fit(image_obj, size=(sheet_w, sheet_h), mode=console_args.display_mode)
                #image_landscape = image_resize_crop(image_obj, (126, 298)) # LIES
                layer_base = image_convert_mono(image_disp, 
                    layer=1,
                    primary=thresh_primary,
                    contrast=console_args.img_contrast,
                    sharpness=console_args.img_sharpness)
                if console_args.display_color > 0:
                    assert (console_args.display_color == 1 or console_args.display_color == 2), \
                        ('Invalid Color[%s], see help for default values' % console_args.display_color)
                    eink_sheet.display_mono(eink_sheet.getbuffer(layer_base), console_args.display_color)
                else:
                    layer_secondary = image_convert_mono(image_disp,
                        layer=2,
                        secondary=(thresh_secondary, thresh_white),
                        contrast=console_args.img_contrast,
                        sharpness=console_args.img_sharpness)
                    eink_sheet.display(
                        eink_sheet.getbuffer(layer_secondary),
                        eink_sheet.getbuffer(layer_base)
                    )
                if save_debug:
                    image_name = os.path.basename(image_file).rsplit('.', 1)[0]
                    image_disp.save(os.path.join(console_args.img_debug, '%s-display.png' % image_name), 'PNG')
                    layer_base.save(os.path.join(console_args.img_debug, '%s-layer1-bB.png' % image_name), 'PNG')
                    if console_args.display_color == 0:
                        layer_secondary.save(os.path.join(console_args.img_debug, '%s-layer2-bR.png' % image_name), 'PNG')
                #image_obj.close()
                sleep(console_args.display_wait)
            else:
                logging.info('3-%s. File notfound "%s"' % (x, image_file))
                pass

        logging.info('4. Turning off 5V [cls=%s]' % console_args.display_clear)
        if console_args.display_clear:
            eink_sheet.init()
            eink_sheet.Clear()
        eink_sheet.sleep()

    except Exception as excp:
        logging.info("5. Exception: %s" % repr(excp))
        traceback.print_exc()
        exit(1)

    except KeyboardInterrupt:    
        logging.info("5. Ctrl+C")
        waveshare_driver.epdconfig.module_exit()
        exit()

    logging.info("5. Done !?")
    exit()
else:
    pass
