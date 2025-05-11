import re
import numpy as np
import pyttsx3
from sklearn.tree import _tree

class HealthcareChatbot:
    """Chatbot for disease diagnosis with text-to-speech interaction."""
    def __init__(self, data_loader, predictor, reduced_data):
        """Initialize with data loader, predictor, and reduced data.
        Args:
            data_loader (DataLoader): Loads dataset CSVs.
            predictor (DiseasePredictor): Predicts diseases.
            reduced_data (pandas.DataFrame): Grouped symptom data for follow-up questions.
        """
        self.data_loader = data_loader
        self.predictor = predictor
        self.reduced_data = reduced_data
        self.symptoms = self.predictor.get_feature_names()  # Symptom feature names
        self.engine = pyttsx3.init()  # Initialize text-to-speech engine
        self.engine.setProperty('voice', "english+f5")  # Set voice
        self.engine.setProperty('rate', 130)  # Set speech rate

    def speak(self, text):
        """Speak text using pyttsx3.
        Args:
            text (str): Text to be spoken.
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def check_pattern(self, dis_list, inp):
        """Check if input matches symptom patterns using regex.
        Args:
            dis_list (list): List of possible symptoms.
            inp (str): User input symptom.
        Returns:
            tuple: (1, matched symptoms) if match found, (0, []) otherwise.
        """
        inp = inp.replace(' ', '_')  # Normalize input
        patt = f"{inp}"
        regexp = re.compile(patt)
        pred_list = [item for item in dis_list if regexp.search(item)]  # Find matches
        if len(pred_list) > 0:
            return 1, pred_list
        return 0, []

    def calc_condition(self, symptoms_exp, days):
        """Calculate severity score and provide medical advice.
        Args:
            symptoms_exp (list): List of confirmed symptoms.
            days (int): Number of days symptoms have been present.
        """
        severity_dict = self.data_loader.load_severity()
        # Sum severity scores for present symptoms
        sum_severity = sum(severity_dict.get(item, 0) for item in symptoms_exp)
        # Calculate severity score
        if (sum_severity * days) / (len(symptoms_exp) + 1) > 13:
            print("You should take the consultation from doctor.")
            self.speak("You should take the consultation from doctor.")
        else:
            print("It might not be that bad but you should take precautions.")
            self.speak("It might not be that bad but you should take precautions.")

    def get_user_symptoms(self, tree):
        """Collect symptoms from user input using the decision tree.
        Args:
            tree: Trained decision tree model.
        """
        tree_ = tree.tree_
        # Map node features to symptom names
        feature_name = [
            self.symptoms[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        chk_dis = ",".join(self.symptoms).split(",")  # List of symptoms
        symptoms_present = []

        # Get initial symptom
        while True:
            print("\nEnter the symptom you are experiencing  \t\t", end="->")
            disease_input = input("")
            conf, cnf_dis = self.check_pattern(chk_dis, disease_input)
            if conf == 1:
                print("searches related to input: ")
                for num, it in enumerate(cnf_dis):
                    print(num, ")", it)
                if num != 0:
                    print(f"Select the one you meant (0 - {num}):  ", end="")
                    conf_inp = int(input(""))
                else:
                    conf_inp = 0
                disease_input = cnf_dis[conf_inp]
                break
            else:
                print("Enter valid symptom.")

        # Get duration of symptoms
        while True:
            try:
                num_days = int(input("Okay. From how many days ? : "))
                break
            except:
                print("Enter valid input.")

        symptoms_exp = [disease_input]  # Initialize with primary symptom

        def recurse(node, depth):
            """Recursively traverse the decision tree to collect symptoms and predict."""
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                val = 1 if name == disease_input else 0
                if val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                # Predict disease from node
                present_disease = self.predictor.print_disease(tree_.value[node])
                # Get related symptoms for follow-up questions
                red_cols = self.reduced_data.columns
                symptoms_given = red_cols[self.reduced_data.loc[present_disease].values[0].nonzero()]
                print("Are you experiencing any ")
                for syms in list(symptoms_given):
                    inp = ""
                    print(syms, "? : ", end='')
                    while True:
                        inp = input("")
                        if inp in ["yes", "no"]:
                            break
                        print("provide proper answers i.e. (yes/no) : ", end="")
                    if inp == "yes":
                        symptoms_exp.append(syms)
                # Calculate severity
                self.calc_condition(symptoms_exp, num_days)
                # Predict using collected symptoms
                second_prediction = self.predictor.predict(symptoms_exp)
                description_list = self.data_loader.load_descriptions()
                precaution_dict = self.data_loader.load_precautions()
                # Compare tree and model predictions
                if present_disease[0] == second_prediction:
                    print("You may have ", present_disease[0])
                    print(description_list.get(present_disease[0], "Description not available"))
                    self.speak(f"You may have {present_disease[0]}")
                    self.speak(description_list.get(present_disease[0], ""))
                else:
                    print("You may have ", present_disease[0], "or ", second_prediction)
                    print(description_list.get(present_disease[0], "Description not available"))
                    print(description_list.get(second_prediction, "Description not available"))
                    self.speak(f"You may have {present_disease[0]} or {second_prediction}")
                    self.speak(description_list.get(present_disease[0], ""))
                    self.speak(description_list.get(second_prediction, ""))
                # Display precautions
                precaution_list = precaution_dict.get(present_disease[0], [])
                print("Take following measures : ")
                for i, j in enumerate(precaution_list):
                    if j:
                        print(i + 1, ")", j)
                        self.speak(j)

        recurse(0, 1)
        print("-" * 80)

    def run(self):
        """Run the chatbot interaction, starting with user greeting."""
        print("-----------------------------------HealthCare ChatBot-----------------------------------")
        print("\nYour Name? \t\t\t\t", end="->")
        name = input("")
        self.speak(f"Hello, {name}")
        print(f"Hello, {name}\n")
        self.get_user_symptoms(self.predictor.model)