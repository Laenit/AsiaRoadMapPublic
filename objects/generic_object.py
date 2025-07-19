from utils.json_utils import load_data, save_data


class GenericObejct():
    def __init__(self, input_data_path, output_data_path):
        self.input_data_path = input_data_path
        self.output_data_path = output_data_path

        self.data_file = load_data(self.input_data_path)

    def change_key(self, new_key, path):
        current = self.data_file
        for key in path[:-1]:
            current = current[key]
        current[new_key] = current.pop(path[-1])
        save_data(self.data_file, self.output_data_path)
        self.data_file = load_data(self.output_data_path)

    def change_value(self, new_value, path):
        current = self.data_file
        for key in path[:-1]:
            current = current[key]
        current[path[-1]] = new_value
        save_data(self.data_file, self.output_data_path)
        self.data_file = load_data(self.output_data_path)

    def delete_item(self, path):
        current = self.data_file
        for key in path[:-1]:
            current = current[key]
        del current[path[-1]]
        save_data(self.data_file, self.output_data_path)
        self.data_file = load_data(self.output_data_path)

    def get_information(self, path):
        current = self.data_file
        for key in path[:-1]:
            current = current[key]
        return current[path[-1]]
