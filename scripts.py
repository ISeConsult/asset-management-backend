import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asm_backend.settings")
django.setup()

from post_office.models import EmailTemplate
from apps.assets.models import AssetStatus

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



def upload_asset_status():
    status = ['pending','in_repair','checked_in','checked_out']

    for stat in status:
        AssetStatus.objects.create(name=stat)
        print(f"{stat} created")

    


upload_asset_status()
# upload_templates('templates')

