import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asm_backend.settings")
django.setup()

from post_office.models import EmailTemplate

def upload_templates(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                content = f.read()
                template_name = os.path.splitext(filename)[0]
                # Save or update the template in the database
                email_template, created = EmailTemplate.objects.update_or_create(
                    name=template_name, 
                    defaults={'subject': template_name, 'html_content': content}
                )
                if created:
                    print(f"Template '{template_name}' created successfully.")
                else:
                    print(f"Template '{template_name}' updated successfully.")

    


# upload_asset_status()
# upload_templates('templates')


from django.apps import apps

excluded_apps = ['auth', 'contenttypes', 'admin', 'sessions', 'django_celery_results', 'django_celery_beat', 'post_office']

local_apps = []
for model in apps.get_models():
    if model._meta.app_label not in excluded_apps:
        local_apps.append(model)
        print(f"{model._meta.app_label}.{model.__name__}")

print(local_apps)

