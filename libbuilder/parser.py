import pipe

from .specification import default_specification, match_dict_with_specification


def parse_identifier(identifier_string):
    """For format specification see
    http://support.illumina.com/help/SequencingAnalysisWorkflow/Content/Vault/
    Informatics/Sequencing_Analysis/CASAVA/swSEQ_mCA_FASTQFiles.htm
    """
    read_identifier, description = identifier_string.strip("@").split()
    read_identifier_splited = read_identifier.split(":")
    description_splited = description.split(":")
    return {
        "read_identifier": read_identifier,
        "instrument": read_identifier_splited[0],
        "run_number": int(read_identifier_splited[1]),
        "flowcell_id": read_identifier_splited[2],
        "lane": int(read_identifier_splited[3]),
        "tile": int(read_identifier_splited[4]),
        "x_pos": int(read_identifier_splited[5]),
        "y_pos": int(read_identifier_splited[6]),
        "sigle_paired": "single" if description_splited[0] == "1" else "paired",
        "is_filtered": description_splited[1],
        "control_number": int(description_splited[2]),
        "index_sequence": description_splited[3],
    }


DEFAULT_PARSE_ROUTINES = {"identifier_string": parse_identifier}


@pipe.Pipe
def parse_records(records, parse_routines=None, specification=None):
    parse_routines = parse_routines or DEFAULT_PARSE_ROUTINES
    specification = specification or default_specification

    for record in records:
        parsed_record = record.copy()
        for key, parser in parse_routines.items():
            field_value = record.get(key)
            if field_value is None:
                raise ValueError("No parser for field %." % key)
            parsed_record.update(parser(field_value))

        yield match_dict_with_specification(parsed_record, specification)
