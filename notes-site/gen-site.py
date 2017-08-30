import os, shutil
from urllib.request import unquote

content_path = "content/"
notes_path = "../Notes/"

try:
    shutil.rmtree(os.path.join(content_path, 'Year 1'))
except Exception as e:
    print(e)


def process(path):
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        new_file_path = os.path.join(content_path, file_path[len(notes_path):])
        new_file_root = os.path.join(content_path, path[len(notes_path):])
        try:
            if os.path.isfile(file_path):
                if f.endswith('.ipynb'):
                    # Generate page for notebook
                    command = "jupyter nbconvert --to markdown --execute --output-dir '" + new_file_root + "' '" + file_path + "'"
                    os.system(command)
                    
                    md_path = new_file_path[:-len('.ipynb')] + ".md"
                    with open(md_path, 'r+') as md_file:
                        # Append title to page
                        content = md_file.read()
                        md_file.seek(0, 0)
                        md_file.truncate()
                        md_file.write("---\n")
                        md_file.write("title: \"" + f[:-len(".ipynb")] + "\"\n")
                        md_file.write("---\n")
                        md_file.write(content)

                    with open(md_path, 'r+') as md_file:
                        # Embed svg's
                        content = md_file.read()
                        # print(content)
                        while True:
                            index = content.find("![svg](")
                            if index == -1: break
                            print("\n\n\n\nCUTTING SVG\n\n\n\n")
                            end = index
                            while content[end] != ")": end += 1
                            
                            # Extract and transform svg path
                            svg_path = content[index + len("![svg](") : end]
                            svg_path = unquote(svg_path)
                            svg_path = os.path.join(new_file_root, svg_path)
                            
                            # Replace svg path in file
                            content = content[:index] + "{{< svg \"" + svg_path + "\" >}}" + content[end+1:]
                        
                        md_file.seek(0, 0)
                        md_file.truncate()
                        md_file.write(content)
                else:
                    # Copy resource file
                    shutil.copyfile(file_path, new_file_path)

            elif os.path.isdir(file_path):
                # Create folder
                os.makedirs(new_file_path)
                
                # Create _index.md file
                with open(os.path.join(new_file_path, "_index.md"), "w+") as index_file:
                    index_file.write("---\n")
                    index_file.write("title: \"" + f + "\"\n")
                    index_file.write("---\n")

                # Process subdirectorys
                process(file_path)
        except Exception as e:
            print(e)

process(notes_path)