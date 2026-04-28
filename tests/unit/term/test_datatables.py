"""
Book tests.
"""

import pytest
from lute.term.datatables import get_data_tables_list
from lute.db import db
from lute.models.term import TermReference
from tests.utils import add_terms


@pytest.fixture(name="_dt_params")
def fixture_dt_params():
    "Sample query params."
    columns = [
        {"data": "0", "name": "WoID", "searchable": False, "orderable": False},
        {"data": "1", "name": "WoText", "searchable": True, "orderable": True},
    ]
    params = {
        "draw": "1",
        "columns": columns,
        "order": [{"column": "1", "dir": "asc"}],
        "start": "0",
        "length": "10",
        "search": {"value": "", "regex": False},
        # Filters - set "manually" in the route.
        # Cheating here ... had to look at the request payload
        # in devtools to see what was being sent.
        "filtLanguage": "null",  # Ha!
        "filtParentsOnly": "false",
        "filtAgeMin": "",
        "filtAgeMax": "",
        "filtStatusMin": "0",
        "filtStatusMax": "99",
        "filtIncludeIgnored": "false",
        "filtTermIDs": "",
    }
    return params


def test_smoke_term_datatables_query_runs(app_context, _dt_params):
    """
    Smoke test only, ensure query runs.
    """
    get_data_tables_list(_dt_params, db.session)
    # print(d['data'])
    a = 1
    assert a == 1, "dummy check"


def test_smoke_query_with_filter_params_runs(app_context, _dt_params):
    "Smoke test with filters set."
    _dt_params["filtLanguage"] = "44"
    _dt_params["filtParentsOnly"] = "true"
    _dt_params["filtAgeMin"] = "1"
    _dt_params["filtAgeMax"] = "10"
    _dt_params["filtStatusMin"] = "2"
    _dt_params["filtStatusMax"] = "4"
    _dt_params["filtIncludeIgnored"] = "true"
    _dt_params["filtTermIDs"] = "42,43"
    get_data_tables_list(_dt_params, db.session)


def test_parents_included_in_termids_query(app_context, _dt_params, spanish):
    "For term list viewing from page, it's useful to see parents as well."
    # pylint: disable=unbalanced-tuple-unpacking
    [t, p, g] = add_terms(spanish, ["T", "P", "G"])
    t.add_parent(p)
    p.add_parent(g)
    db.session.add(t)
    db.session.add(p)
    db.session.commit()

    _dt_params["filtTermIDs"] = f"{t.id}"
    d = get_data_tables_list(_dt_params, db.session)
    terms = [t["WoText"] for t in d["data"]]
    terms = sorted(terms)
    assert terms == ["P", "T"]


def test_latest_reference_included(app_context, _dt_params, spanish):
    "Term listing returns the most recently saved reader reference."
    # pylint: disable=unbalanced-tuple-unpacking
    [_term_without_ref, term_with_ref] = add_terms(spanish, ["sin ref", "una ciudad"])
    db.session.add(
        TermReference(
            term_id=term_with_ref.id,
            book_title="Older",
            sentence_html="Older <b>una ciudad</b>.",
        )
    )
    db.session.add(
        TermReference(
            term_id=term_with_ref.id,
            book_title="Aladino y la lámpara maravillosa",
            sentence_html=(
                "But don&#39;t delete &quot;unknown&quot; at AT&amp;T "
                "while going <b>through</b>."
            ),
        )
    )
    db.session.commit()

    d = get_data_tables_list(_dt_params, db.session)
    rows = {row["WoText"]: row for row in d["data"]}
    assert rows["sin ref"]["TrBookTitle"] is None
    assert rows["sin ref"]["TrSentenceHTML"] is None
    assert rows["una ciudad"]["TrBookTitle"] == "Aladino y la lámpara maravillosa"
    assert (
        rows["una ciudad"]["TrSentenceHTML"]
        == "But don&#39;t delete &quot;unknown&quot; at AT&amp;T while going <b>through</b>."
    )
