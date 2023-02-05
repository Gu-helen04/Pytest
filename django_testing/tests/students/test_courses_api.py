import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course,*args, **kwargs )
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student,*args, **kwargs )
    return factory

# проверка получения 1го курса
@pytest.mark.django_db
def test_courses_first(client, courses_factory):
    courses_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse('courses-detail', args=(course_first.id, ))

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == course_first.id
    assert response.data['name'] == course_first.name

# проверка получения списка курсов
@pytest.mark.django_db
def test_courses_list(client, courses_factory):
    courses = courses_factory(_quantity=5)
    url = reverse('courses-list')

    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == len(courses)

# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_id(client, courses_factory):
    courses_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse('courses-list') + f'?id={course_first.id}'

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    for course_ in data:
        assert course_['id'] == course_first.id
        assert course_['name'] == course_first.name

# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name(client, courses_factory):
    courses_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse('courses-list') + f'?name={course_first.name}'

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    for course_ in data:
        assert course_['id'] == course_first.id
        assert course_['name'] == course_first.name

# тест успешного создания курса
@pytest.mark.django_db
def test_course_creation(client):
    url = reverse('courses-list')

    response = client.post(url, data={'name':'DJ-54', 'students':[]})

    assert response.status_code == 201

# тест успешного обновления курса
@pytest.mark.django_db
def test_course_update(client, courses_factory):
    courses_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse('courses-detail', args=(course_first.id,))

    response = client.patch(path=url, data={'name':'Test_Course'})

    assert response.status_code == 200

# тест успешного удаления курса
@pytest.mark.django_db
def test_deleting_a_course(client, courses_factory):
    courses_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse('courses-detail', args=(course_first.id,))

    response = client.delete(url)

    assert response.status_code == 204


