from table_analyzer import extract_tables


def compare_table_structures(template_path, target_path):
    template_tables = extract_tables(template_path)
    target_tables = extract_tables(target_path)

    results = []

    # Compare number of tables
    if len(template_tables) == len(target_tables):
        results.append(f"✓ Number of tables matches ({len(template_tables)})")
    else:
        results.append(
            f"✗ Number of tables differs "
            f"(Template: {len(template_tables)}, "
            f"Target: {len(target_tables)})"
        )

    max_tables = max(len(template_tables), len(target_tables))

    for i in range(max_tables):
        if i >= len(template_tables):
            results.append(f"✗ Extra table found in target: Table {i+1}")
            continue

        if i >= len(target_tables):
            results.append(f"✗ Missing table in target: Table {i+1}")
            continue

        template_table = template_tables[i]
        target_table = target_tables[i]

        # Row count
        if template_table["rows"] == target_table["rows"]:
            results.append(
                f"✓ Table {i+1}: Row count matches "
                f"({template_table['rows']})"
            )
        else:
            results.append(
                f"✗ Table {i+1}: Row count differs "
                f"(Template: {template_table['rows']}, "
                f"Target: {target_table['rows']})"
            )

        # Column count
        if template_table["columns"] == target_table["columns"]:
            results.append(
                f"✓ Table {i+1}: Column count matches "
                f"({template_table['columns']})"
            )
        else:
            results.append(
                f"✗ Table {i+1}: Column count differs "
                f"(Template: {template_table['columns']}, "
                f"Target: {target_table['columns']})"
            )

        # Compare cell content
        rows_to_compare = min(template_table["rows"], target_table["rows"])

        for row_index in range(rows_to_compare):
            template_row = template_table["data"][row_index]
            target_row = target_table["data"][row_index]

            cols_to_compare = min(len(template_row), len(target_row))

            for col_index in range(cols_to_compare):
                template_text = template_row[col_index].strip()
                target_text = target_row[col_index].strip()

                # Skip empty cells
                if not template_text and not target_text:
                    continue

                if template_text.lower() == target_text.lower():
                    results.append(
                        f"✓ Table {i+1}, Row {row_index+1}, "
                        f"Cell {col_index+1}: Content matches"
                    )
                else:
                    results.append(
                        f"✗ Table {i+1}, Row {row_index+1}, "
                        f"Cell {col_index+1}: Content differs\n"
                        f"   Template: {template_text}\n"
                        f"   Target  : {target_text}"
                    )

    return results
