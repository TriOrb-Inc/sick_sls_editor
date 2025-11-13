"""Flask アプリの最小限の起動確認テスト。"""

from main import create_app


def test_index_returns_ok():
    """ルートパスにアクセスしたときに 200 が返ることを確認。"""
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
