import pandas as pd
import csv
import os

file_path = os.path.join(os.getcwd(), 'Data', 'Training.csv')
class DataLoader:
    """Loads healthcare dataset CSV files and dictionaries for symptoms and diseases."""
    def __init__(self, data_dir='Data', master_dir='MasterData'):
        """Initialize with directory paths for data and metadata.
        Args:
            data_dir (str): Path to training/testing data (default: 'Data').
            master_dir (str): Path to metadata files (default: 'MasterData').
        """
        self.data_dir = data_dir
        self.master_dir = master_dir
        self.training_data = None  # Store Training.csv data
        self.testing_data = None   # Store Testing.csv data
        self.description_list = {} # Dictionary for disease descriptions
        self.severity_dict = {}    # Dictionary for symptom severity scores
        self.precaution_dict = {}  # Dictionary for disease precautions

    def load_training_data(self):
        """Load Training.csv containing symptom-disease mappings.
        Returns:
            pandas.DataFrame: Training data with symptoms and prognosis.
        """
        file_path = os.path.join(self.data_dir, 'Training.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        self.training_data = pd.read_csv(file_path)
        return self.training_data

    def load_testing_data(self):
        """Load Testing.csv for model evaluation.
        Returns:
            pandas.DataFrame: Testing data with symptoms and prognosis.
        """
        file_path = os.path.join(self.data_dir, 'Testing.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        self.testing_data = pd.read_csv(file_path)
        return self.testing_data

    def load_descriptions(self):
        """Load symptom_Description.csv with disease descriptions.
        Returns:
            dict: Dictionary mapping diseases to their descriptions.
        """
        file_path = os.path.join(self.master_dir, 'symptom_Description.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.description_list[row[0]] = row[1]  # Map disease to description
        return self.description_list

    def load_severity(self):
        """Load symptom_severity.csv with symptom severity scores.
        Returns:
            dict: Dictionary mapping symptoms to severity scores (int).
        """
        file_path = os.path.join(self.master_dir, 'symptom_severity.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            try:
                for row in csv_reader:
                    self.severity_dict[row[0]] = int(row[1])  # Map symptom to severity
            except:
                pass  # Skip invalid rows
        return self.severity_dict

    def load_precautions(self):
        """Load symptom_precaution.csv with disease precautions.
        Returns:
            dict: Dictionary mapping diseases to lists of precautions.
        """
        file_path = os.path.join(self.master_dir, 'symptom_precaution.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.precaution_dict[row[0]] = [row[1], row[2], row[3], row[4]]  # Map disease to precautions
        return self.precaution_dict