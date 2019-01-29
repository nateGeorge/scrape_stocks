# TODO: dynamically update HOME_DIR + 'short_squeeze_release_dates.xlsx'

# would need to use selenium to get this to work...meh, just use a multidownloader for chrome
# core
import os
import time
import pytz
import glob
import shutil
import calendar
import datetime
import traceback

# installed
import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

# custom
import scrape_stockdata as ss
from utils import get_home_dir

try:
    ua = UserAgent()
except:
    print("Couldn't make user agent, trying again")
    ua = UserAgent()

base_url = 'http://shortsqueeze.com/{}.php'
login_url = 'http://shortsqueeze.com/signin.php'
daily_url = 'http://shortsqueeze.com/down.php?fi={}.csv'  # date should be like 2017-11-13

YEARS = ['2015', '2016', '2017']
UNAME = os.environ.get('ss_uname')
PWORD = os.environ.get('ss_pass')
# HOME_DIR = get_home_dir(repo_name='scrape_stocks')
HOME_DIR = '/home/nate/Dropbox/data/shortsqueeze/'


def get_years(driver):
    """
    gets available years from the title bar
    """
    menu_bar = driver.find_element_by_xpath('/html/body/div/table[9]/tbody/tr/td/div/table')
    years = menu_bar.text.split('\n')
    int_years = []
    for y in years:
        try:
            int_years.append(int(y))
        except ValueError:
            pass

    return np.array(int_years)


def parse_bimo_dates(filename, dates_df, rev_cal_dict):
    """
    gets date from release dates dataframe and filename
    """
    # get the date from the dates_df and filename
    # old way of doing it which worked before the effed up filenames with an extra 0 in nov 2017...
    # date = f.split('/')[-1][9:16]
    date = filename.split('/')[-1].split('-')[0].split('.')[1]
    year = date[:4]
    month_num = int(date[-3:-1])
    month = rev_cal_dict[month_num]
    ab = date[-1].upper()
    t_df = dates_df[year]
    date = '-'.join([year,
                    str(month_num).zfill(2),
                    str(t_df[t_df[int(year)] == (month + ' ' + ab)]['NASDAQ®'].values[0]).zfill(2)])
    date = pd.to_datetime(date, format='%Y-%m-%d')
    return date


def check_for_new_excel(driver):
    """
    checks for new excel files to download, and if they aren't in the data folder,
    downloads them
    """
    while True:
        try:
            driver.get('http://shortsqueeze.com/ShortFiles.php')
            break
        except TimeoutException:
            pass

    years = get_years(driver)
    # get currently downloaded files
    dates_df = pd.read_excel(get_home_dir(repo_name='scrape_stocks') + 'short_squeeze_release_dates.xlsx', None)
    cal_dict = {v: k for k, v in enumerate(calendar.month_name)}
    del cal_dict['']
    rev_cal_dict = {v: k for k, v in cal_dict.items()}

    bimonthly_files = glob.glob(HOME_DIR + 'short_squeeze.com/*.xlsx')
    bimonthly_filenames = set([f.split('/')[-1] for f in bimonthly_files])
    bimo_dates = [parse_bimo_dates(f, dates_df, rev_cal_dict) for f in bimonthly_files]
    latest_date = max(bimo_dates).date()
    latest_year = latest_date.year
    check_years = years[years >= latest_year]

    files_to_dl = []
    filenames = []
    for y in check_years:
        driver.get('http://shortsqueeze.com/' + str(y) + '.php')
        links = driver.find_elements_by_partial_link_text('Download')
        for l in links:
            link = l.get_attribute('href')
            if link == 'http://shortsqueeze.com/ShortFiles.php':
                continue

            filename = link.split('/')[-1]
            if filename in bimonthly_filenames:
                continue

            files_to_dl.append(link)
            filenames.append(filename)

    if len(files_to_dl) == 0:
        print('no new files to download')

    # seems to hang on download, so this will make it continue
    driver.set_page_load_timeout(4)
    for l in files_to_dl:
        try:
            print('downloading', l)
            driver.get(l) # saves to downloads folder
        except TimeoutException:
            pass

    for f in filenames:
        full_fn = '/home/nate/Downloads/' + f
        print(full_fn)
        if os.path.exists(full_fn):
            # os.rename(full_fn, HOME_DIR + 'short_squeeze.com/' + f)
            shutil.copy(full_fn, HOME_DIR + 'short_squeeze.com/' + f)
            os.remove(full_fn)


