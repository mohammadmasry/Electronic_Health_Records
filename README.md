Here’s the updated `README.md` file with the requested content:

```markdown
# README

## Additional Steps for Virtual Environment

### Create and Activate the Virtual Environment (if not already created):

#### On Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\\Scripts\\activate
```

### Install Required Dependencies:
```bash
pip install -r requirements.txt
```

## To create and initialize the data, follow these steps:

1. **Initialize the database:**
   ```bash
   flask db init
   ```

2. **Generate migration scripts:**
   ```bash
   flask db migrate
   ```

3. **Apply the migrations:**
   ```bash
   flask db upgrade
   ```

4. **Run the app:**
   ```bash
   python3 app.py
   ```

