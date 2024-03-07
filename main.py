from pprint import pprint
from datetime import datetime
import json
import re

class JsonTransformer:
    def __init__(self, input_file: str):
        self.input_data = self.load_json(input_file)
        self.transformed_output = []
        
    
    def load_json(self, file_name: str):
        # import pdb;pdb.set_trace()
        with open(file_name, "r") as json_file:
            json_obj = json.load(json_file)
        return json_obj
    
    def is_rfc3339_formatted(self, input_string):
        rfc3339_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|([+-]\d{2}:\d{2}))$')

        return bool(rfc3339_pattern.match(input_string))
        
    def transform(self):
        
        for key, value in self.input_data.items():
            
            key = key.strip()

            if not key:
                continue
            
            data_type, value = next(iter(value.items()))
            data_type = data_type.strip()
            if data_type == 'S':
                transformed_value = self._transform_string(value)
            elif data_type == 'N':
                transformed_value = self._transform_number(value)
            elif data_type == 'BOOL':
                transformed_value = self._transform_boolean(value)
            elif data_type == 'NULL':
                transformed_value = self._transform_null(value)
            elif data_type == 'L':
                transformed_value = self._transform_list(value)
            elif data_type == 'M':
                transformed_value = self._transform_map(value)
            else:
                continue
            
            if transformed_value is not None:
                self.transformed_output.append({key: transformed_value})
        
        return self.transformed_output

    def _transform_string(self, value):

        value = value.strip()

        if value.isdigit() and value != '0':
            return int(value)
        
        if not value:
            return None

        
        if self.is_rfc3339_formatted(value):
            try:
                datetime_obj = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return int(datetime_obj.timestamp())
            except ValueError:
                return f"Incorrect ISO time stamp format: {value}"
        else:
            return str(value)

    def _transform_number(self, value):

        value = value.strip().lstrip('0')

        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None
    
    def _transform_boolean(self, value):

        value = value.strip().lower()

        if value in ('1', 't', 'true'):
            return "true"
        elif value in ('0', 'f', 'false'):
            return "false"
        else:
            return None
    
    def _transform_null(self, value):

        value = value.strip().lower()

        if value in ('1', 't', 'true'):
            return "null"
        else:
            return None

    def _transform_list(self, value):

        if not value or not isinstance(value, list):
            return None
        
        transformed_list = []

        for item in value:
            if not isinstance(item, dict):
                continue
            item_type, item_value = next(iter(item.items()))
            item_type = item_type.strip()
            if item_type == 'S':
                transformed_item = self._transform_string(item_value)
            elif item_type == 'N':
                transformed_item = self._transform_number(item_value)
            elif item_type == 'BOOL':
                transformed_item = self._transform_boolean(item_value)
            elif item_type == 'NULL':
                transformed_item = self._transform_null(item_value)
            elif item_type == 'L':
                transformed_item = self._transform_list(item_value)
            elif item_type == 'M':
                transformed_item = self._transform_map(item_value)
            else:
                continue

            if transformed_item is not None:
                transformed_list.append(transformed_item)
        
        return transformed_list if len(transformed_list) else None

    def _transform_map(self, value):

        if not value or not isinstance(value, dict):
            return None
        
        transformed_map = {}

        for sub_key, sub_item in value.items():
            sub_key = sub_key.strip()
            item_type, item_value = next(iter(sub_item.items()))
            item_type = item_type.strip()  
            if item_type == 'S':
                transformed_item = self._transform_string(item_value)
            elif item_type == 'N':
                transformed_item = self._transform_number(item_value)
            elif item_type == 'BOOL':
                transformed_item = self._transform_boolean(item_value)
            elif item_type == 'NULL':
                transformed_item = self._transform_null(item_value)
            elif item_type == 'L':
                transformed_item = self._transform_list(item_value)
            elif item_type == 'M':
                transformed_item = self._transform_map(item_value)
            else:
                continue
            
            if transformed_item is not None:
                transformed_map[sub_key] = transformed_item
        
        return transformed_map


def main():
    json_transformer = JsonTransformer("input.json")
    formatted_json = json_transformer.transform()
    pprint(formatted_json, indent=1)
    
if __name__ == "__main__":
    main()