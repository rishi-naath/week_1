Since I've used multiple datasets from various sources, I decided to merge their classes and shuffle them for better training efficiency.

**Class Remapping**:
                  
  The datasets are from different sources, so this simple .py script reforms the classes for a normalized ID generation and labelling.
                  
  Eg: 
  
  - ***Dataset - A*** has car ID as ***0***.
                  
  - ***Dataset - B*** has car ID as ***1***.
                      
  - This script converts the ***Dataset - A***'s car ID ***0 ------> 1***.
                  
  Moreover, it also helps in merging the classes between the two datasets.


  **Data Merging**:

  This simple .py script allows us to create a new directory in which ***multiple datasets*** can be added and is shuffled accordingly.

  

  
