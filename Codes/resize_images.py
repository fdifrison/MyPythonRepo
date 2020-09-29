from PIL import Image
import glob


def ls():
    'List files in cwd'
    for file in glob.glob('*'):
        print(f'\n{file}')
    print('\nThese are the files in the cwd')


class picMod:
    '''
    A Class to modify pictures
    
    Attributes
    ----------
    fname : str
            name of the picture to modify
    
    Methods
    -------
    resize(scalefactor)
        Resize the picture based on the specified scaling factor
        
    TODO
    -------
    - add other methods like: rename, change format etc..
    - add the possibility to navigate throu folders
    '''
    
    def __init__(self, fname):
        '''
        Parameters
        ----------
        fname : str
            name of the picture to modify

        '''
        
        self.fname = fname
        self.image = Image.open(self.fname)
        print(f'{self.fname} is ready to be modified')
    
    def __str__(self):
        return(f'You are modifying {self.fname}')
    
    
    def resize(self, scale_factor):
        '''
        Parameters
        ----------

        scale_factor : float
            scaling factor wrt original size
    
        Returns
        -------
        Resized image
    
        '''
        
        old_size = list(self.image.size)  
        
        self.image = self.image.resize(tuple(int(s*scale_factor) for s in old_size))
        
        print(f'{self.fname} has been scaled by a factor of {scale_factor}')
        print('Rember to save()')
        
        
    def save(self):
        '''
        Returns
        -------
        Save modified picture
        '''
        self.image.save(f'{self.fname.split(".")[0]}_mod.png')
        
        return print(f'Saving file..')
        

if __name__ == '__main__':
    info = '''
    Welcome to picture Modifier!
    type help(picMod) for more information
    type ls() for listing the files in cwd
    
    Author: Giovanni Frison
    Last Update: 05/09/2020
    Conctact: ing.giovanni.frison@gmail.com
    '''
    print(info)
