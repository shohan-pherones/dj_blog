# DJ Blog: A Django-Based Blogging Platform

DJ Blog is a sleek and developer-friendly blogging platform built entirely with Django and styled using Tailwind CSS. It offers a straightforward yet powerful solution for developers to share knowledge, write tutorials, and showcase their projects in a clean and intuitive interface.

Designed with simplicity and functionality in mind, DJ Blog empowers users to focus on content creation without being bogged down by technical complexities. Whether you're sharing coding tips, documenting your latest project, or writing in-depth tutorials, DJ Blog provides all the essential tools to make your content stand out.

With a responsive, mobile-first design powered by Tailwind CSS, your blog will look great on any device. Django's robust backend ensures seamless performance, while its customizable features allow developers to tailor the platform to their unique needs.

Whether you're a seasoned developer looking for a personal blogging platform or a team building a community-driven knowledge hub, DJ Blog is the perfect starting point for creating engaging, developer-centric content.

## Installation

Clone the repository

```bash
git clone https://github.com/shohan-pherones/dj_blog
```

Navigate into the project directory

```bash
cd dj_blog
```

Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/Script/activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Create a .env file in the project root directory and define the following variables

```bash
DATABASE_NAME
```

Create and apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

Launch the application using

```bash
python manage.py runserver
```

Your application should now be running locally at `http://127.0.0.1:8000`

## Deployments

- **Front-End**: <https://djblog-2vnf.onrender.com>
- **Docker Image**: <https://hub.docker.com/r/spectrashohan/djblog>

## Feedback

If you have any feedback, please reach out to me at <shohan.sub.56@gmail.com>
