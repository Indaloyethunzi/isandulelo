#!/usr/bin/env python
"""
Setup script for Isandulelo development environment.
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Isandulelo development environment...\n")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: You don't appear to be in a virtual environment.")
        print("   It's recommended to create one first with: python -m venv venv")
        print("   Then activate it and run this script again.\n")
        
        choice = input("Continue anyway? (y/n): ").lower()
        if choice != 'y':
            print("Exiting setup. Please create a virtual environment first.")
            return False
    
    # Install Python dependencies
    if not run_command("pip install -r requirements/development.txt", "Installing Python dependencies"):
        return False
    
    # Change to Django project directory
    django_dir = Path(__file__).parent.parent / "isandulelo"
    os.chdir(django_dir)
    
    # Run Django migrations
    if not run_command("python manage.py migrate", "Running Django migrations"):
        return False
    
    # Create superuser (interactive)
    print("\n📝 Creating Django superuser...")
    print("You'll be prompted to create an admin user for the Django admin interface.")
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, check=True)
        print("✅ Superuser created successfully")
    except subprocess.CalledProcessError:
        print("❌ Superuser creation failed or was cancelled")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    # Create .env file if it doesn't exist
    env_file = django_dir / ".env"
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Isandulelo Environment Configuration
DJANGO_ENVIRONMENT=development
SECRET_KEY=django-insecure-replace-this-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Optional: Set these for production
# POSTGRES_DB=isandulelo
# POSTGRES_USER=isandulelo
# POSTGRES_PASSWORD=your-password
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Navigate to the Django directory: cd isandulelo")
    print("2. Start the development server: python manage.py runserver")
    print("3. Visit http://127.0.0.1:8000/admin/ to access the admin interface")
    print("4. Visit http://127.0.0.1:8000/api/ to explore the API")
    print("\n🔧 Development commands:")
    print("  python manage.py runserver     - Start development server")
    print("  python manage.py shell         - Open Django shell")
    print("  python manage.py test          - Run tests")
    print("  python manage.py makemigrations - Create new migrations")
    print("  python manage.py migrate       - Apply migrations")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        sys.exit(1)