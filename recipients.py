import csv

def load_recipients(file_path):
    recipients = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipients.append({
                'name': row['name'],
                'email': row['email']
            })
    return recipients

def save_recipients(file_path, recipients):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'email'])
        writer.writeheader()
        writer.writerows(recipients) 