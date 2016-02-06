PRIMARI_KEY = "read_identifier"
DEFAULT_SPECIFICATION = {
    "instrument": str,
    "run_number": int,
    "flowcell_id": str,
    "lane": int,
    "tile": int,
    "x_pos": int,
    "y_pos":  int,
    "sigle_paired": str,
    "is_filtered": str,
    "control_number": int,
    "index_sequence": str,
    "identifier_string": str,
    "sequence": str,
    "quality_marker": str,
    "quality_string": str,
}
DEFAULT_SPECIFICATION.update({PRIMARI_KEY: str})


def match_dict_with_specification(dict_to_test, specification):

    output = {}
    for field_name, field_type in specification.items():
        value_from_dict = dict_to_test.get(field_name)
        if value_from_dict is None:
            raise TypeError(
                "Specification mismatch: dict %s ommits field '%s'." %
                (dict_to_test, field_name)
            )
        if not isinstance(value_from_dict, field_type):
            raise TypeError(
                "Specification mismatch: field '%s' has value %s of type %s, "
                "but should be an instance of type %s." %
                (
                    field_name, value_from_dict,
                    type(value_from_dict), field_type
                )
            )
        output[field_name] = value_from_dict

    return output
