        text = base64.b64decode(file_content).decode('utf-8')
        with open(f'check/{filename}','w') as f:
            f.write(text)
        print(text)