from feedparser import parse

feed = parse("https://blog.mannu.me/rss/").entries
latest = [f"""- [{feed[i].title}]({feed[i].link})  \n{feed[i].description} - {feed[i].published}"""for i in range(3)]
farr = []
with open("README.md", "r", encoding='utf8') as x:
    for line in x:
        if line.strip() == "<!--bp-->":
            break
        farr.append(line)

with open("README.md", "w", encoding='utf8') as x:
    x.writelines(farr)
    x.write("<!--bp-->\n\n")
    li = [x.write(i + "\n\n") for i in latest]
