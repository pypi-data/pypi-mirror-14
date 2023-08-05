# napper

A REST framework for asyncio.

Currently in experimental stage. Use at your own risk.

.. code:: python

    import asyncio

    from napper import apis

    async def getstargazers():
        """Print the most popular repository of the authors of
        the most recent gists from github."""
        with apis.github() as github:
            gists = github.gists.get()
            async for gist in gists:
                try:
                    repo = await gist.owner.repos_url.get()[0]
                except AttributeError:
                    print("{0.id}: Gist has no owner".format(gist))
                    continue
                except IndexError:
                    print("{0.id}: {0.owner.login} has no repositories".format(gist))
                    continue
                print("{0.id}: {0.owner.login} {1.name} {1.stargazers_count}".format(
                    gist, repo
                    ))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(getstargazers())
