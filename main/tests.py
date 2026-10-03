from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Staf Komisi Disiplin",
            description="Mengatur dan mengawasi jalannya penegakan kedisiplinan.",
            category="volunteer",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Staf Komisi Disiplin")
        self.assertEqual(self.experience.category, "volunteer")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        self.assertFalse(self.experience.is_ongoing)


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Smoking Detector Arduino",
            description="Detektor asap rokok berbasis IoT menggunakan Arduino.",
            tech_stack="C++, Arduino, Sensors",
        )

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("main:show_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_page_renders_ajax_states_without_project_data(self):
        response = self.client.get(reverse("main:show_project"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Memuat proyek...")
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="grid"')
        self.assertNotContains(response, self.project.title)

    def test_projects_json_returns_data_and_star_state(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json(), [{
            "pk": str(self.project.pk),
            "fields": {
                "title": self.project.title,
                "description": self.project.description,
                "tech_stack": self.project.tech_stack,
                "repository_url": "",
                "project_image_url": "",
                "star_count": 0,
                "is_starred": False,
                "starred_by_names": "",
            },
        }])

    def test_projects_json_includes_logged_in_users_star(self):
        user = User.objects.create_user(username="star-user", password="test-password")
        self.project.starred_by.add(user)
        self.client.force_login(user)

        response = self.client.get(reverse("main:get_projects_json"))
        project_data = response.json()[0]["fields"]

        self.assertEqual(project_data["star_count"], 1)
        self.assertTrue(project_data["is_starred"])
        self.assertEqual(project_data["starred_by_names"], "star-user")

    def test_empty_projects_json_returns_empty_list(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])