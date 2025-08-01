import re
import os
def handle_comment_token(word, lineNumber, colNumber, in_comment, in_single_comment, comment_content, tokens,lineContent):
    if in_single_comment:
        comment_content += word + " "
        return in_comment, in_single_comment, comment_content, tokens, True,lineContent

    if in_comment:
        if word == "@/":
            tokens.append({f"{lineNumber},{colNumber-1},{comment_content.strip()},comment_content"})
            lineContent +="comment_content "
            tokens.append({f"{lineNumber},{colNumber},@/,comment_end"})
            lineContent+="comment_end "
            in_comment = False
        else:
            comment_content += word + " "
        return in_comment, in_single_comment, comment_content, tokens, True ,lineContent

    if word == "/^":
        tokens.append({f"{lineNumber},{colNumber},/^,comment_start"})
        lineContent += "comment_start "
        return in_comment, True, "", tokens, True,lineContent

    if word == "/@":
        tokens.append({f"{lineNumber},{colNumber},/@,comment_start"})
        lineContent +="comment_start "
        return True, in_single_comment, "", tokens, True ,lineContent

    return in_comment, in_single_comment, comment_content, tokens, False ,lineContent

def tokanize(filename):
    s = []
    l = []
    in_comment = False
    in_single_comment = False
    lineNumber = 1

    keyword_map = {
        "Stop": "Stop",
        "Imw": "Integer",
        "SIMw": "Signed_Integer",
        "Chj": "Character",
        "Series": "String",
        "IMwf": "Float",
        "SIMwf": "Signed_Float",
        "NOReturn": "Void",
        "IfTrue": "Condition",
        "Otherwise": "OtherCondition",
        "RepeatWhen": "Loop",
        "Reiterate": "Loop",
        "Turnback": "Return",
        "OutLoop": "Break",
        "Loli": "Struct",
        "Include": "Inclusion",
        "->": "Access Operator",
        "=": "Assignment",
        ";": "semiColon",
        ",": "comma"
    }

    patterns = [
        # (r'^[-+]?\d*\.?\d+$', "constant"),
        (r'==|!=|<=|>=|<|>', "Relational_Operator"),
        (r'[-+*/]', "Arithmetic_Operation"),
        (r'["\']', "Quotation Mark"),
        (r'[{}()]', "Braces"),
        (r'^[a-zA-Z_]\w*$', "Identifier"),
        (r'^[-+]?(?:\d+\.\d+|\d+)$', "constant"),
                (r"'(?:\\.|[^'\\])*'", "String_Literal")   # Match string literals with single quotes

    ]
    if os.path.exists(filename):
        with open(filename, 'r+') as myFile:
            comment_content = ""
            for line in myFile.readlines():
                lineContent = ""
                if in_single_comment:
                    s.append({f"{lineNumber-1},1,{comment_content.strip()},comment content"})
                    lineContent += "comment_content comment_end1"
                if not(lineContent == ""):
                    l.append(lineContent.strip())
                    lineContent = ""
                in_single_comment = False
                bo = re.match(r'\s*Include\s*\(\s*"[^"]+"\s*\)', line)
                if bo:
                    ms = re.search(r'"([^"]+)"', line)
                    if ms:
                        text = ms.group(1)
                        if os.path.exists(text):
                            b ,d = tokanize(text.strip())
                            s.append("")
                            for i in b:
                                s.append(i)
                            s.append("")
                            l.append("")
                            for i in d :
                                l.append(i)
                            l.append("")
                            continue
                # not working well but don't remove it
                # bo = re.match(r'\s*Include.*',line)
                # if bo:
                #     ms = re.search(r'\"[a-zA-Z_]+\d\.txt\"',line)
                #     ww = ms.span()
                #     text= line[ww[0]+1:ww[1]-1]
                #     b = tokanize(text)
                #     s.append("")
                #     for i in b:
                #         s.append(i)
                #     s.append("")
                #     continue
                words = re.findall(
                    r'==|!=|<=|>=|->|/\^|/@|@/|'            # special operators and comments
                    r'[-+*/=<>;(),{}]|'                     # single-char tokens
                    r'"[^"]*"|\'[^\']*\'|'                  # string literals
                    r'\b\d+(?:\.\d+)?\b|'                   # constants
                    r'\b[a-zA-Z_]\w*\b|'                    # valid identifiers
                    r'\d+[a-zA-Z_]\w*',                     # invalid identifiers starting with digits
                    line
                )
                
                colNumber = 1
                for word in words:
                    in_comment, in_single_comment, comment_content, s, handled ,lineContent = handle_comment_token(
                        word, lineNumber, colNumber, in_comment, in_single_comment, comment_content, s ,lineContent
                    )
                    if handled:
                        colNumber += 1
                        continue

                    token_type = None
                    if word in keyword_map:
                        token_type = keyword_map[word]
                    elif word =="(":
                        token_type ="("
                    elif word ==")":
                        token_type =")"
                    elif word =="{":
                        token_type ="{"
                    elif word =="}":
                        token_type ="}"
                    else:
                        for pattern, desc in patterns:
                            if re.fullmatch(pattern, word):
                                token_type = desc
                                break

                    if token_type:
                        s.append({f"{lineNumber},{colNumber},{word},{token_type}"})
                        lineContent += token_type+" "
                    else:
                        s.append({f"{lineNumber},{colNumber},{word},invalid-------------------------------"})
                        lineContent += "invalid "
                    
                    colNumber += 1
                lineNumber += 1
                l.append(lineContent.strip())

    return s ,l


