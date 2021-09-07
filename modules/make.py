"""
##########################################################################
*
*   Copyright © 2019-2021 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

import urllib.request as ulrq
from json import dumps
from sys import exit
from time import time

import bs4 as btsp
from cite import StatusDecorator
from click import command, option, version_option

statdcrt = StatusDecorator()


def generate_list_from_file(chanlist: str):
    try:
        channel_list = open(chanlist, "r").read().split("\n")
        return True, list(channel_list)
    except Exception as expt:
        statdcrt.failure(str(expt))
        return False, []


def generate_list_from_link():
    try:
        source = ulrq.urlopen("https://meetbot-raw.fedoraproject.org").read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        channel_list = []
        for channel in parse_object.find_all("a")[5:]:
            channel_list.append(channel.string[0:-1])
        return True, list(channel_list)
    except Exception as expt:
        statdcrt.failure(str(expt))
        return False, []


def generate_json_index_for_conversations(chanlist: list, indexout: str):
    chanlist = list(chanlist)
    convdict, passqant, failqant, listqant = {}, 0, 0, len(chanlist)
    for chanindx in chanlist:
        try:
            channel_name = chanindx
            channel_link = "https://meetbot-raw.fedoraproject.org/%s/" % channel_name
            channel_date_source = ulrq.urlopen(channel_link).read()
            channel_date_parse_object = btsp.BeautifulSoup(channel_date_source, "html.parser")
            channel_date_dict = {}
            for dateindx in channel_date_parse_object.find_all("a")[5:]:
                datetime_name = dateindx.string[0:-1]
                datetime_link = "https://meetbot-raw.fedoraproject.org/%s/%s/" % (channel_name, dateindx.get("href"))
                datetime_dict = {}
                channel_date_meetlist_source = ulrq.urlopen(datetime_link).read()
                channel_date_meetlist_parse_object = btsp.BeautifulSoup(channel_date_meetlist_source, "html.parser")
                for meetindx in channel_date_meetlist_parse_object.find_all("a")[5:]:
                    if ".log.html" in meetindx.string:
                        meeting_name = meetindx.string.replace(".log.html", "")
                        channel_date_meetlist_dict = {
                            "meeting_log": "https://meetbot-raw.fedoraproject.org/%s/%s/%s/" %
                                           (channel_name, datetime_name, meetindx.string),
                            "meeting_sum": "https://meetbot-raw.fedoraproject.org/%s/%s/%s/" %
                                           (channel_name, datetime_name, meetindx.string.replace(".log.html", ".html")),
                        }
                        datetime_dict[meeting_name] = channel_date_meetlist_dict
                channel_date_dict[datetime_name] = {
                    "datetime_link": datetime_link,
                    "datetime_conv": datetime_dict
                }
            convdict[channel_name] = {
                "channel_link": channel_link,
                "conversation": channel_date_dict
            }
            statdcrt.success(chanindx)
            passqant += 1
        except Exception as expt:
            statdcrt.warning(str(chanindx))
            failqant += 1
            continue
    try:
        jsontext = dumps(convdict, indent=4)
        with open(indexout, "w") as datafile:
            datafile.write(jsontext)
    except Exception as expt:
        statdcrt.failure("Could not store JSON index to a file")
        statdcrt.general(str(expt))
    return passqant, failqant, listqant


@command()
@option("-f", "--listfile", "listfile", help="Load a list of channels from a file", default=None)
@option("-o", "--indexout", "indexout", help="Output the generated index to a specific file", default="database.json")
@version_option(version="0.1.0", prog_name="Fragment Indexer")
def mainfunc(listfile, indexout):
    """
    Indexes metadata about IRC/Matrix channels, meeting dates and conversations into a JSON file
    """
    statdcrt.section("FRAGMENT INDEXER")
    strttime = time()
    if listfile:
        statdcrt.general("Starting conditional indexing...")
        retndata = generate_list_from_file(listfile)
    else:
        statdcrt.general("Starting unconditional indexing...")
        retndata = generate_list_from_link()
    if retndata[0] is True and retndata[1] != []:
        statdcrt.success("Found %d channels" % len(retndata[1]))
        gentuple = generate_json_index_for_conversations(retndata[1], indexout)
        stoptime = time()
        duration = stoptime - strttime
        statdcrt.section("%d passed, %d failed, %d total, %d seconds" %
                         (gentuple[0], gentuple[1], gentuple[2], duration))
    else:
        exit(0)


if __name__ == "__main__":
    mainfunc()