def setup_driver(backend='FF'):
    """
    :param backend: string, one of FF, PH, CH (firefox, phantom, or chrome)
    currently phantomjs cannot download files
    """
    if backend == 'PH':
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            "(KHTML, like Gecko) Chrome/15.0.87"
        )
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1920, 1080)
    elif backend == 'FF':
        # couldn't get download working without manual settings...
        # https://stackoverflow.com/questions/38307446/selenium-browser-helperapps-neverask-openfile-and-savetodisk-is-not-working
        # create the profile (on ubuntu, firefox -P from command line),
        # download once, check 'don't ask again' and 'save'
        # also change downloads folder to ticker_data within git repo
        # then file path to profile, and use here:
        # short_squeeze was the name of the profile
        prof_paths = ['/home/nate/.mozilla/firefox/4mmudyyu.short_squeeze',
                        '/home/nate/.mozilla/firefox/bnmsym9o.short_squeeze',
                        # work ubuntu 18.04
                        '/home/nate/.mozilla/firefox/9xcrqt7o.short_squeeze'
                        ]
        # saves to downloads folder by default
        found_prof = False
        for p in prof_paths:
            if os.path.exists(p):
                found_prof = True
                profile = webdriver.FirefoxProfile(p)

        if not found_prof:
            print('couldn\'t find profile, going with default')
            profile = webdirver.FirefoxProfile()

        # auto-download unknown mime types:
        # http://forums.mozillazine.org/viewtopic.php?f=38&t=2430485
        # set to text/csv and comma-separated any other file types
        # https://stackoverflow.com/a/9329022/4549682
        # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

        # dont ask to download any files

        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/vnd.hzn-3d-crossword;video/3gpp;video/3gpp2;application/vnd.mseq;application/vnd.3m.post-it-notes;application/vnd.3gpp.pic-bw-large;application/vnd.3gpp.pic-bw-small;application/vnd.3gpp.pic-bw-var;application/vnd.3gp2.tcap;application/x-7z-compressed;application/x-abiword;application/x-ace-compressed;application/vnd.americandynamics.acc;application/vnd.acucobol;application/vnd.acucorp;audio/adpcm;application/x-authorware-bin;application/x-athorware-map;application/x-authorware-seg;application/vnd.adobe.air-application-installer-package+zip;application/x-shockwave-flash;application/vnd.adobe.fxp;application/pdf;application/vnd.cups-ppd;application/x-director;applicaion/vnd.adobe.xdp+xml;application/vnd.adobe.xfdf;audio/x-aac;application/vnd.ahead.space;application/vnd.airzip.filesecure.azf;application/vnd.airzip.filesecure.azs;application/vnd.amazon.ebook;application/vnd.amiga.ami;applicatin/andrew-inset;application/vnd.android.package-archive;application/vnd.anser-web-certificate-issue-initiation;application/vnd.anser-web-funds-transfer-initiation;application/vnd.antix.game-component;application/vnd.apple.installe+xml;application/applixware;application/vnd.hhe.lesson-player;application/vnd.aristanetworks.swi;text/x-asm;application/atomcat+xml;application/atomsvc+xml;application/atom+xml;application/pkix-attr-cert;audio/x-aiff;video/x-msvieo;application/vnd.audiograph;image/vnd.dxf;model/vnd.dwf;text/plain-bas;application/x-bcpio;application/octet-stream;image/bmp;application/x-bittorrent;application/vnd.rim.cod;application/vnd.blueice.multipass;application/vnd.bm;application/x-sh;image/prs.btif;application/vnd.businessobjects;application/x-bzip;application/x-bzip2;application/x-csh;text/x-c;application/vnd.chemdraw+xml;text/css;chemical/x-cdx;chemical/x-cml;chemical/x-csml;application/vn.contact.cmsg;application/vnd.claymore;application/vnd.clonk.c4group;image/vnd.dvb.subtitle;application/cdmi-capability;application/cdmi-container;application/cdmi-domain;application/cdmi-object;application/cdmi-queue;applicationvnd.cluetrust.cartomobile-config;application/vnd.cluetrust.cartomobile-config-pkg;image/x-cmu-raster;model/vnd.collada+xml;text/csv;application/mac-compactpro;application/vnd.wap.wmlc;image/cgm;x-conference/x-cooltalk;image/x-cmx;application/vnd.xara;application/vnd.cosmocaller;application/x-cpio;application/vnd.crick.clicker;application/vnd.crick.clicker.keyboard;application/vnd.crick.clicker.palette;application/vnd.crick.clicker.template;application/vn.crick.clicker.wordbank;application/vnd.criticaltools.wbs+xml;application/vnd.rig.cryptonote;chemical/x-cif;chemical/x-cmdf;application/cu-seeme;application/prs.cww;text/vnd.curl;text/vnd.curl.dcurl;text/vnd.curl.mcurl;text/vnd.crl.scurl;application/vnd.curl.car;application/vnd.curl.pcurl;application/vnd.yellowriver-custom-menu;application/dssc+der;application/dssc+xml;application/x-debian-package;audio/vnd.dece.audio;image/vnd.dece.graphic;video/vnd.dec.hd;video/vnd.dece.mobile;video/vnd.uvvu.mp4;video/vnd.dece.pd;video/vnd.dece.sd;video/vnd.dece.video;application/x-dvi;application/vnd.fdsn.seed;application/x-dtbook+xml;application/x-dtbresource+xml;application/vnd.dvb.ait;applcation/vnd.dvb.service;audio/vnd.digital-winds;image/vnd.djvu;application/xml-dtd;application/vnd.dolby.mlp;application/x-doom;application/vnd.dpgraph;audio/vnd.dra;application/vnd.dreamfactory;audio/vnd.dts;audio/vnd.dts.hd;imag/vnd.dwg;application/vnd.dynageo;application/ecmascript;application/vnd.ecowin.chart;image/vnd.fujixerox.edmics-mmr;image/vnd.fujixerox.edmics-rlc;application/exi;application/vnd.proteus.magazine;application/epub+zip;message/rfc82;application/vnd.enliven;application/vnd.is-xpr;image/vnd.xiff;application/vnd.xfdl;application/emma+xml;application/vnd.ezpix-album;application/vnd.ezpix-package;image/vnd.fst;video/vnd.fvt;image/vnd.fastbidsheet;application/vn.denovo.fcselayout-link;video/x-f4v;video/x-flv;image/vnd.fpx;image/vnd.net-fpx;text/vnd.fmi.flexstor;video/x-fli;application/vnd.fluxtime.clip;application/vnd.fdf;text/x-fortran;application/vnd.mif;application/vnd.framemaker;imae/x-freehand;application/vnd.fsc.weblaunch;application/vnd.frogans.fnc;application/vnd.frogans.ltf;application/vnd.fujixerox.ddd;application/vnd.fujixerox.docuworks;application/vnd.fujixerox.docuworks.binder;application/vnd.fujitu.oasys;application/vnd.fujitsu.oasys2;application/vnd.fujitsu.oasys3;application/vnd.fujitsu.oasysgp;application/vnd.fujitsu.oasysprs;application/x-futuresplash;application/vnd.fuzzysheet;image/g3fax;application/vnd.gmx;model/vn.gtw;application/vnd.genomatix.tuxedo;application/vnd.geogebra.file;application/vnd.geogebra.tool;model/vnd.gdl;application/vnd.geometry-explorer;application/vnd.geonext;application/vnd.geoplan;application/vnd.geospace;applicatio/x-font-ghostscript;application/x-font-bdf;application/x-gtar;application/x-texinfo;application/x-gnumeric;application/vnd.google-earth.kml+xml;application/vnd.google-earth.kmz;application/vnd.grafeq;image/gif;text/vnd.graphviz;aplication/vnd.groove-account;application/vnd.groove-help;application/vnd.groove-identity-message;application/vnd.groove-injector;application/vnd.groove-tool-message;application/vnd.groove-tool-template;application/vnd.groove-vcar;video/h261;video/h263;video/h264;application/vnd.hp-hpid;application/vnd.hp-hps;application/x-hdf;audio/vnd.rip;application/vnd.hbci;application/vnd.hp-jlyt;application/vnd.hp-pcl;application/vnd.hp-hpgl;application/vnd.yamaha.h-script;application/vnd.yamaha.hv-dic;application/vnd.yamaha.hv-voice;application/vnd.hydrostatix.sof-data;application/hyperstudio;application/vnd.hal+xml;text/html;application/vnd.ibm.rights-management;application/vnd.ibm.securecontainer;text/calendar;application/vnd.iccprofile;image/x-icon;application/vnd.igloader;image/ief;application/vnd.immervision-ivp;application/vnd.immervision-ivu;application/reginfo+xml;text/vnd.in3d.3dml;text/vnd.in3d.spot;mode/iges;application/vnd.intergeo;application/vnd.cinderella;application/vnd.intercon.formnet;application/vnd.isac.fcs;application/ipfix;application/pkix-cert;application/pkixcmp;application/pkix-crl;application/pkix-pkipath;applicaion/vnd.insors.igm;application/vnd.ipunplugged.rcprofile;application/vnd.irepository.package+xml;text/vnd.sun.j2me.app-descriptor;application/java-archive;application/java-vm;application/x-java-jnlp-file;application/java-serializd-object;text/x-java-source,java;application/javascript;application/json;application/vnd.joost.joda-archive;video/jpm;image/jpeg;video/jpeg;application/vnd.kahootz;application/vnd.chipnuts.karaoke-mmd;application/vnd.kde.karbon;aplication/vnd.kde.kchart;application/vnd.kde.kformula;application/vnd.kde.kivio;application/vnd.kde.kontour;application/vnd.kde.kpresenter;application/vnd.kde.kspread;application/vnd.kde.kword;application/vnd.kenameaapp;applicatin/vnd.kidspiration;application/vnd.kinar;application/vnd.kodak-descriptor;application/vnd.las.las+xml;application/x-latex;application/vnd.llamagraphics.life-balance.desktop;application/vnd.llamagraphics.life-balance.exchange+xml;application/vnd.jam;application/vnd.lotus-1-2-3;application/vnd.lotus-approach;application/vnd.lotus-freelance;application/vnd.lotus-notes;application/vnd.lotus-organizer;application/vnd.lotus-screencam;application/vnd.lotus-wordro;audio/vnd.lucent.voice;audio/x-mpegurl;video/x-m4v;application/mac-binhex40;application/vnd.macports.portpkg;application/vnd.osgeo.mapguide.package;application/marc;application/marcxml+xml;application/mxf;application/vnd.wolfrm.player;application/mathematica;application/mathml+xml;application/mbox;application/vnd.medcalcdata;application/mediaservercontrol+xml;application/vnd.mediastation.cdkey;application/vnd.mfer;application/vnd.mfmp;model/mesh;appliation/mads+xml;application/mets+xml;application/mods+xml;application/metalink4+xml;application/vnd.ms-powerpoint.template.macroenabled.12;application/vnd.ms-word.document.macroenabled.12;application/vnd.ms-word.template.macroenabed.12;application/vnd.mcd;application/vnd.micrografx.flo;application/vnd.micrografx.igx;application/vnd.eszigno3+xml;application/x-msaccess;video/x-ms-asf;application/x-msdownload;application/vnd.ms-artgalry;application/vnd.ms-ca-compressed;application/vnd.ms-ims;application/x-ms-application;application/x-msclip;image/vnd.ms-modi;application/vnd.ms-fontobject;application/vnd.ms-excel;application/vnd.ms-excel.addin.macroenabled.12;application/vnd.ms-excelsheet.binary.macroenabled.12;application/vnd.ms-excel.template.macroenabled.12;application/vnd.ms-excel.sheet.macroenabled.12;application/vnd.ms-htmlhelp;application/x-mscardfile;application/vnd.ms-lrm;application/x-msmediaview;aplication/x-msmoney;application/vnd.openxmlformats-officedocument.presentationml.presentation;application/vnd.openxmlformats-officedocument.presentationml.slide;application/vnd.openxmlformats-officedocument.presentationml.slideshw;application/vnd.openxmlformats-officedocument.presentationml.template;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;application/vnd.openxmlformats-officedocument.spreadsheetml.template;application/vnd.openxmformats-officedocument.wordprocessingml.document;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/x-msbinder;application/vnd.ms-officetheme;application/onenote;audio/vnd.ms-playready.media.pya;vdeo/vnd.ms-playready.media.pyv;application/vnd.ms-powerpoint;application/vnd.ms-powerpoint.addin.macroenabled.12;application/vnd.ms-powerpoint.slide.macroenabled.12;application/vnd.ms-powerpoint.presentation.macroenabled.12;appliation/vnd.ms-powerpoint.slideshow.macroenabled.12;application/vnd.ms-project;application/x-mspublisher;application/x-msschedule;application/x-silverlight-app;application/vnd.ms-pki.stl;application/vnd.ms-pki.seccat;application/vn.visio;video/x-ms-wm;audio/x-ms-wma;audio/x-ms-wax;video/x-ms-wmx;application/x-ms-wmd;application/vnd.ms-wpl;application/x-ms-wmz;video/x-ms-wmv;video/x-ms-wvx;application/x-msmetafile;application/x-msterminal;application/msword;application/x-mswrite;application/vnd.ms-works;application/x-ms-xbap;application/vnd.ms-xpsdocument;audio/midi;application/vnd.ibm.minipay;application/vnd.ibm.modcap;application/vnd.jcp.javame.midlet-rms;application/vnd.tmobile-ivetv;application/x-mobipocket-ebook;application/vnd.mobius.mbk;application/vnd.mobius.dis;application/vnd.mobius.plc;application/vnd.mobius.mqy;application/vnd.mobius.msl;application/vnd.mobius.txf;application/vnd.mobius.daf;tex/vnd.fly;application/vnd.mophun.certificate;application/vnd.mophun.application;video/mj2;audio/mpeg;video/vnd.mpegurl;video/mpeg;application/mp21;audio/mp4;video/mp4;application/mp4;application/vnd.apple.mpegurl;application/vnd.msician;application/vnd.muvee.style;application/xv+xml;application/vnd.nokia.n-gage.data;application/vnd.nokia.n-gage.symbian.install;application/x-dtbncx+xml;application/x-netcdf;application/vnd.neurolanguage.nlu;application/vnd.na;application/vnd.noblenet-directory;application/vnd.noblenet-sealer;application/vnd.noblenet-web;application/vnd.nokia.radio-preset;application/vnd.nokia.radio-presets;text/n3;application/vnd.novadigm.edm;application/vnd.novadim.edx;application/vnd.novadigm.ext;application/vnd.flographit;audio/vnd.nuera.ecelp4800;audio/vnd.nuera.ecelp7470;audio/vnd.nuera.ecelp9600;application/oda;application/ogg;audio/ogg;video/ogg;application/vnd.oma.dd2+xml;applicatin/vnd.oasis.opendocument.text-web;application/oebps-package+xml;application/vnd.intu.qbo;application/vnd.openofficeorg.extension;application/vnd.yamaha.openscoreformat;audio/webm;video/webm;application/vnd.oasis.opendocument.char;application/vnd.oasis.opendocument.chart-template;application/vnd.oasis.opendocument.database;application/vnd.oasis.opendocument.formula;application/vnd.oasis.opendocument.formula-template;application/vnd.oasis.opendocument.grapics;application/vnd.oasis.opendocument.graphics-template;application/vnd.oasis.opendocument.image;application/vnd.oasis.opendocument.image-template;application/vnd.oasis.opendocument.presentation;application/vnd.oasis.opendocumen.presentation-template;application/vnd.oasis.opendocument.spreadsheet;application/vnd.oasis.opendocument.spreadsheet-template;application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-master;application/vnd.asis.opendocument.text-template;image/ktx;application/vnd.sun.xml.calc;application/vnd.sun.xml.calc.template;application/vnd.sun.xml.draw;application/vnd.sun.xml.draw.template;application/vnd.sun.xml.impress;application/vnd.sun.xl.impress.template;application/vnd.sun.xml.math;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.global;application/vnd.sun.xml.writer.template;application/x-font-otf;application/vnd.yamaha.openscoreformat.osfpvg+xml;application/vnd.osgi.dp;application/vnd.palm;text/x-pascal;application/vnd.pawaafile;application/vnd.hp-pclxl;application/vnd.picsel;image/x-pcx;image/vnd.adobe.photoshop;application/pics-rules;image/x-pict;application/x-chat;aplication/pkcs10;application/x-pkcs12;application/pkcs7-mime;application/pkcs7-signature;application/x-pkcs7-certreqresp;application/x-pkcs7-certificates;application/pkcs8;application/vnd.pocketlearn;image/x-portable-anymap;image/-portable-bitmap;application/x-font-pcf;application/font-tdpfr;application/x-chess-pgn;image/x-portable-graymap;image/png;image/x-portable-pixmap;application/pskc+xml;application/vnd.ctc-posml;application/postscript;application/xfont-type1;application/vnd.powerbuilder6;application/pgp-encrypted;application/pgp-signature;application/vnd.previewsystems.box;application/vnd.pvi.ptid1;application/pls+xml;application/vnd.pg.format;application/vnd.pg.osasli;tex/prs.lines.tag;application/x-font-linux-psf;application/vnd.publishare-delta-tree;application/vnd.pmi.widget;application/vnd.quark.quarkxpress;application/vnd.epson.esf;application/vnd.epson.msf;application/vnd.epson.ssf;applicaton/vnd.epson.quickanime;application/vnd.intu.qfx;video/quicktime;application/x-rar-compressed;audio/x-pn-realaudio;audio/x-pn-realaudio-plugin;application/rsd+xml;application/vnd.rn-realmedia;application/vnd.realvnc.bed;applicatin/vnd.recordare.musicxml;application/vnd.recordare.musicxml+xml;application/relax-ng-compact-syntax;application/vnd.data-vision.rdz;application/rdf+xml;application/vnd.cloanto.rp9;application/vnd.jisp;application/rtf;text/richtex;application/vnd.route66.link66+xml;application/rss+xml;application/shf+xml;application/vnd.sailingtracker.track;image/svg+xml;application/vnd.sus-calendar;application/sru+xml;application/set-payment-initiation;application/set-reistration-initiation;application/vnd.sema;application/vnd.semd;application/vnd.semf;application/vnd.seemail;application/x-font-snf;application/scvp-vp-request;application/scvp-vp-response;application/scvp-cv-request;application/svp-cv-response;application/sdp;text/x-setext;video/x-sgi-movie;application/vnd.shana.informed.formdata;application/vnd.shana.informed.formtemplate;application/vnd.shana.informed.interchange;application/vnd.shana.informed.package;application/thraud+xml;application/x-shar;image/x-rgb;application/vnd.epson.salt;application/vnd.accpac.simply.aso;application/vnd.accpac.simply.imp;application/vnd.simtech-mindmapper;application/vnd.commonspace;application/vnd.ymaha.smaf-audio;application/vnd.smaf;application/vnd.yamaha.smaf-phrase;application/vnd.smart.teacher;application/vnd.svd;application/sparql-query;application/sparql-results+xml;application/srgs;application/srgs+xml;application/sml+xml;application/vnd.koan;text/sgml;application/vnd.stardivision.calc;application/vnd.stardivision.draw;application/vnd.stardivision.impress;application/vnd.stardivision.math;application/vnd.stardivision.writer;application/vnd.tardivision.writer-global;application/vnd.stepmania.stepchart;application/x-stuffit;application/x-stuffitx;application/vnd.solent.sdkm+xml;application/vnd.olpc-sugar;audio/basic;application/vnd.wqd;application/vnd.symbian.install;application/smil+xml;application/vnd.syncml+xml;application/vnd.syncml.dm+wbxml;application/vnd.syncml.dm+xml;application/x-sv4cpio;application/x-sv4crc;application/sbml+xml;text/tab-separated-values;image/tiff;application/vnd.to.intent-module-archive;application/x-tar;application/x-tcl;application/x-tex;application/x-tex-tfm;application/tei+xml;text/plain;application/vnd.spotfire.dxp;application/vnd.spotfire.sfs;application/timestamped-data;applicationvnd.trid.tpt;application/vnd.triscape.mxs;text/troff;application/vnd.trueapp;application/x-font-ttf;text/turtle;application/vnd.umajin;application/vnd.uoml+xml;application/vnd.unity;application/vnd.ufdl;text/uri-list;application/nd.uiq.theme;application/x-ustar;text/x-uuencode;text/x-vcalendar;text/x-vcard;application/x-cdlink;application/vnd.vsf;model/vrml;application/vnd.vcx;model/vnd.mts;model/vnd.vtu;application/vnd.visionary;video/vnd.vivo;applicatin/ccxml+xml,;application/voicexml+xml;application/x-wais-source;application/vnd.wap.wbxml;image/vnd.wap.wbmp;audio/x-wav;application/davmount+xml;application/x-font-woff;application/wspolicy+xml;image/webp;application/vnd.webturb;application/widget;application/winhlp;text/vnd.wap.wml;text/vnd.wap.wmlscript;application/vnd.wap.wmlscriptc;application/vnd.wordperfect;application/vnd.wt.stf;application/wsdl+xml;image/x-xbitmap;image/x-xpixmap;image/x-xwindowump;application/x-x509-ca-cert;application/x-xfig;application/xhtml+xml;application/xml;application/xcap-diff+xml;application/xenc+xml;application/patch-ops-error+xml;application/resource-lists+xml;application/rls-services+xml;aplication/resource-lists-diff+xml;application/xslt+xml;application/xop+xml;application/x-xpinstall;application/xspf+xml;application/vnd.mozilla.xul+xml;chemical/x-xyz;text/yaml;application/yang;application/yin+xml;application/vnd.ul;application/zip;application/vnd.handheld-entertainment+xml;application/vnd.zzazz.deck+xml;csv/comma-separated-values")


        # https://www.lifewire.com/firefox-about-config-entry-browser-445707
        # profile.set_preference('browser.download.folderList', 1) # downloads folder
        # profile.set_preference('browser.download.manager.showWhenStarting', False)
        # profile.set_preference('browser.helperApps.alwaysAsk.force', False)
        # # profile.set_preference('browser.download.dir', '/tmp')
        # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', '*')
        driver = webdriver.Firefox(profile)
    elif backend == 'CH':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
          "download.default_directory": '/home/nate/Downloads/',
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })
        driver = webdriver.Chrome(chrome_options=options)

    return driver


