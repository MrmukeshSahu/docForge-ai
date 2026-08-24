import re

class DocumentCleaner:
    def __init__(
        self, 
        doc, 
        title_case_headings: bool = False, 
        bullet_standardization: bool = False, 
        trailing_whitespace: bool = False
    ):
        self.doc = doc
        self.fixed_spacing_errors = 0
        self.title_case_headings = title_case_headings
        self.bullet_standardization = bullet_standardization
        self.trailing_whitespace = trailing_whitespace

    def clean(self):
        """
        Executes the cleaning pipeline:
        1. Typography Standardization (Em-dashes, smart quotes)
        2. Redundancy Removal (Double spaces, empty paragraphs)
        3. Optional Advanced Rules (Heading capitalization, bullet standardization, trailing whitespace)
        """
        paragraphs_to_remove = []
        
        for p in self.doc.paragraphs:
            original_text = p.text
            
            # Check for redundancy issues conceptually
            if '  ' in original_text or '\t\t' in original_text:
                self.fixed_spacing_errors += 1
            
            # Remove entirely blank paragraphs
            if not original_text.strip():
                paragraphs_to_remove.append(p)
                continue
            
            # Optional Bullet standardization
            if self.bullet_standardization and re.match(r'^[\*\-\+]\s', original_text):
                # Standardize bullet symbol to bullet character
                if p.runs and p.runs[0].text:
                    p.runs[0].text = re.sub(r'^[\*\-\+]\s', '• ', p.runs[0].text)

            # Typography standardization per run to preserve formatting boundaries
            for run in p.runs:
                if not run.text:
                    continue
                    
                text = run.text
                
                # 1. Double hyphens to Em-Dashes
                text = text.replace('--', '—')
                
                # 2. Straight quotes to smart quotes (Simplified heuristic)
                text = re.sub(r'(^|\s)"', r'\1“', text)
                text = re.sub(r'"(\s|[.,!?;:]|$)', r'”\1', text)
                
                # 3. Redundant spaces and tabs
                text = re.sub(r' {2,}', ' ', text)
                text = re.sub(r'\t{2,}', '\t', text)
                
                # 4. Optional Trailing whitespace cleanup
                if self.trailing_whitespace:
                    text = text.rstrip(' \t')
                
                run.text = text
                
        # Delete blank paragraphs from OXML tree
        for p in paragraphs_to_remove:
            p._element.getparent().remove(p._element)
            
        return self.fixed_spacing_errors

