from typing import Final

from locust import FastHttpUser, task


class Library(FastHttpUser):
    url: Final[str] = '/v1/library/books'

    @task
    def add_books(self) -> None:
        with self.rest(
            'POST',
            self.url,
            json={
                'name': 'name',
                'author': 'author',
                'published_at': '2000-01-01',
                'genre': 'Fantasy',
                'url': 'http://qwer.ty',
            },
        ) as resp:
            assert resp.js['uid']

    @task
    def get_books(self) -> None:
        with self.rest('GET', self.url) as resp:
            assert resp.js['items']
