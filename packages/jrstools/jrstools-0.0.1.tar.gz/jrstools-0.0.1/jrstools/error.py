# -*- coding: utf-8 -*-
import json


class JrsError(Exception):
    pass


class JrsSchemaError(JrsError):
    pass


class JrsNodeError(JrsError):
    def __init__(self, message, node):
        self.value = u"{}. node: {}, schema_id: {}".format(
            message,
            unicode(json.dumps(node.parent, indent=2, separators=(',', ': '))),
            node.root["id"]
        )


class JrsExportError(JrsError):
    pass


class JrsMakeError(JrsError):
    pass
