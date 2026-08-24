import re
import os
import pickle
import numpy as np

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except (ImportError, OSError):
    nlp = None
    print("[!] spaCy en_core_web_sm not loaded. Using fallback NLP features.")

try:
    import nltk
except ImportError:
    nltk = None

class ParagraphClassifier:
    def __init__(self):
        self.paragraph_count = 0
        self.model = None
        
        model_path = os.path.join(os.path.dirname(__file__), 'classifier_model.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            print("[*] Successfully loaded Offline ML Classifier (RandomForest).")
        else:
            print("[!] ML model not found. Using heuristic fallback.")

    def is_title_case(self, text):
        words = text.split()
        if not words: return 0.0
        capitalized = sum(1 for w in words if w[0].isupper() or w[0].isdigit())
        return capitalized / len(words)

    def has_person_entity(self, text):
        if not nltk:
            return False
        try:
            tokens = nltk.word_tokenize(text)
            tags = nltk.pos_tag(tokens)
            tree = nltk.ne_chunk(tags, binary=False)
            for subtree in tree.subtrees():
                if type(subtree) == nltk.Tree and subtree.label() == 'PERSON':
                    return True
        except Exception:
            pass
        return False

    def extract_features(self, text, is_bold):
        word_count = len(text.split())
        bold_ratio = 1.0 if is_bold else 0.0
        title_case_ratio = self.is_title_case(text)
        ends_with_punct = 1 if text and text[-1] in '.?!:"\'' else 0
        
        has_verb = 0
        has_noun = 0
        
        if nlp:
            doc = nlp(text)
            for token in doc:
                if token.pos_ == "VERB": has_verb = 1
                if token.pos_ in ["NOUN", "PROPN"]: has_noun = 1
        else:
            # Fallback if spacy is missing
            has_verb = 1 if word_count > 3 else 0
            has_noun = 1 if word_count > 1 else 0
            
        return [word_count, bold_ratio, title_case_ratio, ends_with_punct, has_verb, has_noun]

    def classify(self, element):
        """
        Returns a tuple: (classification_string, confidence_float, review_needed_bool)
        """
        cls_str, conf, review_needed, _ = self.classify_with_explanation(element)
        return cls_str, conf, review_needed

    def classify_with_explanation(self, element):
        """
        Returns a tuple: (classification_string, confidence_float, review_needed_bool, explanation_string)
        """
        text = element['text']
        is_bold = element.get('is_bold', False)
        is_monospace = element.get('is_monospace', False)
        is_indented = element.get('is_indented', False)
        self.paragraph_count += 1
        
        lower_text = text.lower()
        word_count = len(text.split())
        
        # -1. Code Block Rule
        if is_monospace or text.startswith("def ") or text.startswith("class ") or text.startswith("import ") or (text.startswith("```") and text.endswith("```")):
            return "Code Block", 0.95, False, "Matched Code syntax or monospace font"

        # -0.5. Blockquote Rule
        if is_indented or (text.startswith('"') and text.endswith('"') and word_count > 15):
            return "Blockquote", 0.85, False, "Matched blockquote indentation or long quote"

        # 0. NLTK NER Hard Rule for Author
        if self.paragraph_count <= 6 and word_count < 10 and self.has_person_entity(text):
            return "Author", 0.95, False, "Hard Rule: Detected Named Person entity near title"

        # 1. Hard Rule: References Heading
        if lower_text in ["references", "bibliography", "works cited"]:
            return "References Heading", 1.0, False, "Hard Rule: Matched reference section keyword"
            
        # 2. Hard Rule: Caption
        if re.match(r'^(figure|fig\.|table)\s*\d+', lower_text):
            return "Caption", 0.90, False, "Hard Rule: Matched Figure/Table caption pattern"
            
        # 2.5 Subheading 2 / 3 Rules
        if re.match(r'^\d+\.\d+\.\d+', text):
            return "Heading 3", 0.95, False, "Matched sub-sub-section numbering pattern (X.Y.Z)"
        elif re.match(r'^\d+\.\d+', text):
            return "Heading 2", 0.95, False, "Matched sub-section numbering pattern (X.Y)"

        # 3. ML Classification
        if self.model:
            features = self.extract_features(text, is_bold)
            prediction = self.model.predict([features])[0]
            
            probabilities = self.model.predict_proba([features])[0]
            confidence = float(max(probabilities))
            
            # Post-processing tweaks (Hybrid approach)
            if prediction == "Title" and self.paragraph_count > 5:
                prediction = "Heading 1"
                confidence = 0.50 # Forcing review if overridden manually
                return prediction, confidence, True, "ML predicted Title post 5th paragraph; overridden to Heading 1"
                
            review_needed = confidence < 0.60
            exp = f"ML Model prediction (Confidence: {confidence*100:.1f}%)"
            return prediction, confidence, review_needed, exp
            
        else:
            # Fallback heuristics
            if re.match(r'^[\*\-\+•]\s', text) or (re.match(r'^\d+\.\s+[A-Z]', text) and word_count > 3):
                if not is_bold and word_count > 5:
                    return "List", 0.8, False, "Heuristic: List bullet/number pattern"
            if self.paragraph_count <= 3 and word_count < 20 and (self.is_title_case(text) > 0.5 or text.isupper() or is_bold):
                return "Title", 0.8, False, "Heuristic: Early title case text"
            if self.paragraph_count <= 6 and word_count < 10 and not re.match(r'^\d', text):
                return "Author", 0.8, False, "Heuristic: Early short author line"
            if word_count < 15 and (self.is_title_case(text) > 0.5 or text.isupper() or is_bold):
                if re.match(r'^(chapter\s*\d+|\d+\.)', lower_text) or (word_count < 8 and text.isupper()):
                    return "Heading 1", 0.9, False, "Heuristic: Chapter/heading pattern"
                if re.match(r'^\d+\.\d+', text):
                    return "Heading 2", 0.9, False, "Heuristic: Subheading numbering pattern"
                if is_bold or self.is_title_case(text) > 0.5:
                    return "Heading 1", 0.7, False, "Heuristic: Short bold title-cased heading"
            return "Body Paragraph", 0.9, False, "Default fallback classification"

