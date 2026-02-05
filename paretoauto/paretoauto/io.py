# csv/excel/hiphops loading and linking indices back to original rows

import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET


def load_csv(filepath, objective_columns=None):
    # load csv file & return points array with source info for data linking
    df = pd.read_csv(filepath)

    if objective_columns is None:
        # get all numeric columns
        numeric_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        objective_columns = numeric_cols

    points = df[objective_columns].to_numpy()

    source_info = {
        "filepath": filepath,
        "columns": objective_columns,
        "dataframe": df,
    }

    return points, source_info


def load_excel(filepath, sheet_name=0, objective_columns=None):
    # load excel file & return points array with source info for data linking
    df = pd.read_excel(filepath, sheet_name=sheet_name)

    if objective_columns is None:
        numeric_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        objective_columns = numeric_cols

    points = df[objective_columns].to_numpy()

    source_info = {
        "filepath": filepath,
        "sheet": sheet_name,
        "columns": objective_columns,
        "dataframe": df,
    }

    return points, source_info


def get_source_rows(indices, source_info):
    # get original dataframe rows for given point indices
    df = source_info["dataframe"]
    return df.iloc[indices].copy()


def save_with_fronts(source_info, ranks, fronts, output_filepath):
    # save data with pareto_front column added so you can filter in excel
    df = source_info["dataframe"].copy()
    df["Pareto_Front"] = ranks

    # check extension to decide csv or excel
    if output_filepath.endswith('.xlsx') or output_filepath.endswith('.xls'):
        df.to_excel(output_filepath, index=False)
    else:
        df.to_csv(output_filepath, index=False)

    return df


def print_row_references(indices, source_info, front_number=0):
    # prints which excel rows the pareto points are from
    # excel rows are 1-indexed and have header so add 2
    excel_rows = [idx + 2 for idx in indices]

    print(f"\nFront {front_number} corresponds to these rows in Excel/CSV:")
    print(f"  Row numbers: {', '.join(map(str, excel_rows))}")
    print(f"  (Row 1 is the header)")

    # show first column values for reference
    df = source_info["dataframe"]
    if len(df.columns) > 0 and hasattr(df.index, 'name'):
        first_col = df.columns[0]
    else:
        first_col = df.columns[0] if len(df.columns) > 0 else None

    if first_col:
        values = df.iloc[indices][first_col].tolist()
        print(f"  Items: {', '.join(map(str, values))}")


# --- HiP-HOPS XML/JS loading ---

def load_hiphops(filepath):
    """Load HiP-HOPS optimisation output (.xml or .js file)."""
    with open(filepath, 'r', encoding='iso-8859-1') as f:
        content = f.read()

    # .js files wrap xml in a variable: var OptimisationState = '<?xml ...>';
    if filepath.endswith('.js'):
        start = content.find("'<?xml")
        if start != -1:
            content = content[start + 1 : content.rfind("'")]

    root = ET.fromstring(content)
    nsga = root.find('NSGA')

    # get objective names (e.g. ['Cost', 'Risk'])
    objectives = nsga.find('Objectives')
    obj_names = [obj.find('Name').text for obj in objectives]

    model_name = root.get('model', 'unknown')
    generation = nsga.find('Generation').text

    # parse each individual in the pareto front
    pop = nsga.find('NonDominatedPopulation')
    individuals = []
    points_list = []

    for ind in pop:
        ind_id = ind.find('IndividualID').text

        # extract objective values
        obj_values = {}
        for eval_elem in ind.find('Evaluations'):
            name = eval_elem.find('Name').text
            value = float(eval_elem.find('Value').text)
            obj_values[name] = value

        # extract component config
        encoding = _extract_encoding(ind.find('Encoding'))

        individuals.append({
            'id': ind_id,
            'objectives': obj_values,
            'encoding': encoding
        })
        points_list.append([obj_values[name] for name in obj_names])

    points = np.array(points_list)

    # build dataframe for consistency with csv/excel loaders
    df = pd.DataFrame([
        {'IndividualID': ind['id'], **ind['objectives']}
        for ind in individuals
    ])

    source_info = {
        'filepath': filepath,
        'columns': obj_names,
        'dataframe': df,
        'model': model_name,
        'generation': generation,
        'individuals': individuals,  # full config for hover
        'type': 'hiphops'
    }

    return points, source_info


def _extract_encoding(encoding_elem):
    """Walk the tree encoding and pull out component -> implementation mappings."""
    components = {}

    def walk(node):
        comp = node.find('Component')
        if comp is not None:
            name = comp.find('Name').text
            impl = comp.find('Implementation/Name').text
            components[name] = impl

        subnodes = node.find('SubNodes')
        if subnodes is not None:
            for child in subnodes:
                walk(child)

    tree_enc = encoding_elem.find('TreeEncoding')
    if tree_enc is not None:
        for node in tree_enc:
            walk(node)

    return components