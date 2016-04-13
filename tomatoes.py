import webbrowser
import os
import re
import json

def ReadTemplate(template):
  """ returns string of html after reading template file """
  filename = './templates/{}.html'.format(template)
  if os.path.isfile(filename):
    return ''.join([row for row in open(filename, 'r').readlines()])
  else:
    print "ERROR: ",filename," not found!";

main_page_head = ReadTemplate('main_page_head')
main_page_content = ReadTemplate('main_page_content')
movie_tile_content = ReadTemplate('movie_tile_content')

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content

def open_movies_page(movies, outputfilename):
    """ outputs movie html and opens in browser """
    # Create or overwrite the output file
    output_file = open(outputfilename, 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)

class Movie(object):
  """ simple movie class """
  def __init__(self, title, image_url, youtube_url):
    self.title = title
    self.poster_image_url = image_url
    self.trailer_youtube_url = youtube_url

  def checktrailer(self):
    webbrowser.open(self.trailer_youtube_url)

  def __str__(self):
    return self.title

def get_movies_list(filename):
  """ Extracts moves from json file """
  movies = []
  if os.path.isfile(filename):
    with open(filename) as data_file:
      data = json.load(data_file)
    for item in data:
      movies.append(Movie(item['movie_title'],
                    item['movie_poster'],
                    item['movie_trailer']
                    ))
    return movies
    
  else:
    print "ERROR: ",filename, "not found!"
    exit(0)

def main():
  """ main subroutine """
  movies = get_movies_list('data/movieslist.json')
  open_movies_page(movies, 'fresh_tomatoes.html')

if __name__ == '__main__':
  main()