import os
import io

# Set directory path
directory = r'C:\\Users\\HP1\Desktop\\!!Vulnerability_Exploitability_test\\reference_commit\\commit_'

# Traverse all txt files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        # Read file content and replace newline characters with escape sequence
        with io.open(os.path.join(directory, filename), 'r', encoding='utf-8') as infile:
            content = infile.read().replace('\n', '\\n')

        # Skip txt files with more than 65510 characters
        if len(content) >= 65510:
            continue
        if content.find('diff') == -1:
            os.remove(os.path.join(directory, filename)) # Remove files without 'diff'
