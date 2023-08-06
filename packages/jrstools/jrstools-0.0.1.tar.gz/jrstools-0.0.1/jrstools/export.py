# -*- coding: utf-8 -*-
import os
import io
import json

from error import JrsExportError

from jinja2 import Environment, FileSystemLoader

j2 = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    trim_blocks=True,
    lstrip_blocks=True
)


def export_json(root, schemas):
    if not os.path.exists(root):
        raise JrsExportError("Path not exists '{}'".format(root))
    for key, sch in schemas.iteritems():
        key = key.strip("/")
        if "/" in key:
            split = key.split("/")
            [os.mkdir(d) for d in split[-1]]
        fpath = "{}/{}.json".format(root, key)
        with io.open(fpath, "w", encoding="utf-8") as fstream:
            fstream.write(unicode(json.dumps(sch, indent=2, separators=(',', ': '))) + u"\n")


def export_js(fpath, schemas):
    if not os.path.exists(os.path.dirname(fpath)):
        raise JrsExportError("Path not exists '{}'".format(os.path.dirname(fpath)))

    with io.open(fpath, "w", encoding="utf-8") as fstream:
        fstream.write(j2.get_template("export_js.j2").render({
            "schemas": dict([
                (
                    key, unicode(
                        json.dumps(sch, indent=2, separators=(',', ': '))
                    )
                )
                for key, sch in schemas.iteritems()
            ])
        }))
