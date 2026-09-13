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
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
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

    def test_project_data_appears(self):
        response = self.client.get(reverse("main:show_project"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")