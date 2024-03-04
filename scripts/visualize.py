import pandas as pd
import utils.visualaizer as vis

if __name__ == '__main__':

    df = pd.read_csv('../new_data/new_mouse_union/09.52.12_2023-11-23.csv')
    visual = vis.Visualizer(df)

    for el in visual.visualize_by_fragment():
        input()
