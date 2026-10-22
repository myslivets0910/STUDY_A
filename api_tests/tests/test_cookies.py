

class TestCookies:
    """ПРоверка автоматической работы requests.Session с cookies"""

    def test_post_sends_cookie_automatically(self, echo_client):
        """Получение куки"""
        set_response = echo_client.set_cookie("qa_session", "test-123")
        assert set_response.status_code == 200


        # отладка 1
        # print(f"куки после set cookie: {dict(echo_client.session.cookies)}")
        # print(f"урл последнего запроса: {set_response.url}")
        # print(f"статус: {set_response.status_code}")


        response = echo_client.post_echo({"qa_session": "test-123"})
        assert response.status_code == 200

        # Отладка 2
        # print(f"Ответ пост:{response.json()}")


        echoed = response.json()["headers"]
        headers = {
            key.lower(): value
            for key, value in echoed.items()
        }

        cookies_header = headers.get('cookie', "Отсутствует")

        # Отладка 3
        # print(f"\nЗаголовки в эхо-ответе: {headers}")
        # print(f"Cookie заголовок: {headers.get('cookie', 'ОТСУТСТВУЕТ')}")
        # assert "qa_session=test-123" in headers.get("cookie", "")

        assert "name=qa_session" in cookies_header
        assert "value=test-123" in cookies_header


    def test_cookie_persist_across_requests(self, echo_client):
        "Куки живет в сессии"
        echo_client.set_cookie("qa_session", "test-123")

        first = echo_client.get_cookie().json()["cookies"]
        second = echo_client.get_cookie().json()["cookies"]

        assert first.get("name") == "qa_session"
        assert second.get("value") == "test-123"



    def test_new_session_does_not_inherit_cookies(self, echo_client, isolated_echo_client):
        "Куки не сохраняются между сессиями"
        echo_client.set_cookie("qa_session", "test-123")

        assert echo_client.get_cookie().json()["cookies"].get("value") == "test-123"

        isolated_cookies = isolated_echo_client.get_cookie().json()["cookies"]
        assert "qa_session" not in isolated_cookies