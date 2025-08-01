import re

var_types = ["Integer", "Signed_Integer", "Character", "String", "Float", "Signed_Float", "Void"]
types_pattern = '|'.join(re.escape(t) for t in var_types)
parameter = rf'(?:{types_pattern})\s+Identifier'
params = rf'(?:Void|{parameter}(?:\s+comma\s+{parameter})*)?'

# parameter = r'(?:' + types_pattern + r')\s+Identifier)'
fun_parameter = (r'(?:Void|'+parameter+'?')

basic_factor = r'(Identifier|constant)'
operator = r'(Relational_Operator|Arithmetic_Operation)'
grouped_expression = rf'\(\s*{basic_factor}(\s+{operator}\s+{basic_factor})*\s*\)'
factor = rf'({basic_factor}|{grouped_expression})'

term = rf'{factor}'
additive_expression = term
semi_colon = r'semiColon'
simple_expression = rf'{additive_expression}(\s+{operator}\s+{additive_expression})*'
expression = rf'((Identifier\s+Assignment\s+)+({simple_expression})|({simple_expression}))'

brackets = r'( \{\s*\}?\s*)?'
l = []
# def param(specifier,id):
#     if(specifier in var_types and id == "Identifier"):
#         return True
#     return False

def parse(tokens_type):
    Error_num = 0
    i = 0
    while i < len(tokens_type):
        line = tokens_type[i]
        words = line.split(' ')
        declare = ' '.join(words[1:])
        # Expression
        if re.fullmatch(expression+rf' {semi_colon}', line):
                l.append(f"line {i+1}: correct expression end with semi_colon")
        
        # var-declaration | fun-declaration
        elif(words[0] in var_types):
            # (?: Assignment (?:Identifier|constant))? 
            if re.fullmatch(r'Identifier semiColon', declare):
                l.append(f"line {i+1}: variable Declaraion")
            elif re.fullmatch(r'Identifier \( (Void)?\s*\) (\{\s*\}?\s*)?', declare):
                l.append(f"line {i+1}: function declare")
            elif re.fullmatch(r'Identifier \( '+params+r'\s*\)'+brackets, declare):
                l.append(f"line {i+1}: function declare (with params)")
            else: 
                l.append(f"line {i+1}: error in declaration")
                l.append(line)

        # comments
        elif "comment_start" in line:
            if i + 1 < len(tokens_type):
                while True:
                    next_line = tokens_type[i + 1]
                    if "comment_end" in line:
                        l.append(f"line {i+1}: comment")
                        break
                    elif "comment_end" in next_line:
                        l.append(f"line {i+1}: comment")
                        i += 1
                        break
                    else: i+=1

        # loop not much
        elif re.fullmatch(r'Loop \( '+expression+r' \)'+brackets,line) or re.fullmatch(r'Loop\s*\(\s*'+expression+r'\s+semiColon\s+'+expression+r'\s+semiColon\s+'+expression+r'\s*\)\s*'+brackets,line):
            l.append(f"line {i+1}: loop")
        
        elif line == "}":
            l.append(f"line {i+1}: "+ "}")
        #if 
        # elif 
        elif re.fullmatch(r'Condition \( '+expression+r' \)'+brackets,line) or re.fullmatch(r"OtherCondition "+expression,line):
            l.append(f"line {i+1}: Condition")
        elif line=="Stop semiColon" or re.fullmatch(r'Return '+expression+rf' {semi_colon}',line):
            l.append(f"line {i+1}: Jump_stmt")
        else:
            l.append(f"line {i+1}: Doesn't match: " + line)
            Error_num += 1

        
        i += 1
    l.append("\n Num Of Errors in parser: "+str(Error_num) )
    return l