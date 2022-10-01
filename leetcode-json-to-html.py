import glob
import json
import pandas as pd

fields = ['questionId', 'questionFrontendId', 'content', 'title', 'titleSlug', 'isPaidOnly', 'difficulty', 'likes', 'dislikes']

dfs = []

for filename in glob.glob('./json/LC*.json'):
    with open(filename, 'r') as f:
        question = json.load(f)
    main = question['data']['question']
    dfs.append(pd.DataFrame({f:main[f] for f in fields}, index=[int(main['questionFrontendId'])]))

select_df = pd.concat(dfs).sort_index()


# problem filter
select_df['score'] = select_df['likes'] - select_df['dislikes']
select_df = select_df.sort_values(by='score', ascending=False)
select_df = select_df[:700].sort_index()


out = ""
for i, (_, problem) in enumerate(select_df.iterrows()):
    pid, title, difficulty, l, d = problem['questionFrontendId'], problem['title'], problem['difficulty'], problem['likes'], problem['dislikes']
    problem_title_html = f'<h2>{pid}. {title} - {difficulty} {l}/{d}</h2>'
    out += problem_title_html
    out += problem['content']

with open("all.html", "wb") as f:
    f.write(out.encode(encoding="utf-8"))

#pandoc --standalone all.html --output index.tex