def get_latest_daily_date():
    # get latest date from daily scrapes
    daily_files = glob.glob(HOME_DIR + 'short_squeeze_daily/*.csv')
    daily_dates = [pd.to_datetime(f.split('/')[-1].split('.')[0]) for f in daily_files]
    last_daily = max(daily_dates).date()
    return last_daily


def download_daily_data(driver=None, date=None):
    """
    checks which files already exist, then downloads remaining files to bring up to current

    or if 'date' supplied (i.e. 2018-04-12, yyyy-mm-dd, as a string), then downloads for that specific date
    """
    if driver is None:
        driver = setup_driver()
        driver = log_in(driver)
        time.sleep(3)  # wait for login to complete...could also use some element detection

    # TODO: check which files are missing or are size 0 in the existing files after the latest
    # excel file, and download those.  delete/archive any files older than the last excel file
    last_daily = get_latest_daily_date()
    today_utc = pd.to_datetime('now')
    # was thinking about using NY time, but mcal is in UTC
    # local_tz = pytz.timezone('America/New_York')
    # today_ny = today_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
    ndq = mcal.get_calendar('NASDAQ')
    open_days = ndq.schedule(start_date=today_utc - pd.Timedelta(str(3*365) + ' days'), end_date=today_utc)
    # basically, this waits for 3 hours after market close if it's the same day
    if open_days.iloc[-1]['market_close'].date() == today_utc.date():
        open_days = open_days.iloc[:-1]

    open_dates = np.array([o['market_close'].date() for l, o in open_days.iterrows()])
    if date is None:
        to_scrape = open_dates[open_dates > last_daily]
        if len(to_scrape) == 0:
            print('nothing to scrape right now')
            return
    else:
        date_strptime = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if date_strptime not in open_dates:
            print('supplied date of', date, 'is not in the open_dates, doing nothing...')
            return
        else:
            to_scrape = [date_strptime]

    # seems to hang on download, so this will make it continue
    driver.set_page_load_timeout(4)
    filenames = []
    for s in to_scrape:
        d = s.strftime('%Y-%m-%d')
        url = daily_url.format(d)
        filename = url.split('=')[-1]  # gets csv filename right now
        filenames.append(filename)
        try:
            print('downloading', filename)
            driver.get(url) # saves to downloads folder
        except TimeoutException:
            pass

    # moves file to data folder
    for f in filenames:
        og_file = '/home/nate/Downloads/' + f
        if os.path.exists(og_file):
            # os.rename(og_file, HOME_DIR + 'short_squeeze_daily/' + f)
            shutil.copy(og_file, HOME_DIR + 'short_squeeze_daily/' + f)
            os.remove(og_file)


