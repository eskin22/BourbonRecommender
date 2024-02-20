import json

def get_credentials():
    with open('src/data/credentials/.auth.json', 'r') as creds_file:
        creds = json.load(creds_file)
        return creds
        
if __name__ == '__main__':
    print(get_credentials())