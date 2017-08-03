FROM python:3.6.2

MAINTAINER Laurent Vaylet <lvaylet@talend.com>

# Set the working directory (creating it if it does not exist)
WORKDIR /usr/src/app

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app's source code into the working directory
COPY . .

EXPOSE 9118
