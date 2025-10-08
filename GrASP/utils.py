def format_status(status):
    if status == 'done' + " (WARNING)":
        return "$${\\color{green}\\textbf{DONE}}$$ $${\\color{red}\\textbf{(WARNING)}}$$"
        # return '<span style="color:green">Done</span>'
    elif 'done' in status:
        return "$${\\color{green}\\textbf{DONE}}$$"
        # return '<span style="color:green">Done</span>'
    elif 'submitted' in status:
        return "$${\\color{blue}\\textbf{SUBMITTED}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif 'new' in status:
        return "$${\\color{orange}\\textbf{NEW}}$$"
        # return '<span style="color:orange">Submitted</span>'
    elif 'validation' in status:
        return "$${\\color{orange}\\textbf{VALIDATION}}$$"
        # return '<span style="color:blue">Validation</span>'
    elif 'defined' in status:
        return "$${\\color{orange}\\textbf{DEFINED}}$$"
        # return '<span style="color:blue">Validation</span>'
    elif 'N/A' in status:
        return "$${\\color{red}\\textbf{MISSING}}$$"
    elif 'INV' in status:
        return "$${\\color{red}\\textbf{INVALID}}$$"
        # return '<span style="color:red; font-weight:bold">MISSING</span>'
    else:
        return status