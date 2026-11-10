from app.sql_validator import validate_sql


def test_select_is_allowed():

    valid, message = validate_sql(
        "SELECT * FROM customers;"
    )

    assert valid is True


def test_delete_is_blocked():

    valid, message = validate_sql(
        "DELETE FROM customers;"
    )

    assert valid is False


def test_drop_is_blocked():

    valid, message = validate_sql(
        "DROP TABLE customers;"
    )

    assert valid is False


def test_update_is_blocked():

    valid, message = validate_sql(
        "UPDATE customers SET city = 'Delhi';"
    )

    assert valid is False


def test_multiple_statements_are_blocked():

    valid, message = validate_sql(
        "SELECT * FROM customers; DELETE FROM customers;"
    )

    assert valid is False


def test_empty_query_is_blocked():

    valid, message = validate_sql("")

    assert valid is False

from app.main import contains_dangerous_intent


def test_delete_intent_is_blocked():
    assert contains_dangerous_intent("Delete all customers") is True


def test_drop_intent_is_blocked():
    assert contains_dangerous_intent("Drop the customers table") is True


def test_update_intent_is_blocked():
    assert contains_dangerous_intent("Update all customers to Delhi") is True


def test_insert_intent_is_blocked():
    assert contains_dangerous_intent("Insert a new customer") is True


def test_normal_question_is_allowed():
    assert contains_dangerous_intent(
        "Show me customers from Delhi"
    ) is False