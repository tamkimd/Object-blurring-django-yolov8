
# Object Blurring with Django and YOLOv8

This project automatically blurs faces and license plates in a video

## Requirements

The following are required to run this project:

- Python 
- Django 
- Moviepy
- YOLOv8
- Redis
- Celery

## Installation

1. Clone this repository to your local machine and add [this model](https://www.dropbox.com/s/f8un8g8h28pqaic/best.pt?dl=0) to /model/ :

<pre><code class="cmd"> git clone https://github.com/tamkimd/object-blurring-django-yolov8.git</pre></code>

2. Install the necessary packages:

<pre><code class="cmd">pip install -r requirements.txt</pre></code>


3. Start the Redis server:

<pre><code class="cmd">sudo service redis-server start</pre></code>

4. Start the Celery worker:


<pre><code class="cmd">celery -A main worker -P gevent -l INFO</pre></code>

5. Run the Django server:


<pre><code class="cmd">python manage.py runserver</pre></code>


## Demo

 Video :  [face blur](face_blur.mp4)
 ![](face_blur.gif)

## Reference
* [YOLOv8](https://github.com/ultralytics/ultralytics)
