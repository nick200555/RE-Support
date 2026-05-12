from setuptools import setup, find_packages
with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")
setup(name="re_support", version="1.0.0", description="Real estate post-handover customer support application", author="Your Company Name", author_email="user@example.com", packages=find_packages(), zip_safe=False, include_package_data=True, install_requires=install_requires)
