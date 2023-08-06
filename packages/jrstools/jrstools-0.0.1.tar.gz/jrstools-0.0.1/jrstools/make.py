# -*- coding: utf-8 -*-
import os
import io

from error import JrsMakeError

from jinja2 import Environment, FileSystemLoader

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))


def make_docs(
        dst,
        schemas,
        index_path=os.path.join(MODULE_DIR, "templates/docs_index.j2"),
        schema_path=os.path.join(MODULE_DIR, "templates/docs_schema.j2")
    ):
    index_path = os.path.abspath(index_path)
    schema_path = os.path.abspath(schema_path)

    if not os.path.exists(index_path):
        raise JrsMakeError("File not exists: '{}'".format(index_path))

    if not os.path.exists(schema_path):
        raise JrsMakeError("File not exists: '{}'".format(schema_path))

    SCHEMAS_DIR = os.path.join(dst, "schemas")
    if not os.path.exists(SCHEMAS_DIR):
        os.mkdir(SCHEMAS_DIR)

    index_dir, index_name = index_path.rsplit("/", 1)
    j2_index = Environment(loader=FileSystemLoader(index_dir), trim_blocks=True, lstrip_blocks=True)
    docs_index = j2_index.get_template(index_name)

    with io.open(os.path.join(dst, "index.md"), "w", encoding="utf-8") as fstream:
        fstream.write(docs_index.render({"schemas": schemas}))

    schema_dir, schema_name = schema_path.rsplit("/", 1)
    j2_schema = Environment(loader=FileSystemLoader(schema_dir), trim_blocks=True, lstrip_blocks=True,
        extensions=["jinja2.ext.with_"])
    j2_schema.filters["type"] = lambda value, expected: type(value) == expected
    j2_schema.filters["intersectionAny"] = lambda arr1, arr2: len(set(arr1).intersection(arr2)) > 0
    j2_schema.filters["intersectionValue"] = lambda arr1, arr2: list(set(arr1).intersection(arr2))[0]
    docs_schema = j2_schema.get_template(schema_name)

    for sch in schemas.itervalues():
        with io.open(os.path.join(SCHEMAS_DIR, sch["id"] + ".md"), "w", encoding="utf-8") as fstream:
            fstream.write(docs_schema.render({"schema": sch}))
