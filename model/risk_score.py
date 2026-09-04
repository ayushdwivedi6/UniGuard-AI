def calculate_risk(threat, confidence):

    if threat == "BENIGN":
        return min(int((100 - confidence) * 0.5), 30)

    if threat == "PortScan":
        return min(int(60 + confidence * 0.3), 85)

    if threat == "DDoS":
        return min(int(70 + confidence * 0.3), 100)

    return int(confidence)


def get_severity(risk):

    if risk <= 30:
        return "LOW"

    elif risk <= 60:
        return "MEDIUM"

    elif risk <= 80:
        return "HIGH"

    else:
        return "CRITICAL"
    