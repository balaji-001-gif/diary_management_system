from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="dairy_management",
    version="1.0.0",
    description="Dairy Management System (DMS) — Complete dairy value chain on Frappe/ERPNext v15+",
    author="Antigravity",
    author_email="admin@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
