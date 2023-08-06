from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import dirname, basename, abspath
from collections import OrderedDict
from json import loads
from collections import namedtuple
from os import chdir
import re


pymash_version = (0,4)

def convert_to_namedtuple(d):
    return namedtuple('jsonobj', d.keys())(*d.values())

def json2obj(data):
    try:
        return loads(data, object_hook=convert_to_namedtuple)
    except ValueError as e:
        return None

def get_wanted_sections_from_file_content(content, re_ptrn):
    result = re.findall(re_ptrn, content, re.MULTILINE)
    if result:
        return [actual_lines
                for grp_res in result
                for actual_lines in grp_res
                if actual_lines not in ['\n','']]
    return None

def mash(cfg_path):
    """
    :param cfg_path: path to a json encoded file with apropriate configurations
    :return: 0 on success
    """
    cfg_file = open(cfg_path)
    chdir(dirname(abspath(cfg_path)))

    cfg = json2obj(cfg_file.read())
    if cfg is None:
        print ("config file is malformed")
        return -1

    start_marker = re.escape(cfg.wanted_begin).replace('\\ ', '\\s')
    end_marker = re.escape(cfg.wanted_end).replace('\\ ', '\\s')

    re_ptrn = '^{0}\n((.|\n)*?){1}(\n|$)'.format(start_marker, end_marker)

    pts = OrderedDict()
    for wanted_file in cfg.merge:
        pts.setdefault(wanted_file.file, [])

    for wanted_file in cfg.merge:

        entire_file = open(wanted_file.file).read()
        wanted_parts = get_wanted_sections_from_file_content(entire_file, re_ptrn)
        filename = basename(wanted_file.file)

        if cfg.show_desc:
            try:
                desc_txt = '"""\n'+wanted_file.desc +'\n"""\n'
                wanted_parts.insert(0, desc_txt)
            except AttributeError as e:
                pass

        if cfg.show_seams:
            if cfg.replace_seam_with_region:
                seam = filename.center(70, ' ')
                start_seam = cfg.line_comment +  'region    ' + seam +'\n'
                end_seam = cfg.line_comment +    'endregion ' + seam +'\n'
            else:
                seam = filename.center(77, '-')
                start_seam = '{0} {1}{2}{3}\n'.format(cfg.line_comment, 'v', seam, 'v')
                end_seam = '{0} {1}{2}{3}\n'.format(cfg.line_comment, '^', seam, '^')

            wanted_parts.insert(0,start_seam)
            wanted_parts.append(end_seam)

        pts[wanted_file.file].extend(wanted_parts)

    with open(cfg.output, 'w') as outf:
        for wanted_file_name in pts:
            print('mashing `{0}`'.format(wanted_file_name))
            chunks = pts[wanted_file_name]
            outf.write(''.join(chunks))


    print ('done')
    return 0
