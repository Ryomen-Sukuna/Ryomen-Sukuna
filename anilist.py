
import httpx
import re
import trio
import ujson

query = """
query($query: String){
    User(name: $query){
        favourites{
            anime {
                nodes{
                    siteUrl
                    title {
                        romaji
                    }
                }
            }
        }
    }
}
"""


async def array(username: str) -> str:
    async with httpx.AsyncClient() as ses:
        return (
            (
                await ses.post(
                    url='https://graphql.anilist.co',
                    data=ujson.dumps(
                        {
                            'query': query,
                            'variables': {
                                "query": username
                            }
                        }
                    ),
                    headers={
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                )
            ).json()
        )['data']['User']['favourites']['anime']['nodes']


async def main(username: str) -> str:
    r =  await array(username)
    new = '<!-- anilist_start-->\n'
    for x in r:
        new += ' • <a href="{}">{}<a><br>\n'.format(x['siteUrl'], x['title']['romaji'])
    new += "<!-- anilist_end-->"
    async with await trio.open_file("README.md", "r", encoding="utf8") as x:
        text = re.compile(
            "<!-- anilist_start-->.*<!-- anilist_end-->",
            re.DOTALL
        ).sub(new, await x.read())
    async with await trio.open_file("README.md", "w", encoding="utf8") as x:
        await x.write(text)


if __name__ == "__main__":
    trio.run(main, 'pokurt')