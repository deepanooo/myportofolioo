from django.forms import DateInput, ModelForm, TextInput, Textarea, URLInput

from main.models import Experience, Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "repository_url",
            "project_image_url",
        ]
        labels = {
            "title": "Nama proyek",
            "description": "Deskripsi proyek",
            "tech_stack": "Teknologi yang digunakan",
            "repository_url": "URL proyek",
            "project_image_url": "URL gambar proyek",
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "category", "description", "started_at", "ended_at"]
        labels = {
            "title": "Posisi atau pengalaman",
            "category": "Kategori",
            "description": "Deskripsi",
            "started_at": "Tanggal mulai",
            "ended_at": "Tanggal selesai",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Contoh: UI/UX Designer"}),
            "category": TextInput(attrs={"placeholder": "Contoh: Organization, Internship"}),
            "description": Textarea(attrs={"placeholder": "Ceritakan kontribusi atau pengalamanmu", "rows": 4}),
            "started_at": DateInput(attrs={"type": "date"}),
            "ended_at": DateInput(attrs={"type": "date"}),
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Ceritakan proyekmu", "rows": 4}),
            "tech_stack": TextInput(attrs={"placeholder": "Django, Python, HTML, CSS"}),
            "repository_url": URLInput(attrs={"placeholder": "https://github.com/username/project"}),
            "project_image_url": URLInput(attrs={"placeholder": "https://example.com/gambar-proyek.jpg"}),
        }
