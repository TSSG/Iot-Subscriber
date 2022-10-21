from utils import validate

def store_data(data):
    valid_pload = validate.validate_data(data)

    summary = {}
    # report = store_data(valid_pload)
    # summary.append(report)
    
    summary['body'] = "POST successful."

    return summary