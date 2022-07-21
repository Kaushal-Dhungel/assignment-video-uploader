# Assignment-Video Uploader

## About
This is an application that provides APIs to upload videos, list all videos as well as inquire the charges for a video provided
`size, length and extension` of the video. This is written using the `Django Rest Framework`.

### Available API endpoints:-
-- List all Videos ( GET request ) :-127.0.0.1:8000/videos
-- Upload a Video ( POST request, supports date range filter, size range filter, filter by extension ) :- 127.0.0.1:8000/videos/upload
-- Video Charges ( GET request/ size, length and extension query params are mandatory ) :- 127.0.0.1:8000/videos/charges

## Installation 
1. Clone the repo.
```sh
$ git clone https://github.com/Kaushal-Dhungel/assignment-video-uploader.git
```

2. Navigate to the cloned folder.
```sh
$ cd assignment-video-uploader
```

3. Install the dependencies.
```sh
$ pip install -r requirements.txt
```

4. Copy environment variables.
```sh
$ cp env.txt .env
```

5. Run the program.
```sh
$ python3 manage.py runserver
```

## Have a great day ..  :blush: :heart: :)