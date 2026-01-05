from fastapi.testclient import TestClient
from backend.main import app
from backend.schemas import CategoryChoices, DifficultyChoices

client = TestClient(app)

def test_get_root_response():
    response = client.get("/")
    url = "https://trivial.pub"
    expected_response = {
        "api_name": "trivial.pub API",
        "version": "1.0",
        "documentation_url": f"{url}/docs",
        "endpoints": {
            "questions": f"{url}/questions",
            "answers": f"{url}/answers",
            "users": f"{url}/users"
        }
    }
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_questions_random_args_none():
    rand_question_1 = client.get("/questions/random")
    assert rand_question_1.status_code == 200
    rand_question_2 = client.get("/questions/random")
    assert rand_question_2.status_code == 200
    assert rand_question_1.json() != rand_question_2.json()  # 1% chance repeat question

def test_get_questions_random_args_category():
    for category in CategoryChoices:
        query_params = {"category": category.value}
        response = client.get("/questions/random", params=query_params)
        assert response.status_code == 200
        assert response.json()["category"] == query_params["category"]

def test_get_questions_random_args_difficulty():
    for difficulty in DifficultyChoices:
        query_params = {"difficulty": difficulty.value}
        response = client.get("/questions/random", params=query_params)
        assert response.status_code == 200
        assert response.json()["difficulty"] == query_params["difficulty"]

def test_get_questions_random_args_category_and_difficulty():
    for category in CategoryChoices:
        for difficulty in DifficultyChoices:
            query_params = {"category": category.value, "difficulty": difficulty.value}
            response = client.get("/questions/random", params=query_params)
            assert response.status_code == 200
            assert response.json()["category"] == query_params["category"]
            assert response.json()["difficulty"] == query_params["difficulty"]

