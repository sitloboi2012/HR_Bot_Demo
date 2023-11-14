# -*- coding: utf-8 -*-
from __future__ import annotations

from langchain.schema import Document as LangChainDocument

import unicodedata


def parsing_keyword(raw_text: str, keyword_list: list):
    # sourcery skip: assign-if-exp, dict-comprehension, inline-immediately-returned-variable, remove-redundant-if
    indx = []
    for keyword in keyword_list:
        if keyword in raw_text:
            indx.append(raw_text.find(keyword))
        else:
            # you may have to do some processing here if keys is not found
            print("Key not found")

    dic = {}
    for i in range(len(keyword_list)):
        if i != len(keyword_list) - 1:
            dic[keyword_list[i]] = raw_text[(indx[i] + len(keyword_list[i])) : indx[i + 1]].strip()
        elif i == len(keyword_list) - 1:
            dic[keyword_list[i]] = raw_text[indx[i] + len(keyword_list[i]) :].strip()

    return dic


def convert_to_document(dict_values: str, filename: str, role: str):
    return [
        LangChainDocument(
            page_content=": ".join([role, key, value]),
            metadata={"source": filename, "role": role, "information": key},
        )
        for key, value in dict_values.items()
    ]


def chunking_job_description(raw_text: LangChainDocument):
    clean_text = unicodedata.normalize("NFKD", raw_text.page_content)
    clean_text = " \n\n ".join(clean_text.split("\n\n")).lower()
    return parsing_keyword(clean_text, ["job description", "requirements", "benefit"])
