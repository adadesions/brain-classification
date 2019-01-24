from pathlib import Path

root = Path('/media/DarkDim/Thesis/dataset/RIDER NEURO MRI')

with open('dcm_list.txt', 'w') as storage:
    for folder in root.iterdir():
        sub_dir = Path(folder)
        # print(folder)
        for sub in sub_dir.iterdir():
            # print(sub)
            files = Path(sub)
            for file in files.iterdir():
                storage.writelines((str(p)+'\n' for p in list(file.glob('*.dcm'))))