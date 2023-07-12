class ModelStats:
    """ Extract on the data realated to the model"""

    def analyse_stats(self, fr_analysis: dict, process_runtime) -> dict:

        custom_model_stats_table = {}
        number_of_attributes_above_80 = 0
        number_of_attributes_above_90 = 0
        number_of_attributes_below_50 = 0
        total_attributes_found = 10
        if len(fr_analysis['documents']) != 0:
            custom_model_stats_table['Processing Time'] = process_runtime

            fields_raw = fr_analysis['documents'][0]
            fields = fields_raw['fields']

            for key in fields.keys():
                attribute_info = {}
                attribute_info['confidence'] = fields[key]['confidence']

                if attribute_info['confidence'] >= .8:
                    number_of_attributes_above_80 = number_of_attributes_above_80 + 1
                if attribute_info['confidence'] >= .9:
                    number_of_attributes_above_90 = number_of_attributes_above_90 + 1
                if attribute_info['confidence'] < .5:
                    number_of_attributes_below_50 = number_of_attributes_below_50 + 1
                if fields[key]['content'] == None:
                    total_attributes_found = total_attributes_found - 1

            custom_model_stats_table['Total attributes found'] = total_attributes_found
            custom_model_stats_table['Attributes above 80per confidence'] = number_of_attributes_above_80
            custom_model_stats_table['Attributes above 90per confidence'] = number_of_attributes_above_90
            custom_model_stats_table['Attributes less than 50per confidence'] = number_of_attributes_below_50
        return custom_model_stats_table
