#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple

from remove_hairs import remove_hairs
from marcxml_parser import MARCXMLRecord
from edeposit.amqp.aleph import aleph

from ..settings import NTK_ALEPH_URL
from ..data_model import Model
from ..analyzers.source_string import SourceString


# Functions & classes =========================================================
def _first_or_none(array):
    """
    Pick first item from `array`, or return `None`, if there is none.
    """
    if not array:
        return None

    return array[0]


def _add_source(model):
    """
    Go over all attributes in `model` and add :class:`SourceString` to them.

    Args:
        model (obj): :class:`Model` instance.

    Returns:
        obj: :class:`Model` instance with :class:`SourceString` descriptors.
    """
    ignored_keys = {"author_tags"}

    # convert all values to source strings
    source = "Aleph"
    for key, val in model.get_mapping().iteritems():
        if key in ignored_keys:
            continue

        if type(val) in [list, tuple]:
            ss_val = [
                SourceString(item, source).to_dict()
                for item in val
            ]
        else:
            ss_val = [SourceString(val, source).to_dict()]

        setattr(model, key, ss_val)

    return model


def by_issn(issn):
    """
    Query aleph for records with given `issn`.

    Args:
        issn (str): ISSN of the periodical.

    Returns:
        obj: :class:`Model` instances for each record.
    """
    # monkeypatched to allow search in NTK's Aleph
    old_url = aleph.ALEPH_URL
    aleph.ALEPH_URL = NTK_ALEPH_URL
    records = aleph.getISSNsXML(issn, base="STK02")
    aleph.ALEPH_URL = old_url

    # process all records
    for record in records:
        marc = MARCXMLRecord(record)

        author = Author.parse_author(marc)

        model = Model(
            url=_first_or_none(
                marc.get("856u")
            ),
            conspect=_first_or_none(
                marc.get("072a")
            ),
            annotation_tags=_first_or_none(
                marc.get("520a")
            ),
            periodicity=_first_or_none(
                marc.get("310a")
            ),
            title_tags=_first_or_none(
                marc.get("222a")
            ),
            subtitle_tags=_first_or_none(
                marc.get("245b")
            ),
            place_tags=remove_hairs(
                _first_or_none(marc.get("260a")) or ""
            ),
            author_tags=author._asdict() if author else None,
            publisher_tags=remove_hairs(
                (
                    _first_or_none(marc.get("260b")) or
                    _first_or_none(marc.get("264b")) or
                    "",
                ),
                ", "
            ),
            # publisher_tags=,
            creation_dates=_first_or_none(
                marc.get("260c")
            ),
            lang_tags=_first_or_none(
                marc.get("040b")
            ),
            keyword_tags=marc.get("650a07"),
            source_info=_first_or_none(
                marc.get("500a")
            ),
            original_xml=record,
        )

        yield _add_source(model)


class Author(namedtuple("Author", ["name",
                                   "code",
                                   "linked_forms",
                                   "is_corporation",
                                   "record",
                                   "alt_name"])):
    @classmethod
    def parse_author(cls, marc):
        name = None
        code = None
        linked_forms = None
        is_corporation = None
        record = None

        # parse informations from the record
        if marc["100a"]:  # persons
            name = _first_or_none(marc["100a"])
            code = _first_or_none(marc["1007"])
            is_corporation = False
            record = marc.datafields["100"][0]  # transport all fields
        elif marc["110a"]:  # corporations
            name = _first_or_none(marc["110a"])
            code = _first_or_none(marc["1107"])
            linked_forms = marc["410a2 "]
            is_corporation = True
            record = marc.datafields["110"][0]  # transport all fields
        else:
            return None

        # parse linked forms (alternative names)
        linked_forms = marc["410a2 "]

        # put together alt_name
        type_descriptor = ["osoba", "organizace"]
        alt_name = "%s [%s]" % (name, type_descriptor[is_corporation])
        if linked_forms:
            alt_name += " (" + ", ".join(linked_forms) + ")"

        return cls(
            name=name,
            code=code,
            linked_forms=linked_forms,
            is_corporation=is_corporation,
            record=record,
            alt_name=alt_name,
        )

    @classmethod
    def search_by_name(cls, name):
        records = aleph.downloadRecords(
            aleph.searchInAleph("aut", name, False, "wau")
        )

        for record in records:
            marc = MARCXMLRecord(record)

            author = cls.parse_author(marc)

            if author:
                yield author