def check_market_status():
    """
    Checks to see if market is open today.
    Uses the pandas_market_calendars package as mcal
    """
    # today = datetime.datetime.now(pytz.timezone('America/New_York')).date()
    # today_utc = pd.to_datetime('now').date()
    today_ny = datetime.datetime.now(pytz.timezone('America/New_York'))
    ndq = mcal.get_calendar('NASDAQ')
    open_days = ndq.schedule(start_date=today_ny - pd.Timedelta('10 days'), end_date=today_ny)
    if today_ny.date() in open_days.index:
        return open_days
    else:
        return None


def get_latest_close_date(market='NASDAQ'):
    """
    gets the latest date the markets were open (NASDAQ), and returns the closing datetime
    """
    # today = datetime.datetime.now(pytz.timezone('America/New_York')).date()
    today_utc = pd.to_datetime('now').date()
    ndq = mcal.get_calendar(market)
    open_days = ndq.schedule(start_date=today_utc - pd.Timedelta('10 days'), end_date=today_utc)
    return open_days.iloc[-1]['market_close']


def daily_updater():
    """
    checks if any new files to download, if so, downloads them
    """
    latest_scrape = get_latest_daily_date()
    while True:
        latest_close_date = get_latest_close_date()
        today_utc = pd.to_datetime('now')
        today_ny = datetime.datetime.now(pytz.timezone('America/New_York'))
        pd_today_ny = pd.to_datetime(today_ny.date())
        if (latest_close_date.date() - latest_scrape) > pd.Timedelta('1D'):
            print('more than 1 day out of date, downloading...')
            download_updates()
        elif (latest_close_date.date() - latest_scrape) == pd.Timedelta('1D'):
            if today_utc.hour > latest_close_date.hour:
                print('market closed, checking for new data...')
                download_updates()
        elif pd_today_ny.date() == latest_close_date.date():  # if the market is open and the db isn't up to date with today...
            if today_ny.hour >= 22:
                print('downloading update from today...')
                download_updates()

        print('sleeping 1h...')
        time.sleep(3600)
        # try:
        #     driver = log_in(driver)
        # except NoSuchElementException:
        #     driver.quit()
        #     driver = setup_driver()
        #     driver = log_in(driver)
        # time.sleep(3)


def log_in(driver):
    while True:
        try:
            driver.get(login_url)
            time.sleep(1 + np.random.rand())  # should add WebDriverWait
            username = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input')
            password = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input')
            username.send_keys(UNAME)
            password.send_keys(PWORD)
            time.sleep(1 + np.random.rand())
            signIn = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input')
            signIn.click()
            print('logged in successfully')
            return driver
            break  # not sure if this necessary, but[] just in case
        except (TimeoutException, NoSuchElementException):
            driver.quit()
            driver = setup_driver()


def download_updates():
    """
    checks for daily and bimonthly updates, then downloads if needed
    """
    while True:
        try:
            driver = setup_driver()
            driver = log_in(driver)
            time.sleep(3)  # wait for login to complete...could also use some element detection
            download_daily_data(driver)
            check_for_new_excel(driver)
            driver.quit()
            break
        except:
            traceback.print_exc()
            time.sleep(5)
            try:
                driver.quit()
            except:
                pass


if __name__ == "__main__":
    # for headless browser mode with FF
    # http://scraping.pro/use-headless-firefox-scraping-linux/
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(800, 600))
    display.start()

    daily_updater()
