import logging
import string
import os

from matplotlib import pyplot as plt
plt.ioff()
AXIS_FONT = {'fontname': 'Arial', 'size': '14'}
from math import log as mlog2
from collections import Counter, defaultdict

from read import map_to_precursors, map_to_precursors_on_fly, precursor_sequence
from utils import safe_dirs
from progressbar import ProgressBar

from seqcluster.libs.utils import file_exists
from seqcluster.function.rnafold import run_rnafold
from seqcluster.html import HTML
from seqcluster import templates

logger = logging.getLogger('html')


def _get_link(c):
    """Gives html link tag for cluster link information"""
    return "<a href=%s/maps.html>%s</a>" % (c, c)


def _get_ann(dbs, features):
    """
    Gives format to annotation for html table output
    """
    value = ""
    for db, feature in zip(dbs, features):
        value += db + ":" + feature
    return value


def _parse(profile, size):
    total = Counter()
    for sample in profile:
        for pos in range(len(size)):
            total[pos] += profile[sample][pos]
    return total.values()


def make_profile(data, out_dir, args):
    """
    Make html for each cluster
    """
    main_table = []
    header = ['id', 'ann']
    html_file = os.path.join(out_dir, "index.html")
    n = len(data[0])
    bar = ProgressBar(maxval=n)
    bar.start()
    bar.update(0)
    for itern, c in enumerate(data[0]):
        bar.update(itern)
        logger.debug("creating cluser: {}".format(c))
        safe_dirs(os.path.join(out_dir, c))
        valid, ann, pos_structure = _single_cluster(c, data, os.path.join(out_dir, c, "maps.tsv"), args)
        data[0][c].update({'profile': pos_structure})
        loci = data[0][c]['loci']
        data[0][c]['precursor'] = {"seq": precursor_sequence(loci[0][0:5], args.ref)}
        data[0][c]['precursor']["colors"] = _parse(data[0][c]['profile'], data[0][c]['precursor']["seq"])
        data[0][c]['precursor'].update(run_rnafold(data[0][c]['precursor']['seq']))
        if valid:
            main_table.append([_get_link(c), _get_ann(valid, ann)])

    main_html = HTML.table(main_table, header_row=header, attribs={'id': 'keywords'})
    html_template = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(templates.__file__)), "main"))
    content = open(html_template).read()
    main_html = {'main': main_html}
    out_content = string.Template(content).safe_substitute(main_html)
    with open(html_file, 'w') as out_handle:
        print >>out_handle, out_content
    return data


def _expand(dat, counts, start, end):
    """
    expand the same counts from start to end
    """
    for pos in range(start, end):
        for s in counts:
            dat[s][pos] += counts[s]
    return dat


def _convert_to_df(in_file, freq, raw_file):
    """
    convert data frame into table with pandas
    """
    dat = defaultdict(Counter)
    if isinstance(in_file, (str, unicode)):
        with open(in_file) as in_handle:
            for line in in_handle:
                cols = line.strip().split("\t")
                counts = freq[cols[3]]
                dat = _expand(dat, counts, int(cols[1]), int(cols[2]))
    else:
        if raw_file:
            out_handle = open(raw_file, "w")
        for name in in_file:
            counts = freq[name]
            if raw_file:
                print >>out_handle, "%s\t%s\t%s\t%s\t%s\t%s" % ("chr", in_file[name][0], in_file[name][1], name, sum(counts.values()), "+")
            dat = _expand(dat, counts, in_file[name][0], in_file[name][1])

    for s in dat:
        for p in dat[s]:
            dat[s][p] = mlog2(dat[s][p] + 1)
    return dat


def _make_html(c, html_file, figure_file, prefix):
    """
    create html from template, adding figure,
    annotation and sequences counts
    """
    ann = defaultdict(list)
    seqs_table = []
    src_img = "<img src=\"%s\" width=\"800\" height=\"350\" />" % os.path.basename(figure_file)
    coor_list = [" ".join(map(str, l)) for l in c['loci']]

    for pos in c['ann']:
        for db in pos:
            ann[db] += list(pos[db])
    logger.debug(ann)

    valid = [l for l in c['valid']]
    ann_list = [", ".join(list(set(ann[feature]))) for feature in ann if feature in valid]

    seqs = [s.values()[0] for s in c['seqs']]
    freq = [map(float, s.values()[0].values()) for s in c['freq']]
    header = ['seq'] + c['freq'][0].values()[0].keys()
    for s, f in zip(seqs, freq):
        f = map(round, f)
        seqs_table.append([s] + map(str, f))
    # seqs_html = seqs_html.replace("TABLE", "TABLE id=\"keywords\"")
    if not file_exists(html_file):
        coor_html = HTML.list(coor_list)
        ann_html = HTML.list(ann_list)
        seqs_html = HTML.table(seqs_table,
                               header_row=header, attribs={'id': 'keywords'})
        html_template = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(templates.__file__)), "cluster"))
        content = open(html_template).read()
        data = {'profile': src_img,
                'loci': coor_html,
                'annotation': ann_html,
                'table': seqs_html}
        out_content = string.Template(content).safe_substitute(data)
        with open(html_file, 'w') as out_handle:
            print >>out_handle, out_content

    return valid, ann_list


def _single_cluster(c, data, out_file, args):
    """
    Map sequences on precursors and create
    expression profile
    """
    valid, ann = 0, 0
    raw_file = None
    figure_file = out_file.replace(".tsv", ".png")
    html_file = out_file.replace(".tsv", ".html")
    prefix = os.path.dirname(out_file)
    freq = defaultdict()
    [freq.update({s.keys()[0]: s.values()[0]}) for s in data[0][c]['freq']]
    names = [s.keys()[0] for s in data[0][c]['seqs']]
    seqs = [s.values()[0] for s in data[0][c]['seqs']]
    loci = data[0][c]['loci']

    if loci[0][3] - loci[0][2] > 500:
        logger.info("locus bigger > 500 nt, skipping: %s" % loci)
        return valid, ann, {}
    if not file_exists(out_file):
        if args.razer:
            logger.debug("map with razer all sequences to all loci %s " % loci)
            map_to_precursors(seqs, names, {loci[0][0]: [loci[0][0:5]]}, out_file, args)
        else:
            logger.debug("map with C fn all sequences to all loci %s " % loci)
            if args.debug:
                raw_file = out_file
            out_file = map_to_precursors_on_fly(seqs, names, loci[0][0:5], args)

    logger.debug("plot sequences on loci")
    df = _convert_to_df(out_file, freq, raw_file)
    if df:
        if not file_exists(figure_file):
            fig = plt.figure()
            for s in df:
                plt.plot(df[s].keys(), df[s].values())
            plt.ylabel('Normalized expression', fontsize=15)
            plt.xlabel('Position', fontsize=15)
            plt.savefig(figure_file)
            plt.close(fig)
        valid, ann = _make_html(data[0][c], html_file, figure_file, prefix)

    return valid, ann, df
