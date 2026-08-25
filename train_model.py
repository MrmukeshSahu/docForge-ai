import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def train_dummy_model():
    print("[*] Generating expanded synthetic dataset for ML model...")
    # Features: [word_count, bold_ratio, title_case_ratio, ends_with_punct, has_verb, has_noun]
    
    X = []
    y = []
    
    # 1. Title (short, bold/title case, no punct)
    for _ in range(60):
        X.append([np.random.randint(1, 15), np.random.uniform(0.5, 1.0), np.random.uniform(0.6, 1.0), 0, 0, 1])
        y.append("Title")
        
    # 2. Author (short, no punct)
    for _ in range(60):
        X.append([np.random.randint(1, 6), 0.0, np.random.uniform(0.8, 1.0), 0, 0, 1])
        y.append("Author")
        
    # 3. Heading 1 (short, bold, no punct)
    for _ in range(100):
        X.append([np.random.randint(1, 10), 1.0, np.random.uniform(0.5, 1.0), 0, 0, 1])
        y.append("Heading 1")
        
    # 3b. Heading 2 (short, bold/title case)
    for _ in range(80):
        X.append([np.random.randint(2, 8), 0.8, np.random.uniform(0.5, 1.0), 0, 0, 1])
        y.append("Heading 2")

    # 3c. Heading 3 (short, italic/bold)
    for _ in range(60):
        X.append([np.random.randint(2, 6), 0.5, np.random.uniform(0.4, 0.9), 0, 0, 1])
        y.append("Heading 3")
        
    # 4. Body Paragraph (medium/long, low bold, has punct, verbs, nouns)
    for _ in range(600):
        X.append([np.random.randint(8, 300), np.random.uniform(0, 0.1), np.random.uniform(0, 0.2), 1, 1, 1])
        y.append("Body Paragraph")
        
    # 5. Caption (short/medium, ends with punct)
    for _ in range(60):
        X.append([np.random.randint(5, 20), 0.0, 0.1, 1, 1, 1])
        y.append("Caption")
        
    # 6. List (short/medium, no punct at end necessarily)
    for _ in range(120):
        X.append([np.random.randint(3, 25), 0.0, 0.1, 0, 1, 1])
        y.append("List")
        
    # 7. References Heading (very short, bold)
    for _ in range(30):
        X.append([1, 1.0, 1.0, 0, 0, 1])
        y.append("References Heading")

    # 8. Code Block (medium, low title case, high verbs/nouns)
    for _ in range(50):
        X.append([np.random.randint(5, 40), 0.0, 0.0, 0, 1, 1])
        y.append("Code Block")

    # 9. Blockquote (long quotes)
    for _ in range(20):
        X.append([np.random.randint(40, 80), 0.0, 0.05, 1, 1, 1])
        y.append("Blockquote")

    X = np.array(X)
    y = np.array(y)
    
    print("[*] Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    model_path = os.path.join(os.path.dirname(__file__), 'classifier_model.pkl')
    print(f"[*] Saving model to {model_path}")
    with open(model_path, 'wb') as f:
        pickle.dump(clf, f)
        
    print("[*] Model trained and saved successfully.")

if __name__ == "__main__":
    train_dummy_model()
