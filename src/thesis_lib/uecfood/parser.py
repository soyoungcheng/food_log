import os
import glob

import pandas as pd


def get_name_and_category(filename):
    """
    Return a dataframe containing the name and the global category for each
    label of the UEFC-FOOD-256 dataset.

    The 5 possible categories are from ChooseMyPlate and are:

    - fruit
    - protein: meat, egg, ...
    - vegetable
    - dairy
    - grain

    Parameters
    ----------
    filename: string
        path to the file containing the name and categories
        (modified version of category.txt from the dataset).

    Returns
    -------
    :class:`pandas.Dataframe`
        A pandas dataframe with:

        - _id: int
            index, starting from 1, corresponding to the label
        - _name: str
            name of the label
        - _category: category
            one of the five possible categories for a food item.

    References
    ----------
    https://en.wikipedia.org/wiki/Food_group
    http://www.choosemyplate.gov/
    """
    df = pd.read_csv(filename,
                     delimiter=r"\t|\s{2,}",
                     header=0,
                     names=["_id", "_name", "_category"],
                     engine="python")

    df = df.set_index('_id')

    df = df.drop('_category', axis=1) \
           .join(df._category.str.split(',', expand=True) \
                                 .stack().reset_index(drop=True, level=1) \
                                 .rename('_category'))

    df._category = df._category.astype("category",
                                       categories=["grain", "vegetable", "protein", "dairy", "fruit"],
                                       ordered=False)

    return df

def read_bb_info_txt(path, array):
    """
    Read the bb_info.txt to get the rectangle coordinates and its class.
    Append this information into the list 'array' (thus, **the array is
    MODIFIED**).

    The structure of the appending values is:

    - first column (int): the file name without jpg
    - second (int) and third columns (int): coordinate of one of the corner
    - fourth (int) and fifth columns (int): coordinate of the opposte corner
    - sixth column (int): category of the bbox (directory name)
    - seventh column (str): absolute path to the image

    Parameters
    ----------
    path: str
        path to the file bb_info.txt file.
    array: list, modified
        list to append the different bounding boxes
    """
    # Get the label from the path (name of the directory containing the file)
    directory = os.path.dirname(path)
    label = os.path.split(directory)[1]

    with open(path, 'r') as f:
        f.readline() # skip the first line that have the column names
        for line in f:
            # print(line)
            split_line = line.split()

            split_line.append(label)
            data = [int(i) for i in split_line]
            
            data.append(os.path.abspath(directory + "/" + split_line[0] + ".jpg"))
            array.append(data)