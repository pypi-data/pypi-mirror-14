# -*- coding: utf-8 -*-
from copy import deepcopy
from error import JrsNodeError


class Node(object):
    schemas = {}

    @classmethod
    def set_schemas(cls, schemas):
        cls.schemas = schemas

    def _check_ref(self):
        if not type(self.value["$ref"]) == str:
            raise JrsNodeError(u"must be string", self)
        try:
            index = self.value["$ref"].index("#")
            if index != self.value["$ref"].rindex("#"):
                raise JrsNodeError(u"must exists one \"#\"", self)
        except ValueError:
            raise JrsNodeError(u"\"#\" must exists", self)

    def _set_ref(self):
        if self.value["$ref"].index("#") == 0:
            self.ref["path"] = self.value["$ref"].strip("#")
            self.ref["context"] = self.root
        else:
            schemaId, path = self.value["$ref"].split("#")
            if not schemaId in self.schemas:
                raise JrsNodeError(u"Schema not exists", self)
            self.ref["path"] = path
            self.ref["context"] = self.schemas[schemaId]

    def replace_ref(self):
        if self.ref["path"] == "":
            self.parent[self.key] = deepcopy(self.ref["context"])
        else:
            res = self.ref["context"]
            for key in self.ref["path"].lstrip("/").split("/"):
                if key in res:
                    res = res[key]
                else:
                    raise JrsNodeError(u"Can't resolve ref path", self)
            self.parent[self.key] = deepcopy(res)

        self.parent[self.key]["resolved_$ref"] = self.value["$ref"]

    def __init__(self, key, node, parent, root):
        self.value = node
        self.key = key
        self.parent = parent
        self.root = root
        self.ref = {}

        self.is_string = type(self.value) == str
        self.is_dict = type(self.value) == dict
        self.is_list = type(self.value) == list
        self.is_ref = self.is_dict and "$ref" in self.value

        if self.is_ref:
            self._check_ref()
            self._set_ref()

    def childs(self):
        childs = []
        if self.is_dict:
            childs = [Node(key, child, self.value, self.root) for key, child in self.value.iteritems()]
        elif self.is_list:
            childs = [Node(index, child, self.value, self.root) for index, child in enumerate(self.value)]
        return childs
