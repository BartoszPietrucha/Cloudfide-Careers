import pandas as pd
import re
#from solution import add_virtual_column


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Adds a new column to the DataFrame based on the formula provided in role.
    Returns an empty DataFrame if the column names or the formula are invalid.
    """

    #Only leters and _
    name_regex = re.compile(r'^[A-Za-z_]+$') 

    if not name_regex.fullmatch(new_column):
        return pd.DataFrame()

    #for role: spaces; leters and_; spaces; leters and _; spaces
    formula_regex = re.compile(r'^\s*[A-Za-z_]+\s*[\+\-\*]\s*[A-Za-z_]+\s*$')

    if not formula_regex.fullmatch(role):
        return pd.DataFrame()


    columns_test = [e.strip() for e in re.split(r'[\+\-\*]', role)]

    role_clean = re.sub(r'\s+', '', role)

    for col in columns_test:
        if col not in df.columns:
            return pd.DataFrame()

    try:
        result = df.copy()
        result[new_column] = result.eval(role_clean)
        return result
    except Exception:
        return pd.DataFrame()





def test_sum_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one+label_two", "label_three")
    assert df_result.equals(df_expected), f"The function should sum the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_multiplication_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 1]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one * label_two", "label_three")
    assert df_result.equals(df_expected), f"The function should multiply the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_subtraction_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 0]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one - label_two", "label_three")
    assert df_result.equals(df_expected), f"The function should subtract the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_empty_result_when_invalid_labels():
    df = pd.DataFrame([[1, 2]] * 3, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two", "label3")
    assert df_result.empty, f"Should return an empty df when the \"new_column\" is invalid.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"
    df = pd.DataFrame([[1, 2]] * 3, columns = ["label-one", "label_two"])
    df_result = add_virtual_column(df, "label-one + label_two", "label")
    assert df_result.empty, f"Should return an empty df when both df columns and roles are invalid.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"
    df = pd.DataFrame([[1, 2]] * 3, columns = ["label-one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two", "label")
    assert df_result.empty, f"Should return an empty df when a df column is invalid.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"


def test_empty_result_when_invalid_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one \ label_two", "label_three")
    assert df_result.empty, f"Should return an empty df when the role have invalid character: '\\'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"
    df_result = add_virtual_column(df, "label&one + label_two", "label_three")
    assert df_result.empty, f"Should return an empty df when the role have invalid character: '&'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"
    df_result = add_virtual_column(df, "label_five + label_two", "label_three")
    assert df_result.empty, f"Should return an empty df when the role have a column which isn't in the df: 'label_five'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"


def test_when_extra_spaces_in_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one+label_two", "label_three")
    assert df_result.equals(df_expected), f"Should work when the role haven't spaces between the operation and the column.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    df_result = add_virtual_column(df, "label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), f"Should work when the role have spaces between the operation and the column.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    df_result = add_virtual_column(df, "  label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), f"Should work when the role have extra spaces in the start/end.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"

test_sum_of_two_columns()
test_multiplication_of_two_columns()
test_subtraction_of_two_columns()
test_empty_result_when_invalid_labels()
test_empty_result_when_invalid_rules()
test_when_extra_spaces_in_rules()
