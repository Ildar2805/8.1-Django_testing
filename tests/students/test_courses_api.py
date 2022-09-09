import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, student_factory, course_factory):
    students = student_factory(_quantity=1)
    courses = course_factory(_quantity=1, make_m2m=True)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_get_list_courses(client, student_factory, course_factory):
    students = student_factory(_quantity=5)
    courses = course_factory(_quantity=5, make_m2m=True)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(courses) == len(data)
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_id(client, student_factory, course_factory):
    students = student_factory(_quantity=5)
    courses = course_factory(_quantity=5, make_m2m=True)
    response = client.get('/api/v1/courses/?id=8')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == courses[1].name


@pytest.mark.django_db
def test_filter_name(client, student_factory, course_factory):
    students = student_factory(_quantity=5)
    courses = course_factory(_quantity=5, make_m2m=True)
    name = courses[0].name
    response = client.get(f'/api/v1/courses/?name={name}')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == name


@pytest.mark.django_db
def test_post_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'IT'})
    data = response.json()
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_course(client, student_factory, course_factory):
    students = student_factory(_quantity=1)
    courses = course_factory(_quantity=1, make_m2m=True)
    count = Course.objects.count()
    dt = {'name': 'IT'}
    response = client.patch('/api/v1/courses/18/', data=dt)
    data = response.json()
    assert response.status_code == 200
    assert Course.objects.count() == count
    assert data['name'] == dt['name']


@pytest.mark.django_db
def test_delete_course(client, student_factory, course_factory):
    students = student_factory(_quantity=1)
    courses = course_factory(_quantity=1, make_m2m=True)
    count = Course.objects.count()
    response = client.delete('/api/v1/courses/19/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1








