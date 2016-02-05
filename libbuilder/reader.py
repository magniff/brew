def generate_records_from_fastq(file_descriptor_object):

    def yield_new_record(file_descriptor_object):
        next_line = lambda: next(file_descriptor_object)
        end_of_file_flag = False
        while not end_of_file_flag:
            try:
                yield {
                    "identifier_string": str.strip(next_line()),
                    "sequence": str.strip(next_line()),
                    "quality_marker": str.strip(next_line()),
                    "quality_string": str.strip(next_line()),
                }
            except StopIteration:
                end_of_file_flag = True

    yield from yield_new_record(file_descriptor_object)
