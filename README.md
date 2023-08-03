# A web based medical care app developed with Django



# <span style="color:cornflowerblue">OncoConnect</span>

A Web-based medical care app developed with Django

## Setup Instructions

### Prerequisites
- Clone the repository to your local machine.
- Make sure Docker is installed on your system.

### Step 1: Run Docker Compose for the Web Container
```bash
docker-compose up web -d
```

### Step 2: Wait for the Database to Be Ready
After running the previous command, it's essential to wait for at least 1 minute to allow the database to be ready.

### Step 3: Run Docker Compose for the Nginx Container
```bash
docker-compose up nginx -d
```

### Step 4: Collect Static Files
```bashh
docker-compose exec web python manage.py collectstatic
```

### Step 5: Perform Database Migrations
```bash
docker-compose exec web python manage.py migrate
```

Congratulations! The web-based medical care app should now be up and running.

Remember to visit the app on your browser using *http://localhost:80*

If you encounter any issues during setup or usage, please refer to the documentation or raise an issue on the repository.
