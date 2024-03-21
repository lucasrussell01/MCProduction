def format_status(status):
    if status == 'done':
        return "$${\\color{green}\\textbf{DONE}}$$"
        # return '<span style="color:green">Done</span>'
    elif status == 'submitted':
        return "$${\\color{orange}\\textbf{SUBMITTED}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif status == 'new':
        return "$${\\color{orange}\\textbf{NEW}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif status == 'validation':
        return "$${\\color{blue}\\textbf{VALIDATION}}$$"
        # return '<span style="color:blue">Validation</span>'
    elif status == "N/A":
        return "$${\\color{red}\\textbf{MISSING}}$$"
    elif status == "INV":
        return "$${\\color{red}\\textbf{INVALID}}$$"
        # return '<span style="color:red; font-weight:bold">MISSING</span>'
    else:
        return status