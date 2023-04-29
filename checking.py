import requests
import os
import base64
import time

start_time = time.time()

# your code here

url = "https://api.github.com/repos/sankalpa-acharya/karya/git/trees/71cb688eb68831d09c9c4508b2e90ebd0704dab9?recursive=1"
pat = ""
headers = {'Authorization': f'token {pat}'}
response = requests.get(url, headers=headers)
json_response = response.json()  # use response.json() to parse the response as JSON
total_lines = 0
for item in json_response['tree']:
    if total_lines==20:
        break
    if item['type'] == 'blob' and item['path'].endswith(('.py','.html','.css')):  # filter for Python source files
        file_url = item['url']
        filename = os.path.basename(item['path'])
        file_response = requests.get(file_url,headers=headers)
        file_content = file_response.json().get('content')
        text = base64.b64decode(file_content).decode('utf-8')
        with open(f'check/{filename}','w') as f:
            total_lines += 1
            f.write(text)

end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
print("total files-> ",total_lines)