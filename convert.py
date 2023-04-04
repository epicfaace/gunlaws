import json
with open("output.json", "r") as f:
    data = json.load(f)

def convert_to_html(data):
    html = '<table border="1">\n'
    html += '<tr><th>Title</th><th>Subjects</th><th>Jurisdictions</th><th>Year</th><th>Text</th></tr>\n'
    for item in data:
        html += '<tr>\n'
        html += f'<td><a href="{item["url"]}">{item["title"]}</a></td>\n'
        html += f'<td>{"<br>".join(item["subjects"])}</td>\n'
        html += f'<td>{"<br>".join(item["jurisdictions"])}</td>\n'
        html += f'<td>{item["year"]}</td>\n'
        txt = "\n".join(item["text"])
        html += f'<td>{txt}</td>\n'
        html += '</tr>\n'
    html += '</table>'
    return html

html_output = convert_to_html(data)

with open("output.html", "w+") as f:
    f.write(html_output)