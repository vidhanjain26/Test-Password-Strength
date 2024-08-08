import tkinter as tk
from tkinter import ttk
import re

class PasswordAnalyzer:
    def __init__(self, password):
        self.password = password
        self.length_criteria = 8
        self.uppercase_criteria = 1
        self.lowercase_criteria = 1
        self.number_criteria = 1
        self.special_criteria = 1

    def analyze(self):
        length = len(self.password)
        uppercases = sum(1 for c in self.password if c.isupper())
        lowercases = sum(1 for c in self.password if c.islower())
        numbers = sum(1 for c in self.password if c.isdigit())
        specials = sum(1 for c in self.password if not c.isalnum())

        length_score = length >= self.length_criteria
        uppercase_score = uppercases >= self.uppercase_criteria
        lowercase_score = lowercases >= self.lowercase_criteria
        number_score = numbers >= self.number_criteria
        special_score = specials >= self.special_criteria

        common_patterns = re.compile(r'(password|1234|admin|qwerty)', re.IGNORECASE)
        common_pattern_score = not bool(common_patterns.search(self.password))

        overall_score = sum([
            length_score, uppercase_score, lowercase_score,
            number_score, special_score, common_pattern_score
        ])

        return {
            "length": length,
            "uppercases": uppercases,
            "lowercases": lowercases,
            "numbers": numbers,
            "specials": specials,
            "common_patterns": common_pattern_score,
            "overall_score": overall_score,
            "strength": self.get_strength(overall_score),
            "recommendations": self.get_recommendations()
        }

    def get_strength(self, score):
        if score == 6:
            return "Very Strong"
        elif score >= 4:
            return "Strong"
        elif score >= 2:
            return "Moderate"
        else:
            return "Weak"

    def get_recommendations(self):
        recommendations = []
        if len(self.password) < self.length_criteria:
            recommendations.append(f"Increase length to at least {self.length_criteria} characters.")
        if sum(1 for c in self.password if c.isupper()) < self.uppercase_criteria:
            recommendations.append("Include at least one uppercase letter.")
        if sum(1 for c in self.password if c.islower()) < self.lowercase_criteria:
            recommendations.append("Include at least one lowercase letter.")
        if sum(1 for c in self.password if c.isdigit()) < self.number_criteria:
            recommendations.append("Include at least one number.")
        if sum(1 for c in self.password if not c.isalnum()) < self.special_criteria:
            recommendations.append("Include at least one special character.")
        if re.search(r'(password|1234|admin|qwerty)', self.password, re.IGNORECASE):
            recommendations.append("Avoid common words and patterns.")

        return recommendations

def update_results(*args):
    password = password_var.get()
    analyzer = PasswordAnalyzer(password)
    analysis = analyzer.analyze()
    result = (
        f"Length: {analysis['length']}\n"
        f"Uppercase Letters: {analysis['uppercases']}\n"
        f"Lowercase Letters: {analysis['lowercases']}\n"
        f"Numbers: {analysis['numbers']}\n"
        f"Special Characters: {analysis['specials']}\n"
        f"Common Patterns: {'No' if analysis['common_patterns'] else 'Yes'}\n"
        f"Overall Strength: {analysis['strength']}\n"
    )
    recommendations = "\n".join(analysis['recommendations'])
    result_text.set(result + "\nRecommendations:\n" + recommendations)

# Set up GUI
root = tk.Tk()
root.title("Password Analyzer")
root.geometry("450x450")
root.configure(bg="black")

style = ttk.Style()
style.configure("TFrame", background="black")  # Frame background color
style.configure("TLabel", background="black", foreground="green", font=("Helvetica", 12))  # Label style
style.configure("TButton", background="#FF6347", foreground="yellow", font=("Helvetica", 12), padding=10)  # Change button font color
style.map("TButton", background=[('active', '#FF4500')])  # Button hover style

frame = ttk.Frame(root, padding="20", style="TFrame")
frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(frame, text="Password Strength Analyzer", font=("Helvetica", 16, "bold"), foreground="green", background="black")
title_label.pack(pady=10)

label_password = ttk.Label(frame, text="Enter Password:", style="TLabel")
label_password.pack(pady=10)

password_var = tk.StringVar()
password_var.trace_add("write", update_results)

entry_password = ttk.Entry(frame, textvariable=password_var, show='*', font=("Helvetica", 12))
entry_password.pack(pady=10, fill=tk.X)

# Label to display results
result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text, style="TLabel")
result_label.pack(pady=10)

root.mainloop()
