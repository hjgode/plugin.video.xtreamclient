#series xtream API
# Module: series_xtream
# Author: HJ_G.
# Created on: 09.12.2021
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import json

class Categories:
    def __init__(self):
        self.categories={}
    def add(self,name, cat_id):
        self.categories[name]={}
        self.categories[name]['category_name']=name
        self.categories[name]["category_id"]=cat_id
    def get_categories(self):
        return self.categories
    def get_id(self, cat_name):
        return self.categories[cat_name]["category_id"]
    def get_name(self, cat_id):
        for c in self.categories:
            id=self.get_id(c)
            if id==cat_id:
                return self.categories[c]["category_name"]
        return None
    def __str__(self) -> str:
        s=""
        for k in self.categories.keys():
            s+=k+"="
            for k1,v1 in self.categories[k].items():
                s+=k1+":"+v1+", "
            s+="\n"
        return s
