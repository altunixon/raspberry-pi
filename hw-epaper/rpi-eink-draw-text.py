#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import sys
import os
from importlib import import_module
path_root = os.path.dirname(os.path.abspath(__file__))
path_fonts = os.path.join(path_root, 'fonts')
waveshare_lib = 'waveshare_libs'
path_lib = os.path.join(path_root, waveshare_lib)
assert os.path.isdir(path_lib), ('WaveShare E-Ink libraries path missing, check "%s"' % path_lib)
#sys.path.append(path_lib)

import logging
import traceback
from time import sleep
from img_utils import image_resize_fit

logging.basicConfig(level=logging.DEBUG)

def image_load(pil_imgobj, **options):
    convert_mono = options.get('mono', False)
    invert_mode = options.get('mode', 0)
    resize_to = options.get('size', None)
    if resize_to is not None:
        pil_imgobj = image_resize_fit(resize_to)
    else:
        pass
    if invert_mode == 1:
        pil_imgobj = ImageOps.mirror(pil_imgobj)
    elif invert_mode == 2:
        pil_imgobj = ImageOps.flip(pil_imgobj)
    else:
        pass
    # 255 is WHITE, 0 is BLACK
    if convert_mono:
        color_filter = lambda x: 255 if x > 10 else 0
        return pil_imgobj.convert('L').point(color_filter, mode='1')
    else:
        return pil_imgobj

if __name__ == '__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    script_name =  '.'.join(os.path.basename(__file__).split('.')[:-1]).strip()
    parser = argparse.ArgumentParser(description='Draw texts to e-ink display',
        argument_default=argparse.SUPPRESS, formatter_class=RawTextHelpFormatter)
    parser.add_argument('txt_files', nargs='*', default=[],
        help='Text files for the accumulator.')
    parser.add_argument('-t', '--txt', dest='raw_text', nargs='?', default=None,
        help='Write commandline supplied text to screen')
    parser.add_argument('-c', '--color', dest='text_color', nargs='?', type=int, default=1,
        help='Set text color, 1=primary color, usually black(default), 2=secondary color(per model)')
    parser.add_argument('-a', '--animation', dest='text_animation', nargs='?', type=int, default=0,
        help='Set text animation, 0=none(default), 1=scroll')
    parser.add_argument('--wallpaper', dest='text_wallpaper', nargs='?', default=None,
        help='Set wallpaper, points to image file, preferably in binary color')
    parser.add_argument('-w', '--wait', dest='display_wait', nargs='?', type=int, default=9,
        help='Wait n seconds between draws.')
    parser.add_argument('--mode', dest='display_mode', nargs='?', type=int, default=0,
        help='Set text display mode, 0=landscape(default), 1=portrait, 2=landscape-inverted, 3=portrait-inverted')
    parser.add_argument('--clear', dest='display_clear', action='store_true', 
        help='Clear display on exit')
    parser.set_defaults(display_clear=False)
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument('--driver', dest='display_driver', nargs='?', default='epd2in13b_V3',
        help='Set e-ink module driver', required=True)
    console_args = parser.parse_args()
    #print(main_opts)
    assert (len(console_args.txt_files) > 0 or console_args.raw_text is not None), 'Nothing to do'
    try:
        # https://stackoverflow.com/questions/6677424/
        # same as from waveshare_libs import epd2in13b_V3 as waveshare_driver
        waveshare_driver = import_module(console_args.display_driver, waveshare_lib)
        logging.info("1. Initiate [%s] driver" % console_args.display_driver)
        eink_sheet = waveshare_driver.EPD()
        sheet_w = eink_sheet.width 
        sheet_h = eink_sheet.height
        logging.info("2. Init & Clear display: [{w}x{h} px]".format(w=sheet_w, h=sheet_h))
        eink_sheet.init()
        eink_sheet.Clear()
        sleep(1)
        logging.info('2. Creating base image, background [%s]' % console_args.text_wallpaper)
        # default is PORTRAIT mode? (sheet_h, sheet_w)
        
        if console_args.text_wallpaper is not None and os.path.isfile(console_args.text_wallpaper):
            image_base = image_load(Image.open(console_args.text_wallpaper), size=(sheet_w, sheet_h), mode=console_args.display_mode, mono=True)
            bg_enabled = True
        else:
            image_base = Image.new('1', (sheet_w, sheet_h), 255)
            bg_enabled = False

        txt_font = ImageFont.truetype(os.path.join(path_fonts, 'Font.ttc'), 10)
        txt_draw = lambda x, y: x.text((10, 0), z.strip('\n'), font=txt_font, fill=0) for z in y

        for x, txt_file in enumerate(console_args.txt_files):
            if os.path.isfile(txt_file):
                logging.info('2-%s. Read "%s" and display as color [%s]' % (x, image_file, console_args.text_color))
                
                with open(txt_file, 'r') as txt_fd:
                    txt_lines = txt_fd.readlines()
                if console_args.text_color > 1 or bg_enabled:
                    txt_canvas = ImageDraw.Draw(image_load(Image.new('1', (sheet_w, sheet_h), 255), mode=console_args.display_mode, mono=False))
                    #txt_canvas.text((12, 0), txt_lines[0], font=txt_font, fill=0)
                    txt_draw(txt_canvas, txt_lines)
                    eink_sheet.display(eink_sheet.getbuffer(image_base), eink_sheet.getbuffer(txt_canvas))
                else:
                    txt_canvas = ImageDraw.Draw(image_base)
                    #txt_canvas.text((12, 0), txt_lines[0], font=txt_font, fill=0)
                    txt_draw(txt_canvas, txt_lines)
                    eink_sheet.display(eink_sheet.getbuffer(image_base))
            else:
                logging.info('2-%s. File notfound "%s"' % (x, image_file))
                pass
            sleep(eink_sheet.display_wait)
            
        if console_args.display_clear:
            eink_sheet.init()
            eink_sheet.Clear()
        eink_sheet.sleep()

    except Exception as excp:
        logging.info(repr(excp))

    except KeyboardInterrupt:    
        logging.info("Ctrl+C:")
        epd2in13b_V3.epdconfig.module_exit()

    finally:
        logging.info("Done !?")
        exit()
else:
    pass
