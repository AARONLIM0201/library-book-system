# Step 1: Use a lightweight Python base image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code
COPY . .

# Step 6: Expose port 5000 (Flask default)
EXPOSE 5000

# Step 7: Define the command to run the app
CMD ["python", "app.py"]
