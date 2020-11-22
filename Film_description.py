#!/usr/bin/env python
# coding: utf-8

# In[311]:


#/bin python3
import pandas as pd
import requests
from random import randint
from bs4 import BeautifulSoup

class Movie_Generator:
  
    def __init__(self):
        """A list of movies, downloaded in the ANCINE site.
        """
        #https://oca.ancine.gov.br/cinema -> reference
        self.movies = pd.read_excel('filmes_exibidos.xlsx',skiprows=2,skipfooter=21)
        self.rand()
    
    def clean_check(self, check):
        del check[0:]
        return check
    
    def rand(self):
        # Generate a random number which will return a movie of the dataframe
        self.rand_num = randint(0, len(self.movies))
        # Check if the movie have already been selected.
        self.check_film()
        
    def check_film(self):
        # To clean the check list, just discomment the comment below.
        #self.clean_check(check)
        if self.movies.iloc[self.rand_num][1] not in check:
            check.append(self.movies.iloc[self.rand_num][1])
        else:
            self.rand()
        print(check)
        
    def movie_name(self):
        # Return the name of the movie and the year.
        movie_name = self.movies.iloc[self.rand_num][1]
        movie_year = self.movies.iloc[self.rand_num][0]
        print('Filme: '+movie_name+' ('+str(movie_year)+')')
        return movie_name
    
    def sinopse(self, movie_name):
        # Return the sinopse and the director of the movie, obtained in google.
        try:
            movie_sinopse = 'sinopse+filme+'+movie_name.replace(' ','+')
            movie_director = 'filme+'+movie_name.replace(' ','+')
        except AttributeError:
            movie_sinopse = 'sinopse+filme+'+movie_name
            movie_director = 'filme+'+movie_name
        # url to the sinopse
        url_sinopse = f"https://google.com/search?q={movie_sinopse}"
        # url to the director
        url_director = f"https://google.com/search?q={movie_director}"
        self.google_request(url_sinopse)
        self.google_request(url_director)
        
    def google_request(self, url):
        USER_AGENT = 'Chrome/84.0.4147.105'
        headers = {"user-agent" : USER_AGENT}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            # to return the sinopse
            if 'sinopse' in url:
                self.get_sinopse(soup)
            else:
                # to return the director
                self.get_director(soup)
        else:
            print('Access denied! ('+url+')')
            
    def get_sinopse(self, soup):
        keys = soup.find_all('div', class_='BNeawe tAd8D AP7Wnd')
        html = [key.get_text() for key in keys]
        # Some movies have they sinopse incompleted in the first try, so need to check if have a end point "."
        if html[0][-1] == '.':
            sinopse = html[0]
        else:
            # This other garantee the complete sinopse
            sinopse = html[3]
        print('Sinopse: '+sinopse)
    
    def get_director(self, soup):
        keys = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        html = [key.get_text() for key in keys]
        for text in html:
            # Search for director, directora in the soup key div
            if 'Diretor' in text or 'Diretora' in text or 'Direção' in text:
                director = text
                print(director)
                # If found it, break the for
                break

    def movie_views(self):
        movie_views = self.movies.iloc[self.rand_num][-2]
        print('Dados da ANCINE')
        print('Público no Brasil: '+str(movie_views))
        
    def movie_return(self):
        movie_return = self.movies.iloc[self.rand_num][-1]
        print('Bilheteria Brasileira: R$ '+str(round(movie_return,2)))
       
    def main(self):
        self.sinopse(self.movie_name())
        self.movie_views()
        self.movie_return()
        
if __name__ == '__main__':
    x = Movie_Generator()
    x.main()